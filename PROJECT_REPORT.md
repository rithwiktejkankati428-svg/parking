# PROJECT REPORT
**Project Title:** SmartPark Campus – Intelligent College Parking & Access Management System

---

## 1. Title Page
**Project Name**: SmartPark Campus  
**Course**: Advanced Programming Practice (APP)  
**Technology Stack**: Java Swing, JDBC, MySQL, ZXing  

## 2. Abstract
SmartPark Campus is a desktop-based intelligent parking management system designed to optimize parking slot allocation in college environments. Utilizing Core Java, JDBC, and multithreading, it features a smart recommendation algorithm, real-time QR pass generation, stringent double-booking prevention, and role-based access for Students, Faculty, Visitors, Security, and Admins.

## 3. Introduction
Campus parking often suffers from congestion and inefficiency. This project digitizes the reservation and validation process. It provides an automated, scalable software solution integrating user registration, intelligent spatial recommendation, and strict database auditing.

## 4. Problem Statement
Traditional parking methods rely on manual logging and visual search, leading to wasted time, restricted zone violations, and an inability to prioritize modern needs like Electric Vehicle (EV) charging spots.

## 5. Objectives
1. Automate slot reservations using a native GUI.
2. Prevent double-booking using advanced SQL transactions.
3. Generate secure QR passes for gate validation.
4. Provide a background thread monitor to clear expired reservations.
5. Deliver a live analytics dashboard for administration.

## 6. Existing System
The existing system is manual. Guards use paper logbooks. Drivers loop around campus searching for slots. There is no pre-booking, no EV priority, and no historical data analysis.

## 7. Proposed System
A 3-tier Java application connecting to a MySQL backend. Users pre-book slots. An algorithm ensures they park closest to their destination. Security verifies entry via QR code, creating a seamless, logged, and secure environment.

## 8. Scope
The scope encompasses software-based management of users, vehicles, and slots. Hardware integration (boom barriers, physical battery sensors) is outside the scope.

## 9. Requirements
- **Hardware**: Standard PC (Windows/Mac/Linux).
- **Software**: JDK 8+, MySQL Server, ZXing JARs.

## 10. Technology Stack
- **Frontend**: Java Swing & AWT
- **Backend**: Core Java, Multithreading
- **Database**: MySQL 8.0, JDBC API
- **QR Generation**: Zebra Crossing (ZXing)

## 11. System Architecture
**3-Tier Architecture:**
- **Presentation Layer**: Swing Panels (`LoginFrame`, `MainDashboardFrame`).
- **Business Layer**: Service Classes (`ParkingService`, `RecommendationService`).
- **Data Access Layer**: DAOs (`UserDAO`, `SlotDAO`) communicating with MySQL.

## 12. Module Description
- **Authentication**: Role-based login and Visitor registration.
- **Vehicle Management**: Registering 2-Wheelers, 4-Wheelers, and EVs.
- **Reservation**: Smart recommendation and secure booking.
- **Security Checkpost**: Validating Booking IDs and updating entry/exit logs.
- **Admin Dashboard**: Live statistical overview.

## 13. OOP Implementation
- **Inheritance**: `Student`, `Faculty` extend abstract `User`.
- **Encapsulation**: Private fields in models with getters/setters.
- **Polymorphism**: Overridden behaviors based on user role.

## 14. Interface Implementation
Data Access Objects implement shared design patterns for CRUD operations, ensuring loose coupling between the Service layer and the Database.

## 15. Exception Handling
Custom exceptions (`DuplicateBookingException`, `SlotUnavailableException`) are thrown by the Service layer and caught by the GUI to display user-friendly `JOptionPane` alerts.

## 16. Multithreading
`ReservationExpiryThread` extends `Thread`. It runs an infinite loop with `Thread.sleep()`, querying the database periodically to expire unfulfilled reservations without blocking the Swing EDT.

## 17. JDBC Implementation
Extensive use of `PreparedStatement` to prevent SQL Injection. The `DatabaseConnection` class uses the Singleton pattern to provide a single `Connection` instance.

## 18. Database Design
Relational design with 3NF. Employs Foreign Keys with `ON DELETE CASCADE` to maintain referential integrity.

## 19. ER Diagram description
- `Users` (1) to (N) `Vehicles`
- `Users` (1) to (N) `Reservations`
- `Parking_Slots` (1) to (1) `Reservations` (Active)
- `Reservations` (1) to (N) `Parking_Entries_Exits`

## 20. UML Diagram descriptions
- **Class Diagram**: Shows `User` hierarchy, DAOs, and Services.
- **Sequence Diagram**: User clicks Book -> GUI calls `ParkingService` -> `ParkingService` locks row -> `ParkingService` inserts Reservation -> Returns Success -> GUI calls `QRCodeService`.

## 21. Smart Parking Recommendation
Calculates Euclidean distance $D = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$ between the slot and the destination building, converting it to a prioritized score.

## 22. QR Parking Pass
Utilizes ZXing's `MatrixToImageWriter`. The generated `BufferedImage` contains the Booking ID and Vehicle ID, which is rendered in a Swing `JLabel`.

## 23. Security Entry/Exit
Security verifies the Booking ID. A transaction updates `reservations.status`, `parking_slots.status`, and inserts an `ENTRY` log into the `parking_entries_exits` table.

## 24. EV Parking
Software-based tagging of EV slots. The recommendation algorithm grants a +500 point bonus to matching EV vehicles with EV slots.

## 25. Visitor Parking
A specific registration flow bypasses the college ID requirement, storing the user as role `VISITOR`, allowing them to utilize the same robust booking system.

## 26. Admin Analytics
The `AdminPanel` executes aggregate functions (`COUNT(*)`) joined with `DATE()` filters to display live Total, Available, and Today's Entry statistics.

## 27. Double-booking Prevention
The core of the system's integrity. Uses `Connection.setTransactionIsolation(Connection.TRANSACTION_SERIALIZABLE)` and `SELECT ... FOR UPDATE` to physically lock the slot row during the booking microsecond.

## 28. Testing
Unit testing of JDBC transactions and manual integration testing of the Swing GUI flow. 

## 29. Test Cases
1. **Invalid Login**: System denies access.
2. **Double Booking**: Second thread rejected with exception.
3. **QR Generation**: Produces readable PNG matrix.
4. **Invalid Security ID**: Denies entry update.

## 30. Results
The system successfully compiles and runs natively, handling multiple concurrent database requests accurately.

## 31. Screenshots section placeholders
*[Insert Screenshot of Login Screen]*
*[Insert Screenshot of Live Interactive Map]*
*[Insert Screenshot of Generated QR Pass]*
*[Insert Screenshot of Admin Analytics]*

## 32. Advantages
- Native, fast desktop performance.
- Absolute data consistency.
- Highly scalable database schema.
- Automatic expiration clears deadlocks.

## 33. Limitations
- Booking strictly defaults to a 2-hour window (Now to Now + 2).
- EV charging status is software logic, lacking hardware polling.
- Requires local JVM and MySQL Server setup.

## 34. Future Enhancements
- Integration of a manual Date/Time picker calendar.
- Integration of hardware IoT sensors for boom barriers.
- Cloud hosting of the MySQL database.

## 35. Conclusion
SmartPark Campus successfully demonstrates the power of Core Java, Swing, and robust SQL transaction management. It provides a complete, intelligent solution for campus parking.

## 36. References
1. Oracle Java Documentation (Swing, JDBC)
2. MySQL 8.0 Reference Manual (Transactions, Locks)
3. ZXing Project Documentation
