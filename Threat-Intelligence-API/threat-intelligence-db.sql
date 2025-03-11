-- Create DB for Threat Intelligence API data:
CREATE DATABASE threat_intelligence;
USE threat_intelligence;

-- Create the Threats table:
CREATE TABLE threats (
	threat_id INT AUTO_INCREMENT PRIMARY KEY,
    threat_name VARCHAR(255) NOT NULL,
    threat_type VARCHAR(100) NOT NULL,
    threat_severity ENUM('Low', 'Medium', 'High', 'Critical') NOT NULL,
    threat_description TEXT NOT NULL,
    date_reported TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );


-- Insert data in order to test your API:
INSERT INTO threats (threat_name, threat_type, threat_severity, threat_description)
	VALUES ('Emotet', 'Malware', 'High', 'A banking trojan that evolves into a botnet.'),
    ('Phishing Email Campaign', 'Phishing', 'Medium', 'A large-scale email phishing attack targeting users.'),
    ('CEO Fraud','Social Engineering', 'High', 'A scam where attackers impersonate company executives to trick employees into transferring money or sensitive data.'),
    ('Ryuk', 'Ransomware', 'Critical', 'A highly destructive ransomware strain used in targeted attacks, often deployed after an initial infection with TrickBot.'),
    ('DDoS Botnet', 'Malware', 'High', 'A network of infected devices used to launch Distributed Denial of Service (DDoS) attacks against websites and services.');

ALTER TABLE threats
MODIFY threat_type VARCHAR(100) DEFAULT 'Unknown';

SELECT * FROM threats;
    