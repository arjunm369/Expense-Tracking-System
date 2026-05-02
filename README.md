# Expense Tracking System

A simple web-based expense tracker built with Java Spring Boot and MySQL. Users can register, log in, add expenses, and filter them by category or date range.

## Features
- User registration and login with password hashing (BCrypt)
- Add, view, and filter expenses
- Filter by category and date range
- Calculate total expenses for a given period

## Tech Stack
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Java, Spring Boot
- **Database:** MySQL
- **Connector:** JDBC (Spring Data JPA)

## How to Run

### Prerequisites
- Java 17+
- Maven
- MySQL Server

### Steps
1. **Create the database:**
   ```bash
   mysql -u root -p < expense_tracker_db.sql
   ```

2. **Configure database credentials:**
   Update `src/main/resources/application.properties` with your MySQL username and password.

3. **Build and run the backend:**
   ```bash
   mvn spring-boot:run
   ```
   The backend will start on `http://localhost:8080`.

4. **Open the frontend:**
   - Navigate to `src/main/resources/static/index.html`
   - Or serve the static folder with any HTTP server

5. **Use the app:**
   - Register a new account
   - Log in
   - Add and view expenses

## Project Structure
```
Expense-Tracking-System/
├── src/main/java/com/expensetracker/
│   ├── ExpenseTrackerApplication.java
│   ├── controller/   # REST API endpoints
│   ├── model/        # JPA entities
│   ├── repository/   # Data access layer
│   └── service/      # Business logic
├── src/main/resources/
│   ├── application.properties  # DB config
│   └── static/               # Frontend
│       ├── index.html         # Login page
│       ├── register.html      # Registration page
│       ├── dashboard.html     # Main app
│       ├── css/style.css
│       └── js/
│           ├── auth.js
│           └── dashboard.js
├── expense_tracker_db.sql
├── pom.xml
└── README.md
```

## Limitations & Future Improvements
- No session management (stateless, userId passed in requests)
- No expense edit/delete functionality
- Basic UI without advanced styling
- Could add password reset, charts, and mobile responsiveness

## Resume Bullet Points
- Built a full-stack expense tracking system using Java Spring Boot, MySQL, and HTML/CSS/JS, implementing secure user authentication with BCrypt password hashing.
- Designed a normalized MySQL database schema and integrated it with Spring Data JPA for efficient expense querying and filtering.
- Developed RESTful APIs to handle expense CRUD operations and aggregation, serving a clean web UI with category and date-based filtering.