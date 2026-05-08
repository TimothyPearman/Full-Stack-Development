DROP DATABASE IF EXISTS Traffic_Correction_Notices;

CREATE DATABASE Traffic_Correction_Notices;
USE Traffic_Correction_Notices;


# ----------------------------------------------------------------------tables---------------------------------------------------------------------- #


# ---------------------------------------------------------------------- #
# Add table "Notice"                                                     #
# ---------------------------------------------------------------------- #

CREATE TABLE `Notice` (
	`NoticeID` INT NOT NULL AUTO_INCREMENT COMMENT 'auto increment for each new notice record',	
    `IndividualID` INT NOT NULL COMMENT 'int for ID number, not null as must have an value for the key',
    `VehicleID` INT NOT NULL COMMENT 'int for ID number, not null as must have an value for the key',
    `InformationID` INT NOT NULL COMMENT 'int for ID number, not null as must have an value for the key',
    `ViolationID` INT NOT NULL COMMENT 'int for ID number, not null as must have an value for the key',
    `OfficerID` INT NOT NULL COMMENT 'int for ID number, not null as must have an value for the key',
    `ActionSelection` INT NOT NULL COMMENT 'int for index of each action',
    `DriversSignature` VARCHAR(100) NOT NULL COMMENT 'limited to 20 chars, for individuals name, update to image in future',
    CONSTRAINT `pk_Notice` PRIMARY KEY (`NoticeID`)
);

# ---------------------------------------------------------------------- #
# Add table "Individual"                                                 #
# ---------------------------------------------------------------------- #

CREATE TABLE `Individual` (
    `IndividualID` INT NOT NULL AUTO_INCREMENT COMMENT 'auto increment for each new notice record',
    `FirstName` VARCHAR(100) NOT NULL COMMENT 'limited to 20 chars, typical first names rarely exceed this length',
    `LastName` VARCHAR(100) NOT NULL COMMENT 'limited to 20 chars, typical last names rarely exceed this length',
    `Address` VARCHAR(100) NOT NULL COMMENT 'limited to 100 chars, addresses can be exceeding long especially for large/complex buildings',
    `City` VARCHAR(100) COMMENT 'limited to 21 chars, longest name in new york is `Port Washington North`',
    `StateID` INT NOT NULL  COMMENT 'int for ID number, not null as must have an value for the key',
    `ZipCode` VARCHAR(100) COMMENT 'limited to 9 chars, NYC zip codes are between 5 and 9 digits',
    `DriversLicense` VARCHAR(100) COMMENT 'limited to 15 chars, NYC Drivers  Licenses are between  15 digits', 
    `StateIssuedID` INT NOT NULL  COMMENT 'int for ID number, not null as must have an value for the key',
    `BirthDate` DATETIME NOT NULL COMMENT 'Datetime for more accurate and efficent data storage',
    `Height` VARCHAR(100) NOT NULL COMMENT 'limited to 5 chars, height measured in metric usually only requires 4 characters, 5 to be safe e.g. `5 11` ',
    `Weight` int NOT NULL COMMENT 'int as weight is measured in units',
    `Eyes` VARCHAR(100) NOT NULL COMMENT 'limited to 2 chars, eye colour only requires 2 letters to distinguish between entries e.g. BL (blue)',
	CONSTRAINT `pk_Individual` PRIMARY KEY (`IndividualID`)
);

# ---------------------------------------------------------------------- #
# Add table "User"                                    	                 #
# ---------------------------------------------------------------------- #

DROP TABLE IF EXISTS User;
CREATE TABLE `User` (
    `id` INT NOT NULL AUTO_INCREMENT COMMENT 'auto increment for each user',
    `Username` VARCHAR(100) NOT NULL UNIQUE,
    `Password` VARCHAR(100) NOT NULL,
    `Clearance` VARCHAR(100) NOT NULL,
    CONSTRAINT `pk_users` PRIMARY KEY (`id`)
);

# ---------------------------------------------------------------------- #
# Add table "Vehicle"                                                    #
# ---------------------------------------------------------------------- #

