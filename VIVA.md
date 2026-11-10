# SmartPark Campus - VIVA Questions & Answers

## A. Project Basics
**1. What is the title of your project?**
SmartPark Campus – Intelligent College Parking & Access Management System.

**2. What problem does this project solve?**
It solves the problem of campus parking congestion, wasted time searching for slots, and manual security logging by providing a smart, automated reservation system.

**3. What is the 3-tier architecture used in this project?**
It separates the code into Presentation (Swing GUI), Business Logic (Services), and Data Access (DAOs).

**4. Why did you choose Java for this project?**
Java is platform-independent, heavily object-oriented, and excellent for learning robust backend systems, making it ideal for an Advanced Programming Practice (APP) project.

**5. How is the project structured?**
It is divided into packages: `model` (data objects), `dao` (database access), `service` (business logic), `gui` (Swing interfaces), and `threads` (background tasks).

## B. Java Basics
**6. What is the entry point of your Java application?**
The `public static void main(String[] args)` method located in the `Application.java` file.

**7. Why did you use `import` statements?**
To bring classes from different packages (like `java.sql.Connection` or our own `dao.UserDAO`) into the current file.

**8. What is the difference between `==` and `.equals()`?**
`==` compares object references (memory locations), while `.equals()` compares the actual value or content of the objects (like comparing two Strings).

## C. OOP (Object-Oriented Programming)
**9. What are Classes and Objects in your project?**
A Class is a blueprint (e.g., `Vehicle`), and an Object is a specific instance of it (e.g., a specific car with number "AP01-1234").

**10. How did you achieve Encapsulation?**
By making fields in model classes `private` and providing `public` getter and setter methods to access them securely.

## D. Inheritance / Polymorphism / Abstraction
**11. What is inheritance in this project?**
The `User` class is an abstract parent class. `Student`, `Faculty`, `Visitor`, and `Admin` are child classes that `extend User`, inheriting properties like `id` and `username`.

**12. Where is polymorphism used?**
In method overriding. For example, if a method expects a `User` object, we can pass a `Student` or `Admin` object, and they can have their own overridden behaviors.

**13. What is Abstraction in your code?**
We hide complex database SQL logic inside the DAO classes. The GUI only calls `parkingService.reserveSlot(...)` and doesn't know *how* the database handles it.

## E. Interfaces and Packages
**14. Why are interfaces used?**
Interfaces define a contract. For instance, our DAOs implement basic CRUD interfaces, ensuring every DAO has `add()`, `update()`, and `getById()` methods.

**15. Why use packages?**
To organize code logically, prevent naming conflicts, and control access levels (encapsulation).

## F. Exception Handling
**16. Why use exception handling?**
To prevent the program from crashing abruptly when an error occurs, such as a database disconnection or a duplicate booking attempt.

**17. What custom exceptions did you create?**
`DuplicateBookingException` and `SlotUnavailableException` to handle specific business logic errors cleanly.

**18. What is the difference between `throw` and `throws`?**
`throw` is used to trigger an exception inside a method, while `throws` is used in a method signature to declare that the method might throw an exception.

## G. Swing GUI
**19. Why did you use Swing?**
Swing is Java's built-in GUI toolkit. It requires no external web servers and is excellent for building native desktop applications.

**20. What is `CardLayout` used for?**
It allows us to swap multiple panels (like swapping from 'Find Parking' to 'Vehicle Management') in the same window without opening new frames.

**21. How did you draw the interactive map?**
By extending `JPanel` and overriding the `paintComponent(Graphics g)` method to draw shapes based on DB X/Y coordinates.

## H. JDBC and MySQL
**22. What is JDBC?**
Java Database Connectivity. It’s an API that allows Java programs to connect to, and execute queries against, a database.

**23. Why use DAO (Data Access Object)?**
To separate database queries (SQL) from the business logic. If we change to a different database later, we only change the DAO.

**24. How did you prevent SQL Injection?**
By using `PreparedStatement` instead of regular `Statement`, which safely escapes user inputs.

## I. Multithreading
**25. Why use multithreading in this project?**
To perform background tasks (like checking for expired reservations) without freezing the user interface (the Swing Event Dispatch Thread).

