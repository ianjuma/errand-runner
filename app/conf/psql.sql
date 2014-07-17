CREATE TABLE Tasks(task_id SERIAL PRIMARY KEY NOT NULL, task_title varchar(200) NOT NULL, 
	task_desc TEXT NOT NULL, due_date DATE NOT NULL, task_status varchar(100) NOT NULL, 
	username varchar(200) NOT NULL, task_category varchar(100) NOT NULL);


CREATE TABLE UsersInfo(email varchar(200) NOT NULL, mobileNo varchar(100) NOT NULL, 
	dob DATE NOT NULL, password TEXT NOT NULL, smscode DOUBLE PRECISION, 
	state varchar(100) NOT NULL, username VARCHAR(200) NOT NULL PRIMARY KEY);


CREATE TABLE Payments(credit_available INTEGER NOT NULL, username VARCHAR(200) NOT NULL PRIMARY KEY);


CREATE TABLE Admin(username VARCHAR(200) NOT NULL PRIMARY KEY, password VARCHAR(200) NOT NULL);

CREATE TABLE NewsLetter(username VARCHAR(200) NOT NULL PRIMARY KEY, email VARCHAR(200) NOT NULL);