CREATE TABLE `Vehicle` (
    `VehicleID` INT NOT NULL AUTO_INCREMENT COMMENT 'auto increment for each new notice record',
    `VehicleLicense` VARCHAR(100) COMMENT 'limited to 8 chars, USA license plates can only be 8 digits long',
    `StateID` INT NOT NULL COMMENT 'int for ID number, not null as must have an value for the key',
    `Colour` VARCHAR(100) COMMENT 'comment',
    `Year` int NOT NULL COMMENT 'int, 4 digit number',
    `Make` VARCHAR(100) NOT NULL COMMENT 'limited to 20, no valid entries should exceed this',
    `Type` VARCHAR(100) NOT NULL COMMENT 'limited to 30, no valid entries should exceed this',
    `VIN` int COMMENT 'int, 17 digit number',
    `RegisteredOwner` VARCHAR(100) COMMENT 'limited to 40 chars, typical names rarely exceed this length',
    `Address` VARCHAR(100) COMMENT 'limited to 100 chars, addresse can be long but shouldnt exceed this',
    CONSTRAINT `pk_Vehicle` PRIMARY KEY (`VehicleID`)
);

# ---------------------------------------------------------------------- #
# Add table "States"                                                     #
# ---------------------------------------------------------------------- #

CREATE TABLE `States` (
    `StateID` INT NOT NULL AUTO_INCREMENT COMMENT 'auto increment for each new notice record',
    `State` VARCHAR(100) NOT NULL COMMENT 'limited to 14 chars, longest state name in the USA is `North Carolina`',
    CONSTRAINT `pk_State` PRIMARY KEY (`StateID`)
);

# ---------------------------------------------------------------------- #
# Add table "Information"                                                #
# ---------------------------------------------------------------------- #

CREATE TABLE `Information` (
    `InformationID` INT NOT NULL AUTO_INCREMENT COMMENT 'auto increment for each new notice record',
    `LocationID` INT NOT NULL COMMENT 'int for ID number, not null as must have an value for the key',
    `ViolationDate` DATETIME NOT NULL COMMENT 'Datetime for more accurate and efficent data storage',
    `District` int NOT NULL COMMENT 'int as NYC districts are identified numerically',
    `Detachment`int NOT NULL COMMENT 'int as NYC detachment are identified numerically',
    CONSTRAINT `pk_Information` PRIMARY KEY (`InformationID`)
);

# ---------------------------------------------------------------------- #
# Add table "Location"                                                   #
# ---------------------------------------------------------------------- #

CREATE TABLE `Location` (
    `LocationID` INT NOT NULL AUTO_INCREMENT COMMENT 'auto increment for each new notice record',
    `Miles` INT NOT NULL COMMENT 'int miles is a unit of measurement',
    `Direction` CHAR NOT NULL COMMENT 'char, cardinal direction can be identified with one letter e.g. N (North)',
    `Town` VARCHAR(100) NOT NULL COMMENT 'limited to 50 chars, names can be long but should not exceed this',
    `Road` VARCHAR(100) NOT NULL COMMENT 'limited to 50 chars, names can be long but should not exceed this',
    CONSTRAINT `pk_Location` PRIMARY KEY (`LocationID`)
);

# ---------------------------------------------------------------------- #
# Add table "Violations"                                                 #
# ---------------------------------------------------------------------- #


CREATE TABLE `Violation` (
    `ViolationID` INT NOT NULL AUTO_INCREMENT COMMENT 'auto increment for each new notice record',
    `Violation` TEXT NOT NULL COMMENT 'ver large string to accomodate multiple words ',
    CONSTRAINT `pk_Violation` PRIMARY KEY (`ViolationID`)
);

# ---------------------------------------------------------------------- #
# Add table "Officer"                                                    #
# ---------------------------------------------------------------------- #


CREATE TABLE `Officer` (
    `OfficerID` INT NOT NULL AUTO_INCREMENT COMMENT 'auto increment for each new notice record',
    `OfficersSignature` VARCHAR(100) NOT NULL COMMENT 'limited to 40 chars, typical names rarely exceed this length',
    `PersonnelNumber` int NOT NULL COMMENT 'int, personnel are identified by a numerical value',
	CONSTRAINT `pk_Officer` PRIMARY KEY (`OfficerID`)
);


# ----------------------------------------------------------------------info---------------------------------------------------------------------- #


# ---------------------------------------------------------------------- #
# Add info into all tables for Officer                                   #
# ---------------------------------------------------------------------- #

Insert into `Officer`(OfficersSignature,PersonnelNumber) 
values ("S Scott",850);
Insert into `Officer`(OfficersSignature,PersonnelNumber) 
values ("Timothy Pearman",28856139);
Insert into `Officer`(OfficersSignature,PersonnelNumber) 
values ("Amy Owen", 29128567);
Insert into `Officer`(OfficersSignature,PersonnelNumber) 
values ("Quinn Carr", 28945105);

