import os

content = """package gui;

import dao.UserDAO;
import model.Student;
import model.User;
import service.GoogleOAuthService;
import gui.components.ui.ModernButton;
import gui.components.ui.ModernTextField;
import gui.components.ui.PasswordStrengthPanel;
import gui.components.ui.RoundedPanel;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import java.awt.*;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.sql.Date;

public class LoginFrame extends JFrame {

    private CardLayout cardLayout;
    private JPanel rightPanel;
    private UserDAO userDAO;
    private GoogleOAuthService oauthService;
    
    // Wizard state
    private String wizGoogleEmail = "";
    private String wizGoogleSubjectId = "";
    private String wizGoogleName = "";
    
    private String wizFullName = "";
    private Date wizDob = null;
    private String wizGender = "";
    private String wizMobile = "";
    private String wizPersonalEmail = "";
    private String wizAddress = "";
    
    private String wizRegNo = "";
    private String wizCollegeId = "";
    private String wizDept = "";
    private String wizProgram = "";
    private int wizYear = 1;
    private String wizSection = "";

    public LoginFrame() {
        userDAO = new UserDAO();
        oauthService = new GoogleOAuthService();
        setTitle("SmartPark Campus - Login");
        setSize(1000, 700);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        setResizable(false);
        initComponents();
    }

    private void initComponents() {
        JPanel mainPanel = new JPanel(new GridLayout(1, 2));
        mainPanel.setBackground(Color.WHITE);

        // Left Side: Dark Hero Section
        JPanel leftPanel = new JPanel(new BorderLayout()) {
            @Override
            protected void paintComponent(Graphics g) {
                super.paintComponent(g);
                Graphics2D g2 = (Graphics2D) g.create();
                g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
                g2.setColor(new Color(15, 23, 42)); // Deep Navy
                g2.fillRect(0, 0, getWidth(), getHeight());
                
                g2.setColor(new Color(56, 189, 248, 20));
                g2.fillOval(-50, -50, 200, 200);
                
                g2.setColor(new Color(139, 92, 246, 30));
                g2.fillOval(getWidth() - 150, getHeight() - 150, 300, 300);
                g2.dispose();
            }
        };

        JPanel brandingPanel = new JPanel();
        brandingPanel.setOpaque(false);
        brandingPanel.setLayout(new BoxLayout(brandingPanel, BoxLayout.Y_AXIS));
        brandingPanel.setBorder(new EmptyBorder(100, 50, 50, 50));

        JLabel lblTitle = new JLabel("SMARTPARK");
        lblTitle.setFont(new Font("Segoe UI", Font.BOLD, 42));
        lblTitle.setForeground(Color.WHITE);
        
        JLabel lblTitle2 = new JLabel("CAMPUS");
        lblTitle2.setFont(new Font("Segoe UI", Font.BOLD, 42));
        lblTitle2.setForeground(new Color(56, 189, 248));

        JLabel lblSubtitle = new JLabel("<html><br><br>Intelligent College Parking<br>& Access Management</html>");
        lblSubtitle.setFont(new Font("Segoe UI", Font.PLAIN, 20));
        lblSubtitle.setForeground(new Color(203, 213, 225));

        brandingPanel.add(lblTitle);
        brandingPanel.add(lblTitle2);
        brandingPanel.add(lblSubtitle);
        leftPanel.add(brandingPanel, BorderLayout.CENTER);

        // Right Side: CardLayout
        cardLayout = new CardLayout();
        rightPanel = new JPanel(cardLayout);
        rightPanel.setBackground(new Color(248, 250, 252));

        rightPanel.add(createWelcomeCard(), "WELCOME");
        rightPanel.add(createRegLoginCard(), "REG_LOGIN");
        rightPanel.add(createStaffLoginCard(), "STAFF_LOGIN");
        rightPanel.add(createWizStep1Card(), "WIZ_STEP1");
        rightPanel.add(createWizStep2Card(), "WIZ_STEP2");
        rightPanel.add(createWizStep3Card(), "WIZ_STEP3");
        rightPanel.add(createWizStep4Card(), "WIZ_STEP4");
        rightPanel.add(createWizStep5Card(), "WIZ_STEP5");
        rightPanel.add(createSuccessCard(), "SUCCESS");

        mainPanel.add(leftPanel);
        mainPanel.add(rightPanel);
        add(mainPanel);
        
        cardLayout.show(rightPanel, "WELCOME");
    }

    private RoundedPanel createBaseCard() {
        RoundedPanel card = new RoundedPanel(20, Color.WHITE);
        card.setLayout(new GridBagLayout());
        card.setPreferredSize(new Dimension(380, 560));
        card.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(new Color(226, 232, 240)),
                new EmptyBorder(10, 10, 10, 10)
        ));
        return card;
    }

    private GridBagConstraints createGbc() {
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.gridx = 0;
        gbc.gridy = 0;
        gbc.weightx = 1.0;
        gbc.fill = GridBagConstraints.HORIZONTAL;
        gbc.insets = new Insets(5, 20, 5, 20);
        return gbc;
    }

    private void addBackButton(JPanel card, GridBagConstraints gbc, String targetCard) {
        gbc.insets = new Insets(10, 10, 10, 10);
        gbc.anchor = GridBagConstraints.WEST;
        gbc.fill = GridBagConstraints.NONE;
        JLabel lblBack = new JLabel("← Back");
        lblBack.setFont(new Font("Segoe UI", Font.BOLD, 14));
        lblBack.setForeground(new Color(100, 116, 139));
        lblBack.setCursor(new Cursor(Cursor.HAND_CURSOR));
        lblBack.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                cardLayout.show(rightPanel, targetCard);
            }
        });
        card.add(lblBack, gbc);
        gbc.fill = GridBagConstraints.HORIZONTAL;
        gbc.anchor = GridBagConstraints.CENTER;
        gbc.insets = new Insets(5, 20, 5, 20);
    }

    // =========================================================================
    // CARD: WELCOME (First Screen)
    // =========================================================================
    private JPanel createWelcomeCard() {
        JPanel panel = new JPanel(new GridBagLayout());
        panel.setOpaque(false);
        RoundedPanel card = createBaseCard();
        GridBagConstraints gbc = createGbc();

        JLabel lblWelcome = new JLabel("Welcome to SmartPark", SwingConstants.CENTER);
        lblWelcome.setFont(new Font("Segoe UI", Font.BOLD, 22));
        lblWelcome.setForeground(new Color(15, 23, 42));
        card.add(lblWelcome, gbc);

        gbc.gridy++;
        gbc.insets = new Insets(5, 20, 30, 20);
        JLabel lblSub = new JLabel("Secure Campus Parking Access", SwingConstants.CENTER);
        lblSub.setFont(new Font("Segoe UI", Font.PLAIN, 14));
        lblSub.setForeground(new Color(100, 116, 139));
        card.add(lblSub, gbc);

        gbc.gridy++;
        gbc.insets = new Insets(10, 20, 20, 20);
        ModernButton btnGoogle = new ModernButton("G  Continue with Google", new Color(255, 255, 255), new Color(241, 245, 249), Color.BLACK, 10);
        btnGoogle.setBorder(BorderFactory.createLineBorder(new Color(203, 213, 225)));
        btnGoogle.setPreferredSize(new Dimension(0, 50));
        btnGoogle.setFont(new Font("Segoe UI", Font.BOLD, 14));
        btnGoogle.addActionListener(e -> {
            setCursor(Cursor.getPredefinedCursor(Cursor.WAIT_CURSOR));
            oauthService.startOAuthFlow(new GoogleOAuthService.OAuthCallback() {
                @Override
                public void onSuccess(String email) {
                    SwingUtilities.invokeLater(() -> {
                        setCursor(Cursor.getDefaultCursor());
                        User u = userDAO.loginWithGoogle(email, email);
                        if (u != null) {
                            launchDashboard(u);
                        } else {
                            wizGoogleEmail = email;
                            wizGoogleName = email.split("@")[0]; 
                            wizGoogleSubjectId = email; 
                            cardLayout.show(rightPanel, "WIZ_STEP1");
                            updateWizStep1();
                        }
                    });
                }
                @Override
                public void onError(String error) {
                    SwingUtilities.invokeLater(() -> {
                        setCursor(Cursor.getDefaultCursor());
                        JOptionPane.showMessageDialog(LoginFrame.this, error, "Google Login Error", JOptionPane.ERROR_MESSAGE);
                    });
                }
            });
        });
        card.add(btnGoogle, gbc);

        gbc.gridy++;
        gbc.insets = new Insets(20, 20, 5, 20);
        JLabel lblNew = new JLabel("New to SmartPark? Create your student account", SwingConstants.CENTER);
        lblNew.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        lblNew.setForeground(new Color(100, 116, 139));
        card.add(lblNew, gbc);

        gbc.gridy++;
        gbc.insets = new Insets(5, 20, 15, 20);
        JLabel lblCreate = new JLabel("<html><u>Create Student Account</u></html>", SwingConstants.CENTER);
        lblCreate.setFont(new Font("Segoe UI", Font.BOLD, 13));
        lblCreate.setForeground(new Color(16, 185, 129));
        lblCreate.setCursor(new Cursor(Cursor.HAND_CURSOR));
        lblCreate.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                JOptionPane.showMessageDialog(LoginFrame.this, "Please click 'Continue with Google' to verify your identity first.", "Verification Required", JOptionPane.INFORMATION_MESSAGE);
            }
        });
        card.add(lblCreate, gbc);

        gbc.gridy++;
        gbc.insets = new Insets(15, 20, 5, 20);
        JLabel lblLogin = new JLabel("<html><u>Login with Registration Number</u></html>", SwingConstants.CENTER);
        lblLogin.setFont(new Font("Segoe UI", Font.BOLD, 13));
        lblLogin.setForeground(new Color(14, 165, 233));
        lblLogin.setCursor(new Cursor(Cursor.HAND_CURSOR));
        lblLogin.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                cardLayout.show(rightPanel, "REG_LOGIN");
            }
        });
        card.add(lblLogin, gbc);

        gbc.gridy++;
        gbc.insets = new Insets(15, 20, 10, 20);
        JLabel lblStaff = new JLabel("<html><u>Staff / Security Login</u></html>", SwingConstants.CENTER);
        lblStaff.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        lblStaff.setForeground(new Color(100, 116, 139));
        lblStaff.setCursor(new Cursor(Cursor.HAND_CURSOR));
        lblStaff.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                cardLayout.show(rightPanel, "STAFF_LOGIN");
            }
        });
        card.add(lblStaff, gbc);

        panel.add(card);
        return panel;
    }

    // =========================================================================
    // CARD: REGISTRATION NUMBER LOGIN
    // =========================================================================
    private JPanel createRegLoginCard() {
        JPanel panel = new JPanel(new GridBagLayout());
        panel.setOpaque(false);
        RoundedPanel card = createBaseCard();
        GridBagConstraints gbc = createGbc();

        addBackButton(card, gbc, "WELCOME");

        JLabel lblTitle = new JLabel("Student Login", SwingConstants.CENTER);
        lblTitle.setFont(new Font("Segoe UI", Font.BOLD, 22));
        lblTitle.setForeground(new Color(15, 23, 42));
        card.add(lblTitle, gbc);

        gbc.gridy++;
        gbc.insets = new Insets(20, 20, 5, 20);
        JLabel lblUser = new JLabel("Registration Number");
        lblUser.setFont(new Font("Segoe UI", Font.BOLD, 12));
        card.add(lblUser, gbc);

        gbc.gridy++;
        ModernTextField txtReg = new ModernTextField(20);
        card.add(txtReg, gbc);

        gbc.gridy++;
        gbc.insets = new Insets(15, 20, 5, 20);
        JLabel lblPass = new JLabel("Password");
        lblPass.setFont(new Font("Segoe UI", Font.BOLD, 12));
        card.add(lblPass, gbc);

        gbc.gridy++;
        JPasswordField txtPass = new JPasswordField(20);
        txtPass.setPreferredSize(new Dimension(0, 40));
        card.add(txtPass, gbc);

        gbc.gridy++;
        gbc.insets = new Insets(30, 20, 20, 20);
        ModernButton btnLogin = new ModernButton("LOGIN", new Color(14, 165, 233), new Color(2, 132, 199), Color.WHITE, 10);
        btnLogin.setPreferredSize(new Dimension(0, 45));
        btnLogin.addActionListener(e -> {
            String reg = txtReg.getText().trim();
            String pass = new String(txtPass.getPassword());
            if (reg.isEmpty() || pass.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Please enter all fields.", "Error", JOptionPane.ERROR_MESSAGE);
                return;
            }
            User u = userDAO.getStudentByRegistrationNumber(reg);
            if (u == null) {
                JOptionPane.showMessageDialog(this, "Registration number not found.", "Error", JOptionPane.ERROR_MESSAGE);
            } else {
                User loggedIn = userDAO.login(u.getUsername(), hashPassword(pass));
                if (loggedIn != null) {
                    launchDashboard(loggedIn);
                } else {
                    if (userDAO.isUserActive(u.getUsername())) {
                        JOptionPane.showMessageDialog(this, "Incorrect password. Please try again.", "Error", JOptionPane.ERROR_MESSAGE);
                    } else {
                        JOptionPane.showMessageDialog(this, "Your account is not active. Please contact the administrator.", "Error", JOptionPane.ERROR_MESSAGE);
                    }
                }
            }
        });
        card.add(btnLogin, gbc);

        panel.add(card);
        return panel;
    }

    // =========================================================================
    // CARD: WIZARD STEP 1 (Google Verified)
    // =========================================================================
    private JLabel lblWiz1Name;
    private JLabel lblWiz1Email;
    
    private JPanel createWizStep1Card() {
        JPanel panel = new JPanel(new GridBagLayout());
        panel.setOpaque(false);
        RoundedPanel card = createBaseCard();
        GridBagConstraints gbc = createGbc();

        addBackButton(card, gbc, "WELCOME");

        JLabel lblTitle = new JLabel("Step 1 of 5", SwingConstants.CENTER);
        lblTitle.setFont(new Font("Segoe UI", Font.BOLD, 16));
        lblTitle.setForeground(new Color(14, 165, 233));
        card.add(lblTitle, gbc);

        gbc.gridy++;
        JLabel lblSub = new JLabel("Google Account Verified", SwingConstants.CENTER);
        lblSub.setFont(new Font("Segoe UI", Font.BOLD, 20));
        card.add(lblSub, gbc);

        gbc.gridy++;
        gbc.insets = new Insets(20, 20, 10, 20);
        JLabel lblMsg = new JLabel("<html><center>Your Google account has been successfully verified.</center></html>", SwingConstants.CENTER);
        lblMsg.setForeground(new Color(16, 185, 129));
        card.add(lblMsg, gbc);

        gbc.gridy++;
        gbc.insets = new Insets(20, 20, 5, 20);
        lblWiz1Name = new JLabel("Name: ");
        lblWiz1Name.setFont(new Font("Segoe UI", Font.BOLD, 14));
        card.add(lblWiz1Name, gbc);

        gbc.gridy++;
        lblWiz1Email = new JLabel("Email: ");
        lblWiz1Email.setFont(new Font("Segoe UI", Font.PLAIN, 14));
        lblWiz1Email.setForeground(Color.GRAY);
        card.add(lblWiz1Email, gbc);

        gbc.gridy++;
        gbc.insets = new Insets(40, 20, 20, 20);
        ModernButton btnNext = new ModernButton("Continue →", new Color(14, 165, 233), new Color(2, 132, 199), Color.WHITE, 10);
        btnNext.setPreferredSize(new Dimension(0, 45));
        btnNext.addActionListener(e -> cardLayout.show(rightPanel, "WIZ_STEP2"));
        card.add(btnNext, gbc);

        panel.add(card);
        return panel;
    }
    
    private void updateWizStep1() {
        lblWiz1Name.setText("Name: " + wizGoogleName);
        lblWiz1Email.setText("Email: " + wizGoogleEmail);
    }

    // =========================================================================
    // CARD: WIZARD STEP 2 (Personal Details)
    // =========================================================================
    private ModernTextField txtWizName, txtWizMobile, txtWizEmail, txtWizAddress;
    
    private JPanel createWizStep2Card() {
        JPanel panel = new JPanel(new GridBagLayout());
        panel.setOpaque(false);
        RoundedPanel card = createBaseCard();
        GridBagConstraints gbc = createGbc();

        addBackButton(card, gbc, "WIZ_STEP1");

        JLabel lblTitle = new JLabel("Step 2 of 5: Personal Details", SwingConstants.CENTER);
        lblTitle.setFont(new Font("Segoe UI", Font.BOLD, 18));
        card.add(lblTitle, gbc);

        gbc.gridy++;
        gbc.insets = new Insets(10, 20, 2, 20);
        card.add(new JLabel("Full Name"), gbc);
        gbc.gridy++;
        txtWizName = new ModernTextField(20);
        card.add(txtWizName, gbc);

        gbc.gridy++;
        card.add(new JLabel("Mobile Number"), gbc);
        gbc.gridy++;
        txtWizMobile = new ModernTextField(20);
        card.add(txtWizMobile, gbc);

        gbc.gridy++;
        card.add(new JLabel("Personal Email"), gbc);
        gbc.gridy++;
        txtWizEmail = new ModernTextField(20);
        card.add(txtWizEmail, gbc);

        gbc.gridy++;
        card.add(new JLabel("Address"), gbc);
        gbc.gridy++;
        txtWizAddress = new ModernTextField(20);
        card.add(txtWizAddress, gbc);

        gbc.gridy++;
        gbc.insets = new Insets(20, 20, 10, 20);
        ModernButton btnNext = new ModernButton("Continue →", new Color(14, 165, 233), new Color(2, 132, 199), Color.WHITE, 10);
        btnNext.setPreferredSize(new Dimension(0, 45));
        btnNext.addActionListener(e -> {
            wizFullName = txtWizName.getText().trim();
            wizMobile = txtWizMobile.getText().trim();
            wizPersonalEmail = txtWizEmail.getText().trim();
            wizAddress = txtWizAddress.getText().trim();
            
            if (wizFullName.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Full Name is required.");
                return;
            }
            cardLayout.show(rightPanel, "WIZ_STEP3");
        });
        card.add(btnNext, gbc);

        panel.add(card);
        return panel;
    }

    // =========================================================================
    // CARD: WIZARD STEP 3 (College Details)
    // =========================================================================
    private ModernTextField txtWizReg, txtWizCollegeId, txtWizDept, txtWizProg, txtWizSec;
    
    private JPanel createWizStep3Card() {
        JPanel panel = new JPanel(new GridBagLayout());
        panel.setOpaque(false);
        RoundedPanel card = createBaseCard();
        GridBagConstraints gbc = createGbc();

        addBackButton(card, gbc, "WIZ_STEP2");

        JLabel lblTitle = new JLabel("Step 3 of 5: College Details", SwingConstants.CENTER);
        lblTitle.setFont(new Font("Segoe UI", Font.BOLD, 18));
        card.add(lblTitle, gbc);

        gbc.gridy++;
        gbc.insets = new Insets(10, 20, 2, 20);
        card.add(new JLabel("Registration Number *"), gbc);
        gbc.gridy++;
        txtWizReg = new ModernTextField(20);
        card.add(txtWizReg, gbc);

        gbc.gridy++;
        card.add(new JLabel("College ID"), gbc);
        gbc.gridy++;
        txtWizCollegeId = new ModernTextField(20);
        card.add(txtWizCollegeId, gbc);

        gbc.gridy++;
        card.add(new JLabel("Department"), gbc);
        gbc.gridy++;
        txtWizDept = new ModernTextField(20);
        card.add(txtWizDept, gbc);

        gbc.gridy++;
        card.add(new JLabel("Program"), gbc);
        gbc.gridy++;
        txtWizProg = new ModernTextField(20);
        card.add(txtWizProg, gbc);

        gbc.gridy++;
        gbc.insets = new Insets(20, 20, 10, 20);
        ModernButton btnNext = new ModernButton("Continue →", new Color(14, 165, 233), new Color(2, 132, 199), Color.WHITE, 10);
        btnNext.setPreferredSize(new Dimension(0, 45));
        btnNext.addActionListener(e -> {
            wizRegNo = txtWizReg.getText().trim();
            if (wizRegNo.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Registration Number is required.");
                return;
            }
            User existing = userDAO.getStudentByRegistrationNumber(wizRegNo);
            if (existing != null) {
                JOptionPane.showMessageDialog(this, "Registration number already exists. Cannot create a duplicate account.", "Error", JOptionPane.ERROR_MESSAGE);
                return;
            }
            
            wizCollegeId = txtWizCollegeId.getText().trim();
            wizDept = txtWizDept.getText().trim();
            wizProgram = txtWizProg.getText().trim();
            
            cardLayout.show(rightPanel, "WIZ_STEP4");
        });
        card.add(btnNext, gbc);

        panel.add(card);
        return panel;
    }

    // =========================================================================
    // CARD: WIZARD STEP 4 (Password)
    // =========================================================================
    private JPasswordField txtWizPass, txtWizConfPass;
    private String finalHash = "";
    
    private JPanel createWizStep4Card() {
        JPanel panel = new JPanel(new GridBagLayout());
        panel.setOpaque(false);
        RoundedPanel card = createBaseCard();
        GridBagConstraints gbc = createGbc();

        addBackButton(card, gbc, "WIZ_STEP3");

        JLabel lblTitle = new JLabel("Step 4 of 5: Create Password", SwingConstants.CENTER);
        lblTitle.setFont(new Font("Segoe UI", Font.BOLD, 18));
        card.add(lblTitle, gbc);

        gbc.gridy++;
        gbc.insets = new Insets(20, 20, 5, 20);
        card.add(new JLabel("Create Password"), gbc);
        
        gbc.gridy++;
        txtWizPass = new JPasswordField(20);
        txtWizPass.setPreferredSize(new Dimension(0, 40));
        card.add(txtWizPass, gbc);

        gbc.gridy++;
        gbc.insets = new Insets(5, 20, 5, 20);
        PasswordStrengthPanel strengthPanel = new PasswordStrengthPanel();
        card.add(strengthPanel, gbc);
        
        txtWizPass.getDocument().addDocumentListener(new javax.swing.event.DocumentListener() {
            public void insertUpdate(javax.swing.event.DocumentEvent e) { strengthPanel.updateStrength(new String(txtWizPass.getPassword())); }
            public void removeUpdate(javax.swing.event.DocumentEvent e) { strengthPanel.updateStrength(new String(txtWizPass.getPassword())); }
            public void changedUpdate(javax.swing.event.DocumentEvent e) { strengthPanel.updateStrength(new String(txtWizPass.getPassword())); }
        });

        gbc.gridy++;
        gbc.insets = new Insets(15, 20, 5, 20);
        card.add(new JLabel("Confirm Password"), gbc);

        gbc.gridy++;
        txtWizConfPass = new JPasswordField(20);
        txtWizConfPass.setPreferredSize(new Dimension(0, 40));
        card.add(txtWizConfPass, gbc);

        gbc.gridy++;
        gbc.insets = new Insets(30, 20, 10, 20);
        ModernButton btnNext = new ModernButton("Continue →", new Color(14, 165, 233), new Color(2, 132, 199), Color.WHITE, 10);
        btnNext.setPreferredSize(new Dimension(0, 45));
        btnNext.addActionListener(e -> {
            String p1 = new String(txtWizPass.getPassword());
            String p2 = new String(txtWizConfPass.getPassword());
            if (p1.isEmpty() || !p1.equals(p2)) {
                JOptionPane.showMessageDialog(this, "Passwords do not match.");
                return;
            }
            if (!strengthPanel.isStrongEnough()) {
                JOptionPane.showMessageDialog(this, "Password is too weak. Please include uppercase, lowercase, numbers, and special characters.");
                return;
            }
            finalHash = hashPassword(p1);
            updateWizStep5();
            cardLayout.show(rightPanel, "WIZ_STEP5");
        });
        card.add(btnNext, gbc);

        panel.add(card);
        return panel;
    }

    // =========================================================================
    // CARD: WIZARD STEP 5 (Review)
    // =========================================================================
    private JTextArea txtReview;
    private JCheckBox chkConfirm;
    
    private JPanel createWizStep5Card() {
        JPanel panel = new JPanel(new GridBagLayout());
        panel.setOpaque(false);
        RoundedPanel card = createBaseCard();
        GridBagConstraints gbc = createGbc();

        addBackButton(card, gbc, "WIZ_STEP4");

        JLabel lblTitle = new JLabel("Step 5 of 5: Review & Confirm", SwingConstants.CENTER);
        lblTitle.setFont(new Font("Segoe UI", Font.BOLD, 18));
        card.add(lblTitle, gbc);

        gbc.gridy++;
        txtReview = new JTextArea(10, 20);
        txtReview.setEditable(false);
        txtReview.setOpaque(false);
        txtReview.setFont(new Font("Segoe UI", Font.PLAIN, 13));
        JScrollPane scroll = new JScrollPane(txtReview);
        scroll.setBorder(BorderFactory.createLineBorder(Color.LIGHT_GRAY));
        card.add(scroll, gbc);

        gbc.gridy++;
        chkConfirm = new JCheckBox("I confirm that the information provided is correct.");
        chkConfirm.setOpaque(false);
        card.add(chkConfirm, gbc);

        gbc.gridy++;
        gbc.insets = new Insets(20, 20, 10, 20);
        ModernButton btnSubmit = new ModernButton("Create SmartPark Account", new Color(16, 185, 129), new Color(5, 150, 105), Color.WHITE, 10);
        btnSubmit.setPreferredSize(new Dimension(0, 45));
        btnSubmit.addActionListener(e -> {
            if (!chkConfirm.isSelected()) {
                JOptionPane.showMessageDialog(this, "Please confirm your information.");
                return;
            }
            
            Student s = new Student(0, wizFullName, wizRegNo, wizRegNo);
            s.setGoogleEmail(wizGoogleEmail);
            s.setGoogleSubjectId(wizGoogleSubjectId);
            s.setMobile(wizMobile);
            s.setPersonalEmail(wizPersonalEmail);
            s.setAddress(wizAddress);
            s.setDepartment(wizDept);
            s.setProgram(wizProgram);
            s.setDob(wizDob); // null initially, ok
            
            if (userDAO.createStudent(s, finalHash)) {
                cardLayout.show(rightPanel, "SUCCESS");
            } else {
                JOptionPane.showMessageDialog(this, "Database verification failed. Account creation aborted.");
            }
        });
        card.add(btnSubmit, gbc);

        panel.add(card);
        return panel;
    }
    
    private void updateWizStep5() {
        txtReview.setText(
            "Google Account: " + wizGoogleEmail + "\n" +
            "Full Name: " + wizFullName + "\n" +
            "Mobile: " + wizMobile + "\n" +
            "Registration Number: " + wizRegNo + "\n" +
            "Department: " + wizDept + "\n" +
            "Program: " + wizProgram + "\n"
        );
    }

    // =========================================================================
    // CARD: SUCCESS
    // =========================================================================
    private JPanel createSuccessCard() {
        JPanel panel = new JPanel(new GridBagLayout());
        panel.setOpaque(false);
        RoundedPanel card = createBaseCard();
        GridBagConstraints gbc = createGbc();

        JLabel lblIcon = new JLabel("✓", SwingConstants.CENTER);
        lblIcon.setFont(new Font("Segoe UI", Font.BOLD, 48));
        lblIcon.setForeground(new Color(16, 185, 129));
        card.add(lblIcon, gbc);

        gbc.gridy++;
        JLabel lblTitle = new JLabel("Account Created Successfully", SwingConstants.CENTER);
        lblTitle.setFont(new Font("Segoe UI", Font.BOLD, 22));
        card.add(lblTitle, gbc);

        gbc.gridy++;
        JLabel lblSub = new JLabel("Your SmartPark student account is ready.", SwingConstants.CENTER);
        card.add(lblSub, gbc);

        gbc.gridy++;
        gbc.insets = new Insets(30, 20, 20, 20);
        ModernButton btnGo = new ModernButton("Go to Login", new Color(14, 165, 233), new Color(2, 132, 199), Color.WHITE, 10);
        btnGo.setPreferredSize(new Dimension(0, 45));
        btnGo.addActionListener(e -> {
            cardLayout.show(rightPanel, "REG_LOGIN");
        });
        card.add(btnGo, gbc);

        panel.add(card);
        return panel;
    }

    // =========================================================================
    // CARD: STAFF LOGIN (Existing)
    // =========================================================================
    private JPanel createStaffLoginCard() {
        JPanel panel = new JPanel(new GridBagLayout());
        panel.setOpaque(false);
        RoundedPanel card = createBaseCard();
        GridBagConstraints gbc = createGbc();

        addBackButton(card, gbc, "WELCOME");

        JLabel lblWelcome = new JLabel("Staff & Security", SwingConstants.CENTER);
        lblWelcome.setFont(new Font("Segoe UI", Font.BOLD, 22));
        lblWelcome.setForeground(new Color(15, 23, 42));
        card.add(lblWelcome, gbc);

        gbc.gridy++;
        gbc.insets = new Insets(20, 20, 5, 20);
        JLabel lblUser = new JLabel("Username");
        lblUser.setFont(new Font("Segoe UI", Font.BOLD, 12));
        card.add(lblUser, gbc);

        gbc.gridy++;
        ModernTextField txtStaffUser = new ModernTextField(20);
        card.add(txtStaffUser, gbc);

        gbc.gridy++;
        gbc.insets = new Insets(15, 20, 5, 20);
        JLabel lblPass = new JLabel("Password");
        lblPass.setFont(new Font("Segoe UI", Font.BOLD, 12));
        card.add(lblPass, gbc);

        gbc.gridy++;
        JPasswordField txtStaffPass = new JPasswordField(20);
        txtStaffPass.setPreferredSize(new Dimension(0, 40));
        card.add(txtStaffPass, gbc);

        gbc.gridy++;
        gbc.insets = new Insets(30, 20, 20, 20);
        ModernButton btnLogin = new ModernButton("STAFF LOGIN", new Color(15, 23, 42), new Color(30, 41, 59), Color.WHITE, 10);
        btnLogin.setPreferredSize(new Dimension(0, 45));
        btnLogin.addActionListener(e -> {
            String u = txtStaffUser.getText().trim();
            String p = new String(txtStaffPass.getPassword());
            User user = userDAO.login(u, hashPassword(p));
            if (user != null && !user.getRole().equals("STUDENT")) {
                launchDashboard(user);
            } else {
                JOptionPane.showMessageDialog(this, "Invalid credentials or unauthorized.", "Error", JOptionPane.ERROR_MESSAGE);
            }
        });
        card.add(btnLogin, gbc);

        panel.add(card);
        return panel;
    }

    private void launchDashboard(User u) {
        if (u.getRole().equals("STUDENT")) {
            new StudentDashboardFrame(u).setVisible(true);
        } else {
            new MainDashboardFrame(u).setVisible(true);
        }
        this.dispose();
    }

    private String hashPassword(String plain) {
        try {
            java.security.MessageDigest md = java.security.MessageDigest.getInstance("SHA-256");
            byte[] hash = md.digest(plain.getBytes(java.nio.charset.StandardCharsets.UTF_8));
            StringBuilder hexString = new StringBuilder(2 * hash.length);
            for (byte b : hash) {
                String hex = Integer.toHexString(0xff & b);
                if (hex.length() == 1) hexString.append('0');
                hexString.append(hex);
            }
            return hexString.toString();
        } catch (Exception ex) {
            throw new RuntimeException(ex);
        }
    }
}
"""

with open('C:\\Development\\newsrm\\SmartPark\\src\\gui\\LoginFrame.java', 'w', encoding='utf-8') as f:
    f.write(content)
