import os

content = """package service;

import com.sun.net.httpserver.HttpServer;
import org.json.JSONArray;
import org.json.JSONObject;

import java.awt.Desktop;
import java.io.*;
import java.math.BigInteger;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.security.*;
import java.security.spec.RSAPublicKeySpec;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicBoolean;

public class GoogleOAuthService {

    private static String CLIENT_ID = null;
    private static final String AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth";
    private static final String TOKEN_URL = "https://oauth2.googleapis.com/token";
    private static final String JWK_URL = "https://www.googleapis.com/oauth2/v3/certs";

    // JWK Cache
    private static JSONArray cachedJwks = null;

    private AtomicBoolean isRunning = new AtomicBoolean(false);
    private HttpServer server;
    private ScheduledExecutorService timeoutExecutor;

    public interface OAuthCallback {
        void onSuccess(String subjectId, String email, String name);
        void onError(String error);
        void onCancel();
    }

    private void loadConfig() throws Exception {
        if (CLIENT_ID != null) return;
        File configFile = new File("config/oauth.properties");
        if (!configFile.exists()) {
            throw new Exception("config/oauth.properties not found.");
        }
        Properties props = new Properties();
        try (FileInputStream fis = new FileInputStream(configFile)) {
            props.load(fis);
        }
        CLIENT_ID = props.getProperty("client_id");
        if (CLIENT_ID == null || CLIENT_ID.trim().isEmpty()) {
            throw new Exception("client_id is missing in config/oauth.properties");
        }
    }

    public void startOAuthFlow(OAuthCallback callback) {
        if (!isRunning.compareAndSet(false, true)) {
            callback.onError("OAuth flow is already in progress.");
            return;
        }

        try {
            loadConfig();

            // Secure randoms
            SecureRandom sr = new SecureRandom();
            String state = generateRandomString(sr, 32);
            String nonce = generateRandomString(sr, 32);
            String codeVerifier = generateRandomString(sr, 64);
            String codeChallenge = generateCodeChallenge(codeVerifier);

            // Bind to random port
            server = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
            int port = server.getAddress().getPort();
            String redirectUri = "http://127.0.0.1:" + port + "/callback";

            server.createContext("/callback", exchange -> {
                String query = exchange.getRequestURI().getQuery();
                Map<String, String> params = parseQuery(query);

                if (params.containsKey("error")) {
                    sendHtmlResponse(exchange, "Authentication Cancelled", "You can close this tab.", false);
                    stopServer();
                    callback.onCancel();
                    return;
                }

                String code = params.get("code");
                String returnedState = params.get("state");

                if (returnedState == null || !returnedState.equals(state)) {
                    sendHtmlResponse(exchange, "Invalid Request", "State validation failed.", false);
                    stopServer();
                    callback.onError("Invalid state parameter received.");
                    return;
                }

                if (code != null) {
                    sendHtmlResponse(exchange, "Authentication Successful!", "You can close this tab and return to SmartPark Campus.", true);
                    stopServer();
                    processCode(code, codeVerifier, redirectUri, nonce, callback);
                } else {
                    sendHtmlResponse(exchange, "Authentication Failed", "Authorization code not found.", false);
                    stopServer();
                    callback.onError("Authorization code not found.");
                }
            });

            server.setExecutor(null);
            server.start();

            // Timeout after 5 minutes
            timeoutExecutor = Executors.newSingleThreadScheduledExecutor();
            timeoutExecutor.schedule(() -> {
                if (isRunning.get()) {
                    stopServer();
                    callback.onError("Google sign-in timed out. Please try again.");
                }
            }, 5, TimeUnit.MINUTES);

            // Open Default Browser
            String authRequestUrl = AUTH_URL + "?client_id=" + CLIENT_ID
                    + "&redirect_uri=" + URLEncoder.encode(redirectUri, "UTF-8")
                    + "&response_type=code"
                    + "&scope=" + URLEncoder.encode("openid email profile", "UTF-8")
                    + "&state=" + state
                    + "&nonce=" + nonce
                    + "&code_challenge=" + codeChallenge
                    + "&code_challenge_method=S256";

            if (Desktop.isDesktopSupported() && Desktop.getDesktop().isSupported(Desktop.Action.BROWSE)) {
                Desktop.getDesktop().browse(new URI(authRequestUrl));
            } else {
                stopServer();
                callback.onError("Desktop browsing is not supported.");
            }

        } catch (Exception e) {
            stopServer();
            callback.onError("Failed to start OAuth flow: " + e.getMessage());
        }
    }

    private void stopServer() {
        if (server != null) {
            server.stop(0);
            server = null;
        }
        if (timeoutExecutor != null) {
            timeoutExecutor.shutdownNow();
            timeoutExecutor = null;
        }
        isRunning.set(false);
    }

    private void sendHtmlResponse(com.sun.net.httpserver.HttpExchange exchange, String title, String message, boolean success) throws IOException {
        String color = success ? "#10B981" : "#EF4444";
        String html = "<html><body style='font-family: sans-serif; text-align: center; margin-top: 50px;'>"
                + "<h1 style='color: " + color + ";'>" + title + "</h1>"
                + "<p>" + message + "</p></body></html>";
        exchange.sendResponseHeaders(200, html.length());
        OutputStream os = exchange.getResponseBody();
        os.write(html.getBytes());
        os.close();
    }

    private void processCode(String code, String codeVerifier, String redirectUri, String nonce, OAuthCallback callback) {
        new Thread(() -> {
            try {
                URL url = new URL(TOKEN_URL);
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("POST");
                conn.setDoOutput(true);
                conn.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");

                String postData = "code=" + URLEncoder.encode(code, "UTF-8")
                        + "&client_id=" + URLEncoder.encode(CLIENT_ID, "UTF-8")
                        + "&redirect_uri=" + URLEncoder.encode(redirectUri, "UTF-8")
                        + "&code_verifier=" + URLEncoder.encode(codeVerifier, "UTF-8")
                        + "&grant_type=authorization_code";

                OutputStream os = conn.getOutputStream();
                os.write(postData.getBytes(StandardCharsets.UTF_8));
                os.flush();
                os.close();

                if (conn.getResponseCode() == 200) {
                    InputStream is = conn.getInputStream();
                    byte[] response = is.readAllBytes();
                    String jsonResponse = new String(response, StandardCharsets.UTF_8);
                    JSONObject json = new JSONObject(jsonResponse);
                    
                    if (json.has("id_token")) {
                        String idToken = json.getString("id_token");
                        validateAndProcessIdToken(idToken, nonce, callback);
                    } else {
                        callback.onError("No id_token found in response.");
                    }
                } else {
                    callback.onError("Token exchange failed with HTTP " + conn.getResponseCode());
                }
            } catch (Exception e) {
                callback.onError("Error during token exchange.");
            }
        }).start();
    }

    private void validateAndProcessIdToken(String idToken, String expectedNonce, OAuthCallback callback) {
        try {
            String[] parts = idToken.split("\\.");
            if (parts.length != 3) {
                callback.onError("Invalid ID token format.");
                return;
            }

            String headerJson = new String(Base64.getUrlDecoder().decode(parts[0]), StandardCharsets.UTF_8);
            String payloadJson = new String(Base64.getUrlDecoder().decode(parts[1]), StandardCharsets.UTF_8);
            
            JSONObject header = new JSONObject(headerJson);
            JSONObject payload = new JSONObject(payloadJson);

            String kid = header.optString("kid", null);
            if (kid == null) {
                callback.onError("Missing kid in ID token.");
                return;
            }

            PublicKey pubKey = getGooglePublicKey(kid);
            if (pubKey == null) {
                callback.onError("Google sign-in could not be completed. Key not found.");
                return;
            }

            // Verify signature
            Signature sig = Signature.getInstance("SHA256withRSA");
            sig.initVerify(pubKey);
            sig.update((parts[0] + "." + parts[1]).getBytes(StandardCharsets.UTF_8));
            if (!sig.verify(Base64.getUrlDecoder().decode(parts[2]))) {
                callback.onError("ID token signature is invalid.");
                return;
            }

            // Verify claims
            String iss = payload.optString("iss", "");
            if (!iss.equals("accounts.google.com") && !iss.equals("https://accounts.google.com")) {
                callback.onError("Invalid issuer.");
                return;
            }
            
            String aud = payload.optString("aud", "");
            if (!aud.equals(CLIENT_ID)) {
                callback.onError("Invalid audience.");
                return;
            }
            
            long exp = payload.optLong("exp", 0);
            long now = System.currentTimeMillis() / 1000;
            if (exp < now) {
                callback.onError("ID token has expired.");
                return;
            }
            
            String tokenNonce = payload.optString("nonce", null);
            if (tokenNonce == null || !tokenNonce.equals(expectedNonce)) {
                callback.onError("Invalid nonce.");
                return;
            }
            
            String sub = payload.optString("sub", null);
            String email = payload.optString("email", null);
            boolean emailVerified = payload.optBoolean("email_verified", false);
            String name = payload.optString("name", "");

            if (sub == null || email == null || !emailVerified) {
                callback.onError("Incomplete profile information or email not verified.");
                return;
            }

            callback.onSuccess(sub, email, name);

        } catch (Exception e) {
            e.printStackTrace();
            callback.onError("Failed to validate ID token.");
        }
    }

    private PublicKey getGooglePublicKey(String kid) throws Exception {
        if (cachedJwks == null) {
            fetchJwks();
        }
        PublicKey key = findKey(kid);
        if (key == null) {
            // refresh once
            fetchJwks();
            key = findKey(kid);
        }
        return key;
    }

    private PublicKey findKey(String kid) throws Exception {
        if (cachedJwks == null) return null;
        for (int i = 0; i < cachedJwks.length(); i++) {
            JSONObject jwk = cachedJwks.getJSONObject(i);
            if (kid.equals(jwk.optString("kid"))) {
                String nStr = jwk.getString("n");
                String eStr = jwk.getString("e");
                BigInteger n = new BigInteger(1, Base64.getUrlDecoder().decode(nStr));
                BigInteger e = new BigInteger(1, Base64.getUrlDecoder().decode(eStr));
                RSAPublicKeySpec spec = new RSAPublicKeySpec(n, e);
                KeyFactory kf = KeyFactory.getInstance("RSA");
                return kf.generatePublic(spec);
            }
        }
        return null;
    }

    private void fetchJwks() throws Exception {
        URL url = new URL(JWK_URL);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("GET");
        if (conn.getResponseCode() == 200) {
            InputStream is = conn.getInputStream();
            String jsonStr = new String(is.readAllBytes(), StandardCharsets.UTF_8);
            JSONObject root = new JSONObject(jsonStr);
            cachedJwks = root.getJSONArray("keys");
        }
    }

    private String generateRandomString(SecureRandom sr, int length) {
        byte[] bytes = new byte[length];
        sr.nextBytes(bytes);
        return Base64.getUrlEncoder().withoutPadding().encodeToString(bytes);
    }

    private String generateCodeChallenge(String verifier) throws Exception {
        MessageDigest md = MessageDigest.getInstance("SHA-256");
        byte[] digest = md.digest(verifier.getBytes(StandardCharsets.US_ASCII));
        return Base64.getUrlEncoder().withoutPadding().encodeToString(digest);
    }

    private Map<String, String> parseQuery(String query) {
        Map<String, String> params = new HashMap<>();
        if (query == null) return params;
        String[] pairs = query.split("&");
        for (String pair : pairs) {
            String[] idx = pair.split("=");
            if (idx.length > 1) {
                params.put(idx[0], idx[1]);
            } else if (idx.length == 1) {
                params.put(idx[0], "");
            }
        }
        return params;
    }
}
"""

with open(r"C:\Development\newsrm\SmartPark\src\service\GoogleOAuthService.java", "w", encoding="utf-8") as f:
    f.write(content)

print("Generated GoogleOAuthService.java")
