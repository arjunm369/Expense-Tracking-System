-- Expense Tracker Database Schema
-- Compatible with Java Spring Boot + MySQL

CREATE DATABASE IF NOT EXISTS expense_tracker_db;
USE expense_tracker_db;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    dob DATE,
    job VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Categories table
CREATE TABLE IF NOT EXISTS categories (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    user_id BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Expenses table
CREATE TABLE IF NOT EXISTS expenses (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    date DATE NOT NULL,
    category VARCHAR(100),
    description VARCHAR(255),
    amount DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (category) REFERENCES categories(name)
);

-- Insert default categories
INSERT IGNORE INTO categories (name, user_id) VALUES
('Food', NULL),
('Transportation', NULL),
('Entertainment', NULL),
('Utilities', NULL),
('Others', NULL);

-- Insert sample users (password: 'password123' hashed with BCrypt)
-- To generate: BCrypt.hashpw("password123", BCrypt.gensalt(10))
INSERT IGNORE INTO users (id, username, password, email, dob, job) VALUES
(1, 'testuser', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iAt6Z5E', 'test@example.com', '1995-05-15', 'Engineer'),
(2, 'johndoe', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iAt6Z5E', 'john@example.com', '1990-08-22', 'Designer');

-- Insert sample expenses for testuser (id=1)
INSERT IGNORE INTO expenses (user_id, date, category, description, amount) VALUES
(1, '2026-04-01', 'Food', 'Lunch at McDonald\'s', 12.50),
(1, '2026-04-02', 'Transportation', 'Uber to work', 15.00),
(1, '2026-04-03', 'Entertainment', 'Netflix subscription', 15.99),
(1, '2026-04-05', 'Food', 'Grocery shopping', 85.30),
(1, '2026-04-07', 'Utilities', 'Electricity bill', 120.00),
(1, '2026-04-10', 'Food', 'Dinner with friends', 45.00),
(1, '2026-04-12', 'Transportation', 'Gas refill', 40.00),
(1, '2026-04-15', 'Entertainment', 'Movie tickets', 25.00),
(1, '2026-04-18', 'Others', 'Phone bill', 55.00),
(1, '2026-04-20', 'Food', 'Coffee and snacks', 18.75),
(1, '2026-04-25', 'Utilities', 'Internet bill', 60.00);

-- Insert sample expenses for johndoe (id=2)
INSERT IGNORE INTO expenses (user_id, date, category, description, amount) VALUES
(2, '2026-04-02', 'Food', 'Breakfast', 8.50),
(2, '2026-04-04', 'Transportation', 'Bus pass', 25.00),
(2, '2026-04-08', 'Entertainment', 'Spotify subscription', 9.99),
(2, '2026-04-11', 'Food', 'Lunch', 15.00),
(2, '2026-04-14', 'Utilities', 'Water bill', 35.00);