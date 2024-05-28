PRAGMA foreign_keys = ON;

INSERT INTO users(username, password, first_name, last_name)
VALUES ("drevsine", "sha256$6802e0a66d1bbb1ce80cea8efd9036f8$a0d654639c746fe04df07c3ff9111e4cc779f9879328b76b90929a2892ed606e", "Dylan", "Revsine");

INSERT INTO users(username, password, first_name, last_name)
VALUES ("mtaylor", "sha256$6802e0a66d1bbb1ce80cea8efd9036f8$a0d654639c746fe04df07c3ff9111e4cc779f9879328b76b90929a2892ed606e", "Michael", "Taylor");

INSERT INTO users(username, password, first_name, last_name)
VALUES ("lweiss", "sha256$6802e0a66d1bbb1ce80cea8efd9036f8$a0d654639c746fe04df07c3ff9111e4cc779f9879328b76b90929a2892ed606e", "Lori", "Weiss");

INSERT INTO users(username, password, first_name, last_name)
VALUES ("mking", "sha256$6802e0a66d1bbb1ce80cea8efd9036f8$a0d654639c746fe04df07c3ff9111e4cc779f9879328b76b90929a2892ed606e", "Matthew", "King");

INSERT INTO contacts(contact_owner, first_name, last_name, profile_picture, phone_number, email_address, home_address)
VALUES ("drevsine", "Ethan", "Johnson", "", "", "ethan.johnson@example.com", "");

INSERT INTO contacts(contact_owner, first_name, last_name, profile_picture, phone_number, email_address, home_address)
VALUES ("drevsine", "Michael", "Taylor", "", "", "michael.taylor@example.com", "");

INSERT INTO contacts(contact_owner, first_name, last_name, profile_picture, phone_number, email_address, home_address)
VALUES ("drevsine", "Lori", "Weiss", "", "", "lori.weiss@example.com", "");

INSERT INTO contacts(contact_owner, first_name, last_name, profile_picture, phone_number, email_address, home_address)
VALUES ("drevsine", "Matthew", "King", "", "", "matthew.king@example.com", "");

INSERT INTO contacts(contact_owner, first_name, last_name, profile_picture, phone_number, email_address, home_address)
VALUES ("mtaylor", "Dylan", "Revsine", "", "", "dylan.revsine@example.com", "");

INSERT INTO contacts(contact_owner, first_name, last_name, profile_picture, phone_number, email_address, home_address)
VALUES ("mtaylor", "Lori", "Weiss", "", "", "lori.weiss@example.com", "");

INSERT INTO contacts(contact_owner, first_name, last_name, profile_picture, phone_number, email_address, home_address)
VALUES ("mtaylor", "Matthew", "King", "", "", "matthew.king@example.com", "");

INSERT INTO contacts(contact_owner, first_name, last_name, profile_picture, phone_number, email_address, home_address)
VALUES ("mtaylor", "Sally", "Jenkins", "", "", "sally.jenkins@example.com", "");

INSERT INTO contacts(contact_owner, first_name, last_name, profile_picture, phone_number, email_address, home_address)
VALUES ("lweiss", "Dylan", "Revsine", "", "", "dylan.revsine@example.com", "");

INSERT INTO contacts(contact_owner, first_name, last_name, profile_picture, phone_number, email_address, home_address)
VALUES ("lweiss", "Michael", "Taylor", "", "", "michael.taylor@example.com", "");

INSERT INTO contacts(contact_owner, first_name, last_name, profile_picture, phone_number, email_address, home_address)
VALUES ("lweiss", "Matthew", "King", "", "", "matthew.king@example.com", "");

INSERT INTO contacts(contact_owner, first_name, last_name, profile_picture, phone_number, email_address, home_address)
VALUES ("lweiss", "George", "Mitchell", "", "", "george.mitchell@example.com", "");

INSERT INTO contacts(contact_owner, first_name, last_name, profile_picture, phone_number, email_address, home_address)
VALUES ("mking", "Dylan", "Revsine", "", "", "dylan.revsine@example.com", "");

INSERT INTO contacts(contact_owner, first_name, last_name, profile_picture, phone_number, email_address, home_address)
VALUES ("mking", "Michael", "Taylor", "", "", "michael.taylor@example.com", "");

INSERT INTO contacts(contact_owner, first_name, last_name, profile_picture, phone_number, email_address, home_address)
VALUES ("mking", "Lori", "Weiss", "", "", "lori.weiss@example.com", "");

INSERT INTO contacts(contact_owner, first_name, last_name, profile_picture, phone_number, email_address, home_address)
VALUES ("mking", "Janet", "Smith", "", "", "janet.smith@example.com", "");
