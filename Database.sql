#drop database if exists Traffic_Correction_Notices;
CREATE DATABASE IF NOT EXISTS Traffic_Correction_Notices
	CHARACTER SET utf8mb4
	COLLATE utf8mb4_unicode_ci;
    
USE Traffic_Correction_Notices;

DROP TABLE IF EXISTS Notice;

CREATE TABLE `Notice` (
	`NoticeID` INT NOT NULL AUTO_INCREMENT COMMENT 'auto increment for each new notice record',	
    `IndividualID` INT NOT NULL COMMENT 'int for ID number, not null as must have an value for the key',
    `VehicleID` INT NOT NULL COMMENT 'int for ID number, not null as must have an value for the key',
    `InformationID` INT NOT NULL COMMENT 'int for ID number, not null as must have an value for the key',
    `ViolationID` INT NOT NULL COMMENT 'int for ID number, not null as must have an value for the key',
    `OfficerID` INT NOT NULL COMMENT 'int for ID number, not null as must have an value for the key',
    `ActionSelection` INT NOT NULL COMMENT 'int for index of each action',
    `DriversSignature` VARCHAR(40) NOT NULL COMMENT 'limited to 20 chars, for individuals name, update to image in future',
    CONSTRAINT `pk_Notice` PRIMARY KEY (`NoticeID`)
);

START TRANSACTION;

Insert into `Notice`(IndividualID,VehicleID,InformationID,ViolationID,OfficerID,ActionSelection,DriversSignature) 
values (1,1,1,1,1404,12345,"fuckingworkpls");

COMMIT;

USE Traffic_Correction_Notices;
SHOW TABLES;
DESCRIBE Notice;
SELECT * FROM Notice;