**26. What is `ReservationExpiryThread`?**
A thread that sleeps, wakes up periodically, checks the database for reservations past their end time, and automatically marks them `EXPIRED`.

**27. What does the `synchronized` keyword do?**
It prevents multiple threads from executing a critical block of code at the same time, preventing race conditions.

## J. Database and Transactions
**28. Why use `TRANSACTION_SERIALIZABLE`?**
It is the highest isolation level in MySQL. It ensures that transactions execute completely sequentially, completely preventing double-booking anomalies.

**29. What is `SELECT ... FOR UPDATE`?**
It locks the specific database row (the parking slot) during a query so no one else can read or modify it until the transaction commits.

**30. How is double booking prevented?**
By combining `synchronized` Java methods with MySQL `TRANSACTION_SERIALIZABLE` and row locks.

**31. What happens if a transaction fails halfway?**
We call `conn.rollback()` in the `catch` block to undo any partial changes, maintaining database integrity.

## K. QR Code / ZXing
**32. How does the QR code work?**
We use the external ZXing (Zebra Crossing) library. The `QRCodeService` formats data and ZXing's `MatrixToImageWriter` generates a real `BufferedImage`.

**33. What data is stored in the QR Code?**
A secure string payload containing the Booking ID, Vehicle Number, and Slot ID.

## L. Smart Recommendation
**34. How does the recommendation system work?**
It fetches all available slots, calculates the Euclidean distance to the destination building, and applies a scoring formula.

**35. What is the scoring formula?**
Score = 1000 - (Distance * 10). We then add +500 if the slot is an EV slot and the vehicle is an EV, and +100 if the user is Faculty. The slot with the highest score wins.

## M. EV Parking
**36. How are EV slots identified?**
In the `parking_slots` table, they have a boolean `is_ev` flag.

**37. How is EV functionality implemented?**
It is software-based. The algorithm highly prioritizes assigning EV slots to EV vehicles. Non-EV vehicles are directed away from EV slots.

## N. Security Entry/Exit
**38. How does security verify a vehicle?**
Security scans the QR (or enters the ID). The system checks the `reservations` table to ensure it is `ACTIVE` and the vehicle number matches.

**39. How are entry and exit stored?**
When verified, an `INSERT` statement logs the event into the `parking_entries_exits` table with a timestamp, ensuring a permanent audit trail.

**40. What happens to the slot status on entry?**
The slot's status is updated from `RESERVED` to `OCCUPIED`.

## O. Visitor Parking
**41. How does a visitor park?**
They click "Register as Visitor" on the login screen, which creates a specific `VISITOR` role account, allowing them to use the standard booking flow.

## P. Admin Analytics
**42. How does Admin Analytics get live data?**
It executes `COUNT(*)` SQL queries against the `parking_slots` and `parking_entries_exits` tables.

**43. Is the data hardcoded?**
No, clicking the "Refresh Stats" button dynamically runs the queries and updates the Swing UI.

## Q. General / Project Specific
**44. What happens when a reservation expires?**
The background thread detects it, changes reservation status to `EXPIRED`, and resets the slot status to `AVAILABLE`.

**45. What are the limitations of the current system?**
It currently books automatically for a 2-hour window from "Now", rather than using a manual Date/Time picker widget, to keep the UI simple.

**46. What would you improve in the future?**
Add hardware integration (like Raspberry Pi for boom barriers) and email/SMS notifications.

**47. Why are passwords hashed?**
To protect user security. Even if the database is exposed, passwords cannot be easily read. We used a simple SHA-256 hash for this demo.

**48. Why not use Python or Web Technologies?**
Java was specifically chosen to demonstrate Core Object-Oriented Programming, JDBC, and multithreading concepts strictly as per APP college requirements.

**49. Did you use an ORM like Hibernate?**
No, we used raw JDBC to thoroughly demonstrate an understanding of SQL queries and manual `ResultSet` mapping.

**50. What was the most challenging part?**
Implementing the strict double-booking prevention using SQL transaction locks alongside Java threading, ensuring no two students can steal the same slot simultaneously.
