#Task2#
'''
CREATE DATABASE website;
USE website;
CREATE TABLE member (
id BIGINT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(255) NOT NULL,
username VARCHAR(255) NOT NULL,
password VARCHAR(255) NOT NULL,
follower_count INT UNSIGNED NOT NULL DEFAULT 0,
time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
'''

#Task3#
'''
INSERT INTO member (name,username,password) VALUES ('test','test','test');
select * from member;
INSERT INTO member (name, username, password, follower_count) VALUES
('Apple', 'a1', 'password1', 100),
('Bagal', 'b2', 'password2', 200),
('Comic', 'c3', 'password3', 300),
('D', 'd4', 'd4', 400);

select * from member;
SELECT * FROM member ORDER BY time DESC;
SELECT * FROM member ORDER BY time DESC LIMIT 3 OFFSET 1;
SELECT * FROM member WHERE username='test';
SELECT * FROM member WHERE name LIKE '%es%';
SELECT * FROM member WHERE username='test' AND password='test';
UPDATE member SET name='test2' WHERE username='test';
SELECT * FROM member;
'''

#Task4#
'''
SELECT COUNT(*) FROM member;
SELECT SUM(follower_count) FROM member;
SELECT AVG(follower_count) FROM member;
SELECT AVG(follower_count)
FROM (
    SELECT follower_count
    FROM member
    ORDER BY follower_count DESC
    LIMIT 2
) AS F2;
'''

#Task5#
'''
USE website;

CREATE TABLE message (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    member_id BIGINT NOT NULL,
    content VARCHAR(255) NOT NULL,
    like_count INT UNSIGNED NOT NULL DEFAULT 0,
    time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES member(id)
);

INSERT INTO message (member_id, content, like_count) VALUES
	(1, 'Hello World!', 10),
	(1, 'This is a test message.', 5),
	(2, 'Hi there!', 3),
	(3, 'Greetings!', 7),
	(4, 'Welcome to the chat.', 2);

SELECT ms.id, ms.member_ID, ms.content, ms.like_count, ms.time FROM message ms JOIN member mb ON ms.member_id= mb.id;

SELECT ms.id, ms.member_ID, ms.content, ms.like_count, ms.time FROM message ms JOIN member mb ON ms.member_id= mb.id WHERE mb.username = 'test';

SELECT AVG(ms.like_count) FROM message ms  JOIN member mb ON ms.member_id= mb.id WHERE mb.username = 'test';

SELECT mb.username, AVG(ms.like_count) FROM message ms 
JOIN member mb ON ms.member_id= mb.id 
GROUP BY mb.username;
'''
