-- users (employees) table
CREATE TABLE user (id INTEGER PRIMARY KEY ,
                    first_name TEXT NOT NULL,
                    middle_name TEXT,
                    last_name TEXT NOT NULL,
                    username TEXT NOT NULL,
                    hash TEXT NOT NULL,
                    role TEXT NOT NULL, --"Admin","Receptionist"
                    status TEXT NULL-- "Working","Fired","Retired","Moved","Promoted","Demoted","Transferred"
                    );
-- rooms table
CREATE TABLE room (id INTEGER PRIMARY KEY ,
                    room_number INTEGER NOT NULL,
                    status TEXT NOT NULL,-- "open","reserved"
                    price NUMERIC NOT NULL);
-- action report table
CREATE TABLE Employee_Check_In_Record (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    number_of_reservations INTEGER,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
-- patient table
CREATE TABLE patient (id INTEGER PRIMARY KEY,
                        first_name TEXT NOT NULL,
                        middle_name TEXT,
                        last_name TEXT NOT NULL,
                        birth_date DATE NOT NULL,
                        age INTEGER,
                        gender TEXT NOT NULL,
                        Email varchar(255),
                        phone1 VARCHAR(15) NOT NULL,
                        phone2 VARCHAR(15),
                        emergency_contact_name TEXT NOT NULL,
                        emergency_contact_relation TEXT NOT NULL,
                        emergency_contact_phone VARCHAR(15) NOT NULL,
                        emergency_contact_address TEXT,
                        registration_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        Patient_reservation_status TEXT NOT NULL, -- "wait for a room" , "checked in"
                        user_id INTEGER NOT NULL,                        
                        FOREIGN KEY (user_id) REFERENCES user(id));
-- reservations table
CREATE TABLE reservation (id INTEGER PRIMARY KEY ,
                            roomid INTEGER NOT NULL,
                            patient_id INTEGER NOT NULL,
                            user_id INTEGER NOT NULL,
                            price NUMERIC,
                            checkin DATE NOT NULL,
                            checkout DATE NOT NULL,
                            days INTEGER,
                            exit_date DATE,
                            reservation_status TEXT NOT NULL,-- "Done" , "checked out", "hold"
                            payment TEXT NOT NULL,-- "Cash" , "Visa, Mastercard"
                            registration_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                            purpose varchar(20), -- "general consultation", "specialist visit", "surgery", "emergency care"
                            FOREIGN KEY (user_id) REFERENCES user(id),
                            FOREIGN KEY (patient_id) REFERENCES patient(id),
                            FOREIGN KEY (roomid) REFERENCES room(id));

-- contact information
CREATE TABLE contactinformation (
    contact_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    subject VARCHAR(255),
    message TEXT,
    user_id_read_it INT,
    FOREIGN KEY (user_id_read_it) REFERENCES user(id)
);


--clinic part
-- clinics table
CREATE TABLE clinic (
    clinic_id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(13), -- Assuming country code (+20) and 10-digit mobile number +201XXXXXXXXX 
    email VARCHAR(100),
    operating_hours VARCHAR(255)
);

-- doctors table
CREATE TABLE doctor (
    doctor_id INT PRIMARY KEY,
    clinic_id INT,
    first_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    last_name VARCHAR(50) NOT NULL,
    specialty VARCHAR(100),
    phone_number VARCHAR(13), -- Assuming country code (+20) and 10-digit mobile number +201XXXXXXXXX 
    email_address VARCHAR(100),
    max_appointment_per_day INT,
    qualifications TEXT,
    years_of_experience INT,
    consultation_fee DECIMAL(10, 2),
    FOREIGN KEY (clinic_id) REFERENCES clinic(clinic_id)
);
-- appointment table (available time)
CREATE TABLE appointment (
    appointment_id INT PRIMARY KEY,
    doctor_id INT,
    clinic_id INT,
    appointment_date DATE,
    appointment_time TIME,
    status TEXT, -- "occupied", "Available"
    FOREIGN KEY (doctor_id) REFERENCES doctor(doctor_id),
    FOREIGN KEY (clinic_id) REFERENCES clinic(clinic_id)
);


-- booked appointments table 
CREATE TABLE bookedappointment (
    appointment_id INT PRIMARY KEY,
    appointment_from_table_id INT,
    doctor_id INT,
    clinic_id INT,
    user_id_read_it INT,
    patient_name VARCHAR(100),
    patient_phone VARCHAR(13),
    patient_email TEXT,
    status VARCHAR(50), -- status "booked"
    FOREIGN KEY (appointment_from_table_id) REFERENCES appointment(appointment_id),
    FOREIGN KEY (doctor_id) REFERENCES doctor(doctor_id),
    FOREIGN KEY (clinic_id) REFERENCES clinic(clinic_id),
    FOREIGN KEY (user_id_read_it) REFERENCES user(id)
);
