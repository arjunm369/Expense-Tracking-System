-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 09, 2024 at 07:43 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `expense_tracker_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `name`, `created_at`, `user_id`) VALUES
(1, 'Food', '2024-11-21 14:02:16', NULL),
(2, 'Transportation', '2024-11-21 14:02:16', NULL),
(3, 'Entertainment', '2024-11-21 14:02:16', NULL),
(4, 'Utilities', '2024-11-21 14:02:16', NULL),
(5, 'Others', '2024-11-21 14:02:16', NULL),
(7, 'Others(Insurance)', '2024-11-23 12:50:51', 1),
(8, 'Others(Medicine)', '2024-11-23 12:51:37', 2),
(9, 'Others(Mobile)', '2024-12-06 18:07:21', 1),
(10, 'Others(Flight Ticket)', '2024-12-09 18:27:06', 5);

-- --------------------------------------------------------

--
-- Table structure for table `expenses`
--

CREATE TABLE `expenses` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `category` varchar(100) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `amount` decimal(10,2) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `expenses`
--

INSERT INTO `expenses` (`id`, `user_id`, `date`, `category`, `description`, `amount`, `created_at`) VALUES
(1, 1, '2024-11-23', 'Food', 'hgfhfj', 100.00, '2024-11-23 12:49:59'),
(2, 1, '2024-11-24', 'Food', 'fsfs', 200.00, '2024-11-23 12:50:12'),
(3, 1, '2024-11-25', 'Transportation', 'vsbsbs', 410.00, '2024-11-23 12:50:23'),
(4, 1, '2024-11-26', 'Others(Insurance)', 'sgsg', 1800.00, '2024-11-23 12:50:51'),
(5, 2, '2024-11-23', 'Others(Medicine)', 'gg', 450.00, '2024-11-23 12:51:37'),
(6, 1, '2024-12-03', 'Others(Insurance)', 'gggd', 1400.00, '2024-11-23 12:53:30'),
(7, 1, '2024-12-06', 'Food', 'Food', 200.00, '2024-12-06 17:46:23'),
(8, 1, '2024-12-06', 'Others(Mobile)', 'Recharge', 350.00, '2024-12-06 18:07:21'),
(10, 5, '2024-12-09', 'Food', 'Food', 1200.00, '2024-12-09 18:26:06'),
(11, 5, '2024-12-10', 'Others(Flight Ticket)', 'Ticket', 500.00, '2024-12-09 18:27:06'),
(12, 5, '0202-12-11', 'Transportation', 'Bus ', 500.00, '2024-12-09 18:31:01'),
(13, 5, '2024-12-14', 'Others(Flight Ticket)', 'fsfsf', 15000.00, '2024-12-09 18:38:55');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `dob` date NOT NULL,
  `job` varchar(50) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `email`, `dob`, `job`, `created_at`) VALUES
(1, 'arjun', '12345', 'arjun@gmail.com', '2000-01-20', 'Student', '2024-11-21 14:00:12'),
(2, 'arjun1', 'arjun', 'arjun1@gmail.com', '2000-10-20', 'zvzv', '2024-11-21 15:09:28'),
(4, 'arjunm', 'arjun', 'arjun12@gmail.com', '2000-12-20', 'Student', '2024-12-06 18:11:22'),
(5, 'arjxn', '12345', 'a@gmail.com', '2000-12-20', 'Student', '2024-12-09 18:23:55');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD KEY `fk_user_id` (`user_id`);

--
-- Indexes for table `expenses`
--
ALTER TABLE `expenses`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `category` (`category`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `expenses`
--
ALTER TABLE `expenses`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `categories`
--
ALTER TABLE `categories`
  ADD CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `expenses`
--
ALTER TABLE `expenses`
  ADD CONSTRAINT `expenses_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `expenses_ibfk_2` FOREIGN KEY (`category`) REFERENCES `categories` (`name`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
