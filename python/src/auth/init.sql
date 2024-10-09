-- auth service user creation
-- CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'this_is_auth_password';

-- CREATE DATABASE auth;
-- GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';

USE auth;

DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id INT(30) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email varchar(255) NOT NULL UNIQUE,
    password varchar(255) NOT NULL
);

INSERT INTO user (email, password) VALUES ('email', 'passwd');
COMMIT;