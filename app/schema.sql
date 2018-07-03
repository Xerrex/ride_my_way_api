DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS rides;
DROP TABLE IF EXISTS requests;

CREATE TABLE users(
    id uuid PRIMARY KEY,
    name varchar(120) NOT NULL,
    email varchar(120) NOT NULL UNIQUE,
    password varchar(256) NOT NULL
);

CREATE TABLE rides(
    id serial PRIMARY KEY,
    starting_point varchar(256) NOT NULL,
    destination varchar(256) NOT NULL,
    depart_time varchar(256) NOT NULL,
    eta varchar(256) NOT NULL,
    seats int NOT NULL,
    vehicle varchar(120) NOT NULL,
    driver uuid
);

CREATE TABLE requests(
    id serial PRIMARY KEY,
    ride_id int NOT NULL,
    user_id uuid NOT NULL,
    destination varchar(256) NOT NULL,
    status varchar(20
);