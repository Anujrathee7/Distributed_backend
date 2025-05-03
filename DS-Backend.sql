-- Database tables and initial values
-- Ignore


CREATE TABLE users (username VARCHAR(30), pass VARCHAR(30), PRIMARY KEY (username, pass));
INSERT INTO users(username, pass) VALUES('user','123'),('jane doe','securepassword');

CREATE TABLE doctors (dname VARCHAR(30), 
						speciality VARCHAR(30),
						PRIMARY KEY (dname, speciality));
INSERT INTO doctors(dname, speciality) 
VALUES('Dr. Smith','Cardiologist'),('Dr. Johnson','Dermatologist');

ALTER TABLE users ADD CONSTRAINT unique_username UNIQUE (username);
ALTER TABLE doctors ADD CONSTRAINT unique_dname UNIQUE (dname);


CREATE TABLE appointments ( patient VARCHAR(30), 
							doctor VARCHAR(30),
							time VARCHAR(30),
							PRIMARY KEY (patient, doctor, time),
							FOREIGN KEY (patient) REFERENCES users(username),
							FOREIGN KEY (doctor) REFERENCES doctors(dname));

INSERT INTO appointments (patient, doctor, time)
VALUES('jane doe','Dr. Smith','2025-05-01T10:00:00'),
		('jane doe','Dr. Johnson','2025-05-02T14:00:00');




		