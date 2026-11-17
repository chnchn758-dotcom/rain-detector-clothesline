CREATE DATABASE IF NOT EXISTS rain_dashboard;
USE rain_dashboard;

CREATE TABLE IF NOT EXISTS rain_events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    status ENUM('rain', 'dry') NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_created_at (created_at)
);