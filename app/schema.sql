DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS rides;
DROP TABLE IF EXISTS requests;

CREATE TABLE users(
    id TEXT PRIMARY KEY,
    name TEXT(120) NOT NULL,
    email TEXT(120) NOT NULL UNIQUE,
    password TEXT(256) NOT NULL
);

CREATE TABLE rides(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    starting_point TEXT(256) NOT NULL,
    destination TEXT(256) NOT NULL,
    depart_time TEXT(256) NOT NULL,
    eta TEXT(256) NOT NULL,
    seats INTEGER NOT NULL,
    vehicle TEXT(120) NOT NULL,
    driver TEXT,
    FOREIGN KEY (driver) REFERENCES users(id)
);

CREATE TABLE requests(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ride_id INTEGER NOT NULL,
    user_id TEXT NOT NULL,
    destination TEXT(256) NOT NULL,
    req_status TEXT(20),
    FOREIGN KEY(ride_id) REFERENCES rides(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
);