# ---------------------------------------------------------------------- #
# Add info into all tables for States                                    #
# ---------------------------------------------------------------------- #

Insert into `States`(State) values ("Alabama");
Insert into `States`(State) values ("Alaska");
Insert into `States`(State) values ("Arizona");
Insert into `States`(State) values ("Arkansas");
Insert into `States`(State) values ("California");
Insert into `States`(State) values ("Colorado");
Insert into `States`(State) values ("Connecticut");
Insert into `States`(State) values ("Delaware");
Insert into `States`(State) values ("Florida");
Insert into `States`(State) values ("Georgia");
Insert into `States`(State) values ("Hawaii");
Insert into `States`(State) values ("Idaho");
Insert into `States`(State) values ("Illinois");
Insert into `States`(State) values ("Indiana");
Insert into `States`(State) values ("Iowa");
Insert into `States`(State) values ("Kansas");
Insert into `States`(State) values ("Kentucky");
Insert into `States`(State) values ("Louisiana");
Insert into `States`(State) values ("Maine");
Insert into `States`(State) values ("Maryland");
Insert into `States`(State) values ("Massachusetts");
Insert into `States`(State) values ("Michigan");
Insert into `States`(State) values ("Minnesota");
Insert into `States`(State) values ("Mississippi");
Insert into `States`(State) values ("Missouri");
Insert into `States`(State) values ("Montana");
Insert into `States`(State) values ("Nebraska");
Insert into `States`(State) values ("Nevada");
Insert into `States`(State) values ("New Hampshire");
Insert into `States`(State) values ("New Jersey");
Insert into `States`(State) values ("New Mexico");
Insert into `States`(State) values ("New York");
Insert into `States`(State) values ("North Carolina");
Insert into `States`(State) values ("North Dakota");
Insert into `States`(State) values ("Ohio");
Insert into `States`(State) values ("Oklahoma");
Insert into `States`(State) values ("Oregon");
Insert into `States`(State) values ("Pennsylvania");
Insert into `States`(State) values ("Rhode Island");
Insert into `States`(State) values ("South Carolina");
Insert into `States`(State) values ("South Dakota");
Insert into `States`(State) values ("Tennessee");
Insert into `States`(State) values ("Texas");
Insert into `States`(State) values ("Utah");
Insert into `States`(State) values ("Vermont");
Insert into `States`(State) values ("Virginia");
Insert into `States`(State) values ("Washington");
Insert into `States`(State) values ("West Virginia");
Insert into `States`(State) values ("Wisconsin");
Insert into `States`(State) values ("Wyoming");

# ---------------------------------------------------------------------- #
# Add info into all tables for `Record 1`                                #
# ---------------------------------------------------------------------- #

START TRANSACTION;

Insert into `Individual`(FirstName,LastName,Address,City,StateID,ZipCode,DriversLicense,StateIssuedID,BirthDate,Height,Weight,Eyes) 
values ("David M","Kroenke","5053 88 Ave SE",NULL,(SELECT StateID FROM States WHERE State LIKE "Washington"),NULL,NULL,1,"1946-2-27 00:00:00","6",165,"B");
SET @IndividualID = LAST_INSERT_ID();
Insert into `Vehicle`(VehicleLicense,StateID,Colour,Year,Make,Type,VIN,RegisteredOwner,Address) 
values (NULL,1,NULL,90,"Saab","900",NULL,"David_M_Kroenke",NULL);
SET @VehicleID = LAST_INSERT_ID();
Insert into `Location`(Miles,Direction,Town,Road) 
values (17,"E","Enumckum","SR410");
SET @LocationID = LAST_INSERT_ID();
Insert into `Information`(LocationID,ViolationDate,District,Detachment) 
values (@LocationID,"2003-11-7 09:35:00",2,17);
SET @InformationID = LAST_INSERT_ID();
Insert into `Violation`(Violation) 
values ("Writing text while driving");
SET @ViolationID = LAST_INSERT_ID();
Insert into `Notice`(IndividualID,VehicleID,InformationID,ViolationID,OfficerID,ActionSelection,DriversSignature) 
values (@IndividualID,@VehicleID,@InformationID,@ViolationID,(SELECT OfficerID FROM Officer WHERE OfficersSignature LIKE "S Scott"),1,
(SELECT CONCAT(FirstName,LastName) FROM `Individual` WHERE IndividualID like @IndividualID));

COMMIT;

# ---------------------------------------------------------------------- #
# Add info into all tables for `Record 2`                                #
# ---------------------------------------------------------------------- #

START TRANSACTION;

Insert into `Individual`(FirstName,LastName,Address,City,StateID,ZipCode,DriversLicense,StateIssuedID,BirthDate,Height,Weight,Eyes) 
values ("John","Smith","10031 936 Ave SE","",(SELECT StateID FROM States WHERE State LIKE "Washington"),NULL,NULL,1,"1111-11-1 11:11:11","",12345,"");
SET @IndividualID = LAST_INSERT_ID();
Insert into `Vehicle`(VehicleLicense,StateID,Colour,Year,Make,Type,VIN,RegisteredOwner,Address) 
values (NULL,1,NULL,12345,"","",NULL,"John_Smith",NULL);
SET @VehicleID = LAST_INSERT_ID();
Insert into `Location`(Miles,Direction,Town,Road) 
values (12345,"","","");
SET @LocationID = LAST_INSERT_ID();
Insert into `Information`(LocationID,ViolationDate,District,Detachment) 
values (@LocationID,"1111-11-1 11:11:11",12345,12345);
SET @InformationID = LAST_INSERT_ID();
Insert into `Violation`(Violation) 
values ("Speeding 15 mph over limit");
SET @ViolationID = LAST_INSERT_ID();
Insert into `Notice`(IndividualID,VehicleID,InformationID,ViolationID,OfficerID,ActionSelection,DriversSignature) 
values (@IndividualID,@VehicleID,@InformationID,@ViolationID,(SELECT OfficerID FROM Officer WHERE OfficersSignature LIKE "Timothy Pearman"),12345,
(SELECT CONCAT(FirstName,LastName) FROM `Individual` WHERE IndividualID like @IndividualID));

COMMIT;

# ---------------------------------------------------------------------- #
# Add info into all tables for `Record 3`                                #
# ---------------------------------------------------------------------- #

START TRANSACTION;

Insert into `Individual`(FirstName,LastName,Address,City,StateID,ZipCode,DriversLicense,StateIssuedID,BirthDate,Height,Weight,Eyes) 
values ("Emma","Lewis","11757 78 Ave NW",NULL,(SELECT StateID FROM States WHERE State LIKE "Washington"),NULL,NULL,1,"1111-11-1 11:11:11","",12345,"");
SET @IndividualID = LAST_INSERT_ID();
Insert into `Vehicle`(VehicleLicense,StateID,Colour,Year,Make,Type,VIN,RegisteredOwner,Address) 
values (NULL,1,NULL,12345,"","",NULL,"Emma_Lewis",NULL);
SET @VehicleID = LAST_INSERT_ID();
Insert into `Location`(Miles,Direction,Town,Road) 
values (12345,"","","");
SET @LocationID = LAST_INSERT_ID();
Insert into `Information`(LocationID,ViolationDate,District,Detachment) 
values (@LocationID,"1111-11-1 11:11:11",12345,12345);
SET @InformationID = LAST_INSERT_ID();
Insert into `Violation`(Violation) 
values ("");
SET @ViolationID = LAST_INSERT_ID();
Insert into `Notice`(IndividualID,VehicleID,InformationID,ViolationID,OfficerID,ActionSelection,DriversSignature) 
values (@IndividualID,@VehicleID,@InformationID,@ViolationID,(SELECT OfficerID FROM Officer WHERE OfficersSignature LIKE "Amy Owen"),12345,
(SELECT CONCAT(FirstName,LastName) FROM `Individual` WHERE IndividualID like @IndividualID));

COMMIT;

# ---------------------------------------------------------------------- #
# Add info into all tables for `Record 4`                                #
# ---------------------------------------------------------------------- #

START TRANSACTION;

