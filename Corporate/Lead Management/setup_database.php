<?php
// setup_database.php - Run this once to create database
$host = 'localhost';
$username = 'root';
$password = '';

// Create connection
$conn = new mysqli($host, $username, $password);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Create database
$sql = "CREATE DATABASE IF NOT EXISTS lead_management";
if ($conn->query($sql) === TRUE) {
    echo "Database created successfully<br>";
} else {
    echo "Error creating database: " . $conn->error;
}

// Select database
$conn->select_db("lead_management");

// Create leads table
$sql = "CREATE TABLE IF NOT EXISTS leads (
    id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    company VARCHAR(100),
    source VARCHAR(50) DEFAULT 'Website',
    status ENUM('New', 'Contacted', 'Qualified', 'Lost') DEFAULT 'New',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)";

if ($conn->query($sql) === TRUE) {
    echo "Table leads created successfully<br>";
    echo "Setup complete! You can now delete this file.";
} else {
    echo "Error creating table: " . $conn->error;
}

$conn->close();
?>
