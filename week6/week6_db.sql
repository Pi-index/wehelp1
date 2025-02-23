CREATE database week6_db;
USE week6_db;
CREATE TABLE members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    account VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
insert into members (username,account,password) values ('彭彭','test','test');

CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT NOT NULL,
    content text NOT NULL,
    FOREIGN KEY (member_id) REFERENCES members(id)
);