Insert into `Individual`(FirstName,LastName,Address,City,StateID,ZipCode,DriversLicense,StateIssuedID,BirthDate,Height,Weight,Eyes) 
values ("Robert","Davis","11385 33 Ave NE",NULL,(SELECT StateID FROM States WHERE State LIKE "Washington"),NULL,NULL,1,"1111-11-1 11:11:11","",12345,"");
SET @IndividualID = LAST_INSERT_ID();
Insert into `Vehicle`(VehicleLicense,StateID,Colour,Year,Make,Type,VIN,RegisteredOwner,Address) 
values (NULL,1,NULL,12345,"","",NULL,"Robert_Davis",NULL);
SET @VehicleID = LAST_INSERT_ID();
Insert into `Location`(Miles,Direction,Town,Road) 
values (12345,"","","");
SET @LocationID = LAST_INSERT_ID();
Insert into `Information`(LocationID,ViolationDate,District,Detachment) 
values (@LocationID,"1111-11-1 11:11:11",12345,12345);
SET @InformationID = LAST_INSERT_ID();
Insert into `Violation`(Violation) 
values ("");
SET @ViolationID = LAST_INSERT_ID();
Insert into `Notice`(IndividualID,VehicleID,InformationID,ViolationID,OfficerID,ActionSelection,DriversSignature) 
values (@IndividualID,@VehicleID,@InformationID,@ViolationID,(SELECT OfficerID FROM Officer WHERE OfficersSignature LIKE "Quinn Carr"),12345,
(SELECT CONCAT(FirstName,LastName) FROM `Individual` WHERE IndividualID like @IndividualID));

COMMIT;

# ---------------------------------------------------------------------- #
# Add info into all tables for `Record 5`                                #
# ---------------------------------------------------------------------- #

START TRANSACTION;

Insert into `Individual`(FirstName,LastName,Address,City,StateID,ZipCode,DriversLicense,StateIssuedID,BirthDate,Height,Weight,Eyes) 
values ("Mary","Wilson","11106 8500 Ave SW",NULL,(SELECT StateID FROM States WHERE State LIKE "Washington"),NULL,NULL,1,"1111-11-1 11:11:11","",12345,"");
SET @IndividualID = LAST_INSERT_ID();
Insert into `Vehicle`(VehicleLicense,StateID,Colour,Year,Make,Type,VIN,RegisteredOwner,Address) 
values (NULL,1,NULL,12345,"","",NULL,"Mary_Wilson",NULL);
SET @VehicleID = LAST_INSERT_ID();
Insert into `Location`(Miles,Direction,Town,Road) 
values (12345,"","","");
SET @LocationID = LAST_INSERT_ID();
Insert into `Information`(LocationID,ViolationDate,District,Detachment) 
values (@LocationID,"1111-11-1 11:11:11",12345,12345);
SET @InformationID = LAST_INSERT_ID();
Insert into `Violation`(Violation) 
values ("");
SET @ViolationID = LAST_INSERT_ID();
Insert into `Notice`(IndividualID,VehicleID,InformationID,ViolationID,OfficerID,ActionSelection,DriversSignature) 
values (@IndividualID,@VehicleID,@InformationID,@ViolationID,(SELECT OfficerID FROM Officer WHERE OfficersSignature LIKE "Timothy Pearman"),12345,
(SELECT CONCAT(FirstName,LastName) FROM `Individual` WHERE IndividualID like @IndividualID));

COMMIT;

# ---------------------------------------------------------------------- #
# Add info into all tables for `Record 6`                                #
# ---------------------------------------------------------------------- #

START TRANSACTION;

Insert into `Individual`(FirstName,LastName,Address,City,StateID,ZipCode,DriversLicense,StateIssuedID,BirthDate,Height,Weight,Eyes) 
values ("William","Brown","11228 499 Ave NW",NULL,(SELECT StateID FROM States WHERE State LIKE "Washington"),NULL,NULL,1,"1111-11-1 11:11:11","",12345,"");
SET @IndividualID = LAST_INSERT_ID();
Insert into `Vehicle`(VehicleLicense,StateID,Colour,Year,Make,Type,VIN,RegisteredOwner,Address) 
values (NULL,1,NULL,12345,"","",NULL,"William_Brown",NULL);
SET @VehicleID = LAST_INSERT_ID();
Insert into `Location`(Miles,Direction,Town,Road) 
values (12345,"","","");
SET @LocationID = LAST_INSERT_ID();
Insert into `Information`(LocationID,ViolationDate,District,Detachment) 
values (@LocationID,"1111-11-1 11:11:11",12345,12345);
SET @InformationID = LAST_INSERT_ID();
Insert into `Violation`(Violation) 
values ("");
SET @ViolationID = LAST_INSERT_ID();
Insert into `Notice`(IndividualID,VehicleID,InformationID,ViolationID,OfficerID,ActionSelection,DriversSignature) 
values (@IndividualID,@VehicleID,@InformationID,@ViolationID,(SELECT OfficerID FROM Officer WHERE OfficersSignature LIKE "Amy Owen"),12345,
(SELECT CONCAT(FirstName,LastName) FROM `Individual` WHERE IndividualID like @IndividualID));

