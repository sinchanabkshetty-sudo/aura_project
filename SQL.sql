CREATE DATABASE aura_db;
USE aura_db;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(80),
    email VARCHAR(191) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE command_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    user_command TEXT,
    aura_response TEXT,
    input_mode VARCHAR(10) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_history_user
      FOREIGN KEY (user_id)
      REFERENCES users(user_id)
      ON DELETE SET NULL
);

CREATE INDEX idx_history_user_time 
    ON command_history(user_id, timestamp);
