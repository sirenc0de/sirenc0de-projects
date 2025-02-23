-- Creative scenario of use: Cybersecurity Incident Response DB for a Security Operations Center (SOC) that 
-- needs to track cybersecurity incidents. Analysts handle incidents based on type and severity. When an incident
-- is resolved, its status is updated, and data analysis helps prioritise risks. The system must support incident 
-- escalation, report generation, and track analyst performance.  

-- Create the DB and select it:
CREATE DATABASE cybersecurity_db;
USE cybersecurity_db;

-- Create table 1: Analysts (no need to add DROP TABLE IF EXISTS statement as it's the first creation of this table).
	CREATE TABLE Analysts (
		analyst_id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL, -- Constraint 1: NOT NULL, ensures this column cannot have NULL values
        last_name VARCHAR(50) NOT NULL, -- Constraint 2: NOT NULL
        email VARCHAR(100) NOT NULL UNIQUE, -- Constraint 3: UNIQUE to avoid duplicate emails
        start_date DATE NOT NULL
	);
-- Adding a trigger to enforce the date constraint (Constraint 4, table 1), MySQL Workbench, does not support the CURDATE() function, as it doesn't enforce the CHECK constraint in older versions and limited in newer versions. 
	DELIMITER //
    CREATE TRIGGER before_insert_analyst -- A TRIGGER prevents invalid entries
    BEFORE INSERT ON Analysts
    FOR EACH ROW
    BEGIN
		IF NEW.start_date > CURDATE() THEN
			SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Hire start date cannot be in the future';
		END IF;
	END //
    
    DELIMITER ;

-- Create table 2: Incident Types with constraints:        
	CREATE TABLE IncidentTypes (
		type_id INT AUTO_INCREMENT PRIMARY KEY,
        type_name VARCHAR(50) NOT NULL,
        incident_description TEXT CHECK (CHAR_LENGTH(incident_description) >= 10) -- Constraint 2: CHECK ensures the incident description has at least 10 characters
	);

-- Create table 3: Incidents with constraints:
	CREATE TABLE Incidents (
		incident_id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(100) NOT NULL, -- Constraint 1: NOT NULL
        incident_description TEXT,
        reported_date DATE NOT NULL, 
        resolved_date DATE DEFAULT NULL,
        incident_status VARCHAR(20) NOT NULL DEFAULT 'Open', -- Constraint 2: default value constraint, to automatically set status value to 'Open' if not specified 
        severity INT NOT NULL CHECK (severity BETWEEN 1 AND 5), -- Constraint 3: to reflect that the Incident severity level must be 1-5
        analyst_id INT,
        type_id INT,
	FOREIGN KEY (analyst_id) REFERENCES Analysts(analyst_id),
	FOREIGN KEY (type_id) REFERENCES IncidentTypes(type_id)
	);

DELIMITER //
    CREATE TRIGGER before_insert_incident -- Constraint 4: CHECK TRIGGER ensures reported date isn't in the future
    BEFORE INSERT ON Incidents
    FOR EACH ROW
    BEGIN
		IF NEW.reported_date > CURDATE() THEN
			SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Reported date cannot be in the future';
		END IF;
	END //
    
    DELIMITER ; -- Reset delimiter back to default

ALTER TABLE Incidents
CHANGE COLUMN incident_description case_description TEXT NOT NULL;
    
-- Populate the tables with at least 8 rows of mock data:
-- Insert data into Table 1 - Analysts
INSERT INTO Analysts (first_name, last_name, email, start_date)
	VALUES ('Anner', 'Copely', 'anner.cope@live.com', '2023-05-15'),
    ('Krishma', 'Sonu', 'krishma.sonu@gmail.com', '2018-05-13'),
    ('Kerry', 'Thompson', 'kthompson@hotmail.co.uk', '2005-02-02'),
    ('Nehemiah', 'Guapo', 'nehemiah.g@live.com', '2021-11-08'),
    ('Richard', 'Collins', 'richard.collins@gmail.com', '2023-01-13'),
    ('Eva', 'Scott', 'eva.scott4eva@live.co.uk', '2001-04-26'),
    ('Kwame', 'Shields', 'shieldsdidit@hotmail.com', '2019-10-05'),
    ('Derrick', 'Charms', 'charms.derr@cybers.com', '2024-07-01');

-- Insert data into Table 2 - IncidentTypes
INSERT INTO IncidentTypes (type_name, incident_description)
	VALUES ('Phishing', 'Attempts to trick users into providing sensitive information.'),
    ('Malware', 'Malicious software infections that compromise system integrity.'),
    ('DDoS', 'Distributed Denial of Service attacks to overwhelm systems.'),
    ('Unauthorised Access', 'Access to systems or data without permission.'),
    ('Data Breach', 'Unauthorised access and exposure of confidential data.'),
    ('Insider Threat', 'Malicious actions by trusted individuals within the organisation.'),
    ('Ransomware', 'Malware that encrypts data and demands a ransom for decrpytion.'),
    ('Zero-Day Exploit', 'Exploiting previously unknown vulnerabilities.');
    
-- Insert data into Table 3 - Incidents
INSERT INTO Incidents (title, case_description, reported_date, resolved_date, incident_status, severity, analyst_id, type_id)
	VALUES ('Phishing Email Reported', 'Employee received suspicious email asking for credentials.', '2023-04-01', '2023-04-02', 'Resolved', 3, 1, 1),
    ('Malware Detected', 'Malware detected on workstation during routin scan.', '2023-04-05', NULL, 'Open', 4, 2, 2),
    ('DDoS Attack', 'Website experienced high traffic suspected as DDoS attack.', '2023-04-07', '2023-04-08', 'Resolved', 5, 3, 3),
    ('Unauthorised Login Attempt', 'Multiple failed login attempts detected from foreign IP.', '2023-04-10', NULL, 'Open', 2, 4, 4),
    ('Data Breach Suspicion', 'Potential data breach detected with unusual data transfers.', '2024-12-12', NULL, 'Investigating', 5, 5, 5),
    ('Insider Threat Alert', 'Employee accessing restricted files without authorisation.', '2024-04-15', '2024-04-16', 'Resolved', 4, 6, 6),
    ('Ransomware Attack', 'Critical systems encrpyted by ransomware.', '2024-10-18', NULL, 'Open', 5, 7, 7),
    ('Zero-Day Exploit Found', 'Exploit discovered in third-party software, patch pending.', '2024-04-20', NULL, 'Open', 3, 8, 8);

-- Add column for analyst expertise. 
SET SQL_SAFE_UPDATES = 1;
ALTER TABLE Analysts 
ADD COLUMN specialisation VARCHAR(50) NOT NULL;

-- Add more Analyst to distribute reports. 
INSERT INTO Analysts (first_name, last_name, email, start_date, specialisation)
VALUES ('Thor', 'Thunder', 't.thunder@soc.com', '2024-01-02', 'Network Security'),
('Storm', 'Weathers', 'StormWeathers@soc.com', '2024-01-21', 'Malware Analysis'),
('Clark', 'Kent', 'Kent.Clarke@soc.com', '2025-02-14', 'Incident Response'),
('Zari', 'Hussein', 'Z.Hassein@soc.com', '2024-10-16', 'Cloud Security');

-- Update Analysts table with analysts expertise. 
UPDATE Analysts
SET specialisation = 'Network Security'
WHERE first_name = 'Anner' AND last_name = 'Copely';

UPDATE Analysts
SET specialisation = 'Malware Analysis'
WHERE first_name = 'Krishma' AND last_name = 'Sonu';

UPDATE Analysts
SET specialisation = 'Incident Response'
WHERE first_name = 'Kerry' AND last_name = 'Thompson';

UPDATE Analysts
SET specialisation = 'Cloud Security'
WHERE first_name = 'Nehemiah' AND last_name = 'Guapo';

UPDATE Analysts
SET specialisation = 'Malware Analysis'
WHERE first_name = 'Richard' AND last_name = 'Collins';

UPDATE Analysts
SET specialisation = 'Network Security'
WHERE first_name = 'Eva' AND last_name = 'Scott';

UPDATE Analysts
SET specialisation = 'Cloud Security'
WHERE first_name = 'Kwame' AND last_name = 'Shields';

UPDATE Analysts
SET specialisation = 'Incident Response'
WHERE first_name = 'Derrick' AND last_name = 'Charms';

SET SQL_SAFE_UPDATES = 0;

-- Data Retrieval Queries, 
-- 1. Show all Open or Investigating Incidents to help the SOC teams quickly identify ongoing threats. 
SELECT *
FROM Incidents
WHERE incident_status IN ('Open', 'Investigating')
ORDER BY reported_date DESC;

-- 2. Count the Number of Unresolved Incidents per Analyst to help monitor workload distribution amongst analysts. 
SELECT a.analyst_id, a.first_name, a.last_name, 
	COUNT(i.incident_id) AS unresolved_cases
FROM Analysts a
	LEFT JOIN Incidents i ON a.analyst_id = i.analyst_id
    WHERE i.incident_status IN ('Open', 'Investigating')
    GROUP BY a.analyst_id
    ORDER BY unresolved_cases DESC;

-- 3. Show the Most Recent Incident for each analyst to track the latest response effort of each analyst. 
SELECT i.incident_id, i.title, i.reported_date, a.first_name, a.last_name
FROM Incidents i
	JOIN Analysts a ON i.analyst_id = a.analyst_id
    WHERE i.reported_date = (
		SELECT MAX(reported_date)
        FROM Incidents
        WHERE analyst_id = i.analyst_id
);

-- 4. Retrieve all Incidents with High Severity (Priority Cases) to help prioritise and escalate critical threats.
SELECT *
FROM Incidents
WHERE severity >= 4
ORDER BY severity DESC, reported_date DESC;
    
-- 5. Show how many Incidents each Incident Type has to help analyse which threats occur most often. 
SELECT it.type_name, COUNT(i.incident_id) AS total_cases
FROM IncidentTypes it
	JOIN Incidents i ON it.type_id = i.type_id
    GROUP BY it.type_name
    ORDER BY total_cases DESC;

-- 6. Retrieve all Resolved Incidents and their Resolved Time to help assess how long incidents take to resolve. 
SELECT incident_id, title, incident_status, DATEDIFF(IFNULL(resolved_date, CURDATE()), reported_date) 
	AS days_to_resolve
FROM Incidents
WHERE incident_status = 'Resolved'
	 AND (resolved_date IS NOT NULL OR resolved_date IS NULL)
ORDER BY days_to_resolve DESC
LIMIT 5;
-- Unexpected data for Incident 2 in Days to Resolve column. Check resolved date for Incident 2.
SELECT incident_id, reported_date, resolved_date
FROM Incidents
WHERE incident_id = 2;
-- Update Incidents table to include previously missing resolved date value for Incident 2.
UPDATE Incidents
SET resolved_date = '2023-04-12'
WHERE incident_id = 2;
-- Run retrieval query again.

SELECT incident_id, title, incident_status, DATEDIFF(COALESCE(resolved_date, CURDATE()), reported_date) 
	AS days_to_resolve
FROM Incidents
WHERE incident_status = 'Resolved'
	 AND (resolved_date IS NOT NULL OR resolved_date IS NULL)
ORDER BY days_to_resolve DESC
LIMIT 5;

-- 7. Retrieve incident_id, title and a formatted reported date using the DATE_FORMAT (built-in function) and aggregated sum of reports
SELECT
	incident_id, title, DATE_FORMAT(reported_date, '%M %d, %Y') AS formatted_reported_date,
    COUNT(incident_id) AS total_reports
FROM Incidents
	GROUP BY incident_id
	ORDER BY formatted_reported_date DESC;

-- Show Analysts who have no assigned Incidents yet to help identify analysts who are not used effectively. 
SELECT a.analyst_id, a.first_name, a.last_name
FROM Analysts a
	LEFT JOIN Incidents i ON a.analyst_id = i.analyst_id
    WHERE i.incident_id IS NULL;

-- Queries for Data Manipulation 
-- Assign an Analyst to an Incident to simulate an analyst being assigned a case.
UPDATE Incidents
SET analyst_id = 3
WHERE incident_id = 5;

-- Close an Incident to simulate an incident being resolved. 
UPDATE Incidents
SET incident_status = 'Resolved'
WHERE incident_id = 2;

-- Delete an Incident Record to simulate removing incorrect or duplicate reports. 
DELETE FROM Incidents 
	WHERE incident_id = 7;

INSERT INTO Incidents (incident_id, title, case_description, reported_date, resolved_date, incident_status, severity, analyst_id, type_id)
VALUES (7, 'Ransomware Attack', 'Critical systems encrpyted by ransomware.', '2024-10-18', NULL, 'Open', 5, 7, 7);

-- Additional uses of in-built functions:


-- Create a Stored Procedure that checks if an analyst's start date is older than a year from the current date. If it is, the procedure
-- will alert with a message.

DELIMITER //

CREATE PROCEDURE Check_Analyst_Experience()
BEGIN
	DECLARE done INT DEFAULT 0;
    DECLARE analyst_name VARCHAR(100);
    DECLARE analyst_start_date DATE;
    
    DECLARE analyst_cursor CURSOR FOR
    SELECT CONCAT(first_name, ' ', last_name), start_date
    FROM Analysts;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    
    OPEN analyst_cursor;
    
    read_loop: LOOP
		FETCH analyst_cursor INTO analyst_name, analyst_start_date;
        
        IF done THEN
			LEAVE read_loop;
		END IF;
        
        IF DATEDIFF(CURDATE(), analyst_start_date) > 365 THEN
			SELECT CONCAT(analyst_name, ' ', ' has been with the CS SOC for over a year!');
		END IF;
	END LOOP;
    
    CLOSE analyst_cursor;
END //

DELIMITER ;

-- Call the Stored Procedure:
CALL Check_Analyst_Experience;

SELECT 'Script Completed' AS FinalStatus; 

SELECT * FROM Analysts, IncidentTypes, Incidents;



