-- Database schema for Attendance System
-- Run this to create the database manually if needed

CREATE DATABASE IF NOT EXISTS attendance_system;
USE attendance_system;

-- Admin users table
CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Persons (students) table
CREATE TABLE IF NOT EXISTS persons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE,
    student_id VARCHAR(50) UNIQUE,
    photo_path VARCHAR(255),
    face_encoding LONGBLOB,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_student_id (student_id),
    INDEX idx_email (email)
);

-- Attendance records table
CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    person_id INT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'present',
    confidence FLOAT,
    FOREIGN KEY (person_id) REFERENCES persons(id) ON DELETE CASCADE,
    INDEX idx_date (date),
    INDEX idx_person_date (person_id, date),
    UNIQUE KEY unique_person_date (person_id, date)
);

-- Insert default admin (password: admin123)
-- Password hash generated with werkzeug.security.generate_password_hash
INSERT INTO admins (username, password_hash) VALUES 
('admin', 'scrypt:32768:8:1$PLACEHOLDER$HASH');