COMMIT;


# ----------------------------------------------------------------------constraints---------------------------------------------------------------------- #


# ---------------------------------------------------------------------- #
# Foreign key constraints                                                #
# ---------------------------------------------------------------------- #

ALTER TABLE `Notice`
ADD CONSTRAINT `fk_Notice_Individual` FOREIGN KEY (`IndividualID`)
		REFERENCES `Individual`(`IndividualID`);
        
ALTER TABLE `Notice`
ADD CONSTRAINT `fk_Notice_Vehicle` FOREIGN KEY (`VehicleID`)
		REFERENCES `Vehicle`(`VehicleID`);
        
ALTER TABLE `Notice`
ADD CONSTRAINT `fk_Notice_Information` FOREIGN KEY (`InformationID`)
		REFERENCES `Information`(`InformationID`);

ALTER TABLE `Notice`
ADD CONSTRAINT `fk_Notice_Violation` FOREIGN KEY (`ViolationID`)
		REFERENCES `Violation`(`ViolationID`);
        
ALTER TABLE `Notice`
ADD CONSTRAINT `fk_Notice_Officer` FOREIGN KEY (`OfficerID`)
		REFERENCES `Officer`(`OfficerID`);
        
ALTER TABLE `Individual`
ADD CONSTRAINT `fk_Individual_States` FOREIGN KEY (`StateID`)
		REFERENCES `States`(`StateID`);
        
ALTER TABLE `Individual`
ADD CONSTRAINT `fk_Individual_StateIssued` FOREIGN KEY (`StateIssuedID`)
		REFERENCES `States`(`StateID`);

ALTER TABLE `Vehicle`
ADD CONSTRAINT `fk_Vehicle_States` FOREIGN KEY (`StateID`)
		REFERENCES `States`(`StateID`);
        
ALTER TABLE `Information`
ADD CONSTRAINT `fk_Information_Location` FOREIGN KEY (`LocationID`)
		REFERENCES `Location`(`LocationID`);



# ----------------------------------------------------------------------Views---------------------------------------------------------------------- #


# ---------------------------------------------------------------------- #
# Add View "Full Notice Information"                                     #
# ---------------------------------------------------------------------- #

CREATE OR REPLACE SQL SECURITY DEFINER VIEW `Full_Notice` AS		#`SQL SECURITY DEFINER` used to allow querying of parent tables since users are only given access to the views.
SELECT NoticeID,Notice.IndividualID,Notice.VehicleID,Notice.InformationID,Notice.ViolationID,Notice.OfficerID,
FirstName,LastName,Individual.Address AS IndividualAddress,City,StateOfResidence.State AS ResidenceState,ZipCode,DriversLicense,StateIssued.State AS IssuedState,BirthDate,Height,Weight,Eyes,	#Individual Table
VehicleLicense,StateRegistered.State AS RegisteredState,Colour,Year,Make,Type,VIN,RegisteredOwner,Vehicle.Address AS VehicleAddress,															#Vehicle Table
ViolationDate,District,Detachment,																																								#Information Table
Miles,Direction,Town,Road,																																										#Location Table
Violation,																																														#Violations Table
OfficersSignature,PersonnelNumber,																																								#Officer Table
ActionSelection,DriversSignature																																								#Notice Table
FROM Notice 
INNER JOIN Individual
	ON Notice.IndividualID = Individual.IndividualID
INNER JOIN Vehicle 
	ON Notice.VehicleID = Vehicle.VehicleID
INNER JOIN States AS StateOfResidence
	ON Individual.StateID = StateOfResidence.StateID
INNER JOIN States AS StateIssued
	ON Individual.StateIssuedID = StateIssued.StateID
INNER JOIN States AS StateRegistered
	ON Vehicle.StateID = StateRegistered.StateID
INNER JOIN Information
	ON Notice.InformationID = Information.InformationID
INNER JOIN Location
	ON Information.LocationID = Location.LocationID
INNER JOIN Violation
	ON Notice.ViolationID = Violation.ViolationID
INNER JOIN Officer
	ON Notice.OfficerID = Officer.OfficerID
ORDER BY NoticeID ASC;

