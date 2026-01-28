DROP DATABASE IF EXISTS test_db;

CREATE DATABASE test_db;
USE test_db;


# ----------------------------------------------------------------------tables---------------------------------------------------------------------- #


# ---------------------------------------------------------------------- #
# Add table "test_table"                                                     #
# ---------------------------------------------------------------------- #
DROP TABLE IF EXISTS `test_table`;
CREATE TABLE `test_table` (
	`id` INT NOT NULL AUTO_INCREMENT,
    `test_var` INT NOT NULL,
    `test_var2` INT NOT NULL,
    CONSTRAINT `pk_test_table` PRIMARY KEY (`id`)
);

Insert into `test_table`(test_var, test_var2) 
values (694202, 14042);

Insert into `test_table`(test_var, test_var2) 
values (3, 4);


# ----------------------------------------------------------------------Debug---------------------------------------------------------------------- #


SHOW DATABASES;
USE test_db;

SHOW TABLES;
SELECT * FROM `test_table`