<p align="center">
  <img src="src/assets/smartpark_banner.jpg" alt="SmartPark Campus Logo" width="800"/>
</p>

# SmartPark Campus – Intelligent College Parking & Access Management System

## Project Overview
SmartPark Campus is a desktop-based intelligent parking and access management system built for a college campus environment. It is an Advanced Programming Practice (APP) college project designed to reduce parking congestion, streamline vehicle entry/exit, and provide smart slot recommendations based on destination proximity and vehicle type (including EV).

## Problem Statement
Traditional college campus parking systems rely on manual logbooks or first-come-first-serve hunting. This leads to wasted time searching for parking, confusion over restricted zones, inability to track real-time occupancy, and a lack of support for emerging needs like Electric Vehicle (EV) charging prioritization. 

## Objectives
- Automate the reservation and tracking of campus parking slots.
- Prevent double-booking using robust database transaction locks.
- Recommend the best parking slot using a spatial/contextual algorithm.
- Provide secure entry/exit logging with verifiable QR Parking Passes.
- Provide live analytics for campus administration.

## Real-World Use Case
Students, Faculty, and Visitors use the Swing GUI application to register their vehicles and book parking before arriving on campus. Upon arrival, Security verifies their real, auto-generated QR pass against the live database, allowing entry and automatically updating the campus-wide occupancy dashboard. 

## Key Features
- **Smart Parking Recommendation Algorithm**: Calculates a score based on distance to the user's destination building, Faculty role priority, and EV compatibility.
- **Double-Booking Prevention**: Uses `TRANSACTION_SERIALIZABLE` and `SELECT ... FOR UPDATE` to strictly enforce ACID database properties against simultaneous reservations.
- **Real QR Parking Pass**: Uses ZXing to generate an actual `.png` QR code containing the booking payload.
- **Security Verification Workflow**: Security personnel verify the pass, logging exact entry/exit times to a dedicated `parking_entries_exits` audit table.
- **Admin Analytics Dashboard**: Real-time visualization of Total, Available, Occupied, and Reserved slots, plus live daily entry/exit counts.
- **Automated Expiry**: A background multithreaded daemon automatically releases reservations if the user does not arrive in time.
- **EV Parking Support (Software Level)**: Specific zones mapped for EVs, prioritizing them for EV vehicles.

## Technologies Used
- **Programming Language**: Java (JDK 8+)
- **GUI Framework**: Java Swing & AWT (Custom Graphics & CardLayout)
- **Database**: MySQL Server
- **Database Connectivity**: JDBC (Java Database Connectivity)
- **External Libraries**: ZXing (Zebra Crossing) for QR generation (`zxing-core`, `zxing-javase`), MySQL Connector (`mysql-connector-java.jar`)

## APP Concepts Demonstrated
This project is built from scratch utilizing the following Core Java concepts:
- **Classes and Objects**: Used extensively for models (`Vehicle`, `ParkingSlot`, `Reservation`).
- **Inheritance**: `User` acts as an abstract base class inherited by `Student`, `Faculty`, `Visitor`, `SecurityStaff`, and `Admin`.
- **Polymorphism**: Overridden `toString()` and GUI rendering techniques tailored for different user subclasses.
- **Abstraction**: Complex logic like `reserveSlot` hides the heavy SQL transaction logic behind simple method calls.
- **Encapsulation**: Strict use of `private` fields with getters/setters in Model classes.
- **Interfaces**: Service interfaces implemented by concrete classes (e.g., DAOs).
- **Packages**: Code organized into `model`, `dao`, `service`, `gui`, `threads`, and `database`.
- **Exception Handling**: Custom exceptions like `DuplicateBookingException` and `SlotUnavailableException`.
- **Multithreading**: `ReservationExpiryThread` running alongside the Swing Event Dispatch Thread.
- **3-Tier Architecture**: Clean separation of GUI (Presentation) ↔ Service (Business Logic) ↔ DAO (Data Access).

## Database Architecture
The MySQL database enforces foreign key constraints and cascades. Key tables include:
1. `users`: Stores all roles with SHA-256 hashed passwords.
2. `vehicles`: Tracks vehicle types (2-wheeler, 4-wheeler, EV).
3. `buildings`: Stores X/Y coordinates for recommendation logic.
4. `parking_zones`: Logical grouping of parking slots.
5. `parking_slots`: Individual slots with X/Y map coordinates and status (AVAILABLE, OCCUPIED, etc.).
6. `reservations`: Tracks active and historical bookings.
7. `parking_entries_exits`: Dedicated audit trail for physical gate entry and exit.

## Installation & Setup Requirements

1. **Install Java & MySQL**: Ensure JDK 8+ and MySQL Server are installed.
2. **Database Setup**: 
   - Open MySQL Workbench or CLI.
   - Run the provided `database/schema.sql` script to create the schema and insert mock data.
3. **Required JAR Files**: 
   - Create a folder named `lib/` in the project root.
   - Place the following files inside `lib/`:
     - `mysql-connector-java.jar`
     - `zxing-core-3.5.1.jar` (or similar)
     - `zxing-javase-3.5.1.jar` (or similar)
4. **Compile the Project**:
   - Open Command Prompt in the project folder.
   - Run `.\compile.bat`.
5. **Run the Application**:
   - Run `.\run.bat`.

## Workflows & Test Credentials

### Student / Faculty Workflow
- **Login**: `stud1` / `password` (Student) OR `fac1` / `password` (Faculty)
- **Steps**: Navigate to 'My Vehicles' -> Register Vehicle -> Navigate to 'Find Parking' -> Select Destination & Vehicle -> Click 'Find Smart Parking' -> Review Recommendation -> Book -> View QR Code.

### Visitor Workflow
- **Steps**: On the Login screen, click **Register as Visitor**. Enter desired username and password. Log in and book a slot as normal.

### Security Workflow
- **Login**: `sec1` / `password`
- **Steps**: Navigate to the Security Panel. Type in the Booking ID presented on the QR Pass. Click "Verify Entry". The system checks the database, records entry, and marks the slot as OCCUPIED. 

### Admin Workflow
- **Login**: `admin` / `admin`
- **Steps**: Navigate to Analytics Dashboard. Click "Refresh Stats" to view live metrics pulled from `parking_slots` and `parking_entries_exits`.

## Known Limitations
- The current booking system defaults to reserving the slot from "Now to Now + 2 hours". There is no manual Date/Time picker UI to keep the Swing framework simple and native.
- EV Support is strictly software-based; there is no physical IoT hardware or live battery percentage monitoring.
- Passwords use a basic SHA-256 string hash for demo purposes; production systems would require salted bcrypt/Argon2.

## Future Enhancements
- Integration with an actual Date/Time picker library (e.g. LGoodDatePicker).
- Email/SMS notification dispatch for booking confirmations.
- Real hardware integration via Raspberry Pi for boom-barrier automation based on QR scans.