# ---------------------------------------------------------------------- #
# Add View "Citizen Access"                                              #
# ---------------------------------------------------------------------- #

CREATE OR REPLACE SQL SECURITY DEFINER VIEW `Citizen_Access` AS
SELECT *
FROM `Full_Notice`
where `RegisteredOwner` = SUBSTRING_INDEX(USER(), '@', 1);	#get only user name for checking condition

# ---------------------------------------------------------------------- #
# Add View "Officer Access"                                              #
# ---------------------------------------------------------------------- #

CREATE VIEW `Officer_Access` AS
SELECT *
FROM `Full_Notice`;


# ----------------------------------------------------------------------Users---------------------------------------------------------------------- #


# ---------------------------------------------------------------------- #
# Add Users "Citizens"                                                   #
# ---------------------------------------------------------------------- #

DROP USER IF EXISTS `John_Smith`;
DROP USER IF EXISTS `Emma_Lewis`;
DROP USER IF EXISTS `Robert_Davis`;
DROP USER IF EXISTS `Mary_Wilson`;
DROP USER IF EXISTS `William_Brown`;

CREATE USER `John_Smith` IDENTIFIED BY 'JPass';
GRANT SELECT ON Traffic_Correction_Notices.`Citizen_Access`  TO `John_Smith`;		#`GRANT SELECT`only given `select` permission to prevent unauthorised editing of database records 
Insert into `User`(ID,Username,Password,Clearance) 
values (2,"John_Smith","JPass", "Civilian");

CREATE USER `Emma_Lewis` IDENTIFIED BY 'EPass';
GRANT SELECT ON Traffic_Correction_Notices.`Citizen_Access`  TO `Emma_Lewis`;

CREATE USER `Robert_Davis` IDENTIFIED BY 'RPass';
GRANT SELECT ON Traffic_Correction_Notices.`Citizen_Access` TO `Robert_Davis`;

CREATE USER `Mary_Wilson` IDENTIFIED BY 'MPass';
GRANT SELECT ON Traffic_Correction_Notices.`Citizen_Access` TO `Mary_Wilson`;

CREATE USER `William_Brown` IDENTIFIED BY 'WPass';
GRANT SELECT ON Traffic_Correction_Notices.`Citizen_Access` TO `William_Brown`;

# ---------------------------------------------------------------------- #
# Add Users "Officers"                                                   #
# ---------------------------------------------------------------------- #

DROP USER IF EXISTS `Timothy_Pearman`;
DROP USER IF EXISTS `Amy_Owen`;
DROP USER IF EXISTS `Quinn_Myth`;

CREATE USER `Timothy_Pearman` IDENTIFIED BY 'TPass';
GRANT INSERT ON Traffic_Correction_Notices.`Officer_Access` TO `Timothy_Pearman`;		#`GRANT INSERT`only given `INSERT` permission to insert new notice records, not edit or view existing
Insert into `User`(ID,Username,Password,Clearance) 
values (3,"Timothy_Pearman","TPass", "Officer");

CREATE USER `Amy_Owen` IDENTIFIED BY 'APass';
GRANT INSERT ON Traffic_Correction_Notices.`Officer_Access` TO `Amy_Owen`;

CREATE USER `Quinn_Myth` IDENTIFIED BY 'QPass';
GRANT INSERT ON Traffic_Correction_Notices.`Officer_Access` TO `Quinn_Myth`;


# ----------------------------------------------------------------------Other---------------------------------------------------------------------- #


#improved code for future use with external codebase

#DROP USER `Citizen`;
#DROP USER `Officer`;

#CREATE USER `Citizen`;
#GRANT SELECT ON Traffic_Correction_Notice.`Citizen_Access`.* TO `Citizen`;

#CREATE USER `Officer` IDENTIFIED BY 'OfficerPass';
#GRANT INSERT ON Traffic_Correction_Notice.`Officer_Access` TO `Officer`;


# ----------------------------------------------------------------------Debug---------------------------------------------------------------------- #

#pre written querys for debugging databse elements
SHOW DATABASES;
USE Traffic_Correction_Notices;

SHOW TABLES;
SELECT * FROM Notice;
SELECT * FROM Individual;
SELECT * FROM Vehicle;
SELECT * FROM Information;
SELECT * FROM Location;
SELECT * FROM Violation;
SELECT * FROM Officer;

SELECT * FROM User;

SELECT * FROM Citizen_Access;
SELECT * FROM Full_Notice;