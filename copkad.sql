-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Aug 02, 2020 at 05:20 PM
-- Server version: 10.4.13-MariaDB
-- PHP Version: 7.4.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `copkad`
--

-- --------------------------------------------------------

--
-- Table structure for table `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('4f19ee614d13');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `photo_id` varchar(30) NOT NULL,
  `member_id` varchar(20) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `other_names` varchar(50) NOT NULL,
  `gender` varchar(1) NOT NULL,
  `occupation` varchar(50) NOT NULL,
  `contact_phone_1` varchar(14) NOT NULL,
  `contact_phone_2` varchar(14) NOT NULL,
  `dob` datetime NOT NULL,
  `email` varchar(120) NOT NULL,
  `marital_status` varchar(10) NOT NULL,
  `assembly` varchar(30) NOT NULL,
  `ministry` varchar(50) DEFAULT NULL,
  `group` varchar(50) DEFAULT NULL,
  `password_hash` varchar(128) NOT NULL,
  `comm_email` int(11) NOT NULL,
  `comm_sms` int(11) NOT NULL,
  `comm_phone` int(11) NOT NULL,
  `address_line_1` varchar(100) NOT NULL,
  `address_line_2` varchar(100) NOT NULL,
  `digital_address_code` varchar(15) NOT NULL,
  `region` varchar(30) NOT NULL,
  `district` varchar(50) NOT NULL,
  `country` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`,`member_id`),
  ADD UNIQUE KEY `password_hash` (`password_hash`),
  ADD UNIQUE KEY `ix_user_email` (`email`),
  ADD KEY `ix_user_contact_phone_1` (`contact_phone_1`),
  ADD KEY `ix_user_contact_phone_2` (`contact_phone_2`),
  ADD KEY `ix_user_first_name` (`first_name`),
  ADD KEY `ix_user_last_name` (`last_name`),
  ADD KEY `ix_user_member_id` (`member_id`),
  ADD KEY `ix_user_other_names` (`other_names`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
