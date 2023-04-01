DROP DATABASE railroad_nakhod;
CREATE DATABASE railroad_nakhod;
USE railroad_nakhod;

CREATE TABLE user_role (
    id INT AUTO_INCREMENT,
    name VARCHAR(50),
    PRIMARY KEY (id)
);

CREATE TABLE user (
    id INT AUTO_INCREMENT,
    name VARCHAR(50),
    email VARCHAR(50),
    password_hash CHAR(60),
    user_role_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (user_role_id)
        REFERENCES user_role(id)
        ON DELETE SET NULL
);

CREATE TABLE train (
    id INT AUTO_INCREMENT,
    name VARCHAR(50),
    PRIMARY KEY (id)
);

CREATE TABLE station (
    id INT AUTO_INCREMENT,
    name VARCHAR(50), 
    PRIMARY KEY (id)
);

CREATE TABLE trip (
    id INT AUTO_INCREMENT,
    train_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (train_id)
        REFERENCES train(id)
        ON DELETE SET NULL
);

CREATE TABLE trip_station (
    id INT AUTO_INCREMENT,
    trip_id INT,
    station_id INT,
    num INT,
    time_arr DATETIME,
    time_dep DATETIME,
    price INT,
    PRIMARY KEY (id),
    FOREIGN KEY (trip_id)
        REFERENCES trip(id)
        ON DELETE SET NULL,
    FOREIGN KEY (station_id)
        REFERENCES station(id)
        ON DELETE SET NULL
);

CREATE TABLE carriage_type (
    id INT AUTO_INCREMENT,
    name VARCHAR(50),
    price_mod FLOAT,
    PRIMARY KEY (id)
);

CREATE TABLE carriage (
    id INT AUTO_INCREMENT,
    num INT,
    train_id INT,
    carriage_type_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (train_id)
        REFERENCES train(id)
        ON DELETE SET NULL,
    FOREIGN KEY (carriage_type_id)
        REFERENCES carriage_type(id)
        ON DELETE SET NULL
);

CREATE TABLE seat (
    id INT AUTO_INCREMENT,
    num INT,
    carriage_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (carriage_id)
        REFERENCES carriage(id)
        ON DELETE SET NULL
);

CREATE TABLE ticket (
    id INT AUTO_INCREMENT,
    user_id INT,
    seat_id INT,
    trip_station_start_id INT,
    trip_station_end_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id)
        REFERENCES user(id)
        ON DELETE SET NULL,
    FOREIGN KEY (seat_id)
        REFERENCES seat(id)
        ON DELETE SET NULL,
    FOREIGN KEY (trip_station_start_id)
        REFERENCES trip_station(id)
        ON DELETE SET NULL,
    FOREIGN KEY (trip_station_end_id)
        REFERENCES trip_station(id)
        ON DELETE SET NULL
);





INSERT INTO user_role (
    name
)
VALUES (
    'admin'
),
(
    'client'
);

INSERT INTO user (
    name,
    email,
    password_hash,
    user_role_id
)
VALUES (
    'Oleksii',
    'alexey.nakhod@gmail.com',
    '$2y$10$1FVZyP50I7YrEcEcpnAvPOWnIwHXyAsvw3THYhmsEsXKkWOnYHAGa',
    (SELECT id FROM user_role WHERE name = 'client')
);

INSERT INTO train (
    name
)
VALUES (
    '749 K'
);

INSERT INTO carriage_type (
    name,
    price_mod
)
VALUES (
    'C1',
    1.0
);

INSERT INTO carriage (
    num,
    train_id,
    carriage_type_id
)
VALUES (
    7,
    (SELECT id FROM train WHERE name = '749 K'),
    (SELECT id FROM carriage_type WHERE name = 'C1')
);

INSERT INTO seat (
    num,
    carriage_id
)
VALUES (
    20,
    (SELECT id FROM carriage WHERE num = 7)
);



INSERT INTO station (
    name
)
VALUES (
    'A'
),
(
    'B'
),
(
    'C'
);

INSERT INTO trip (
    train_id
)
VALUES (
    (SELECT id FROM train WHERE name = '749 K')
);

INSERT INTO trip_station (
    trip_id,
    num,
    station_id,
    time_arr,
    time_dep,
    price
)
VALUES (
    (SELECT id FROM trip WHERE train_id = (SELECT id FROM train WHERE name = '749 K')),
    1,
    (SELECT id FROM station WHERE name = 'A'),
    '2023-03-27 13:00:00',
    '2023-03-27 13:00:00',
    0
),
(
    (SELECT id FROM trip WHERE train_id = (SELECT id FROM train WHERE name = '749 K')),
    2,
    (SELECT id FROM station WHERE name = 'C'),
    '2023-03-27 13:00:00',
    '2023-03-27 19:00:00',
    400
);

INSERT INTO ticket (
    user_id,
    seat_id,
    trip_station_start_id,
    trip_station_end_id
)
VALUES (
    (SELECT id FROM user WHERE email = 'alexey.nakhod@gmail.com'),
    (SELECT id FROM seat WHERE num = 20),
    (SELECT id FROM trip_station WHERE price = 0),
    (SELECT id FROM trip_station WHERE price = 400)
);