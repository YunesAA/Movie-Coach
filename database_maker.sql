-- USER SCHEMA
DROP TABLE IF EXISTS User;

CREATE TABLE User(
	User_ID INTEGER NOT NULL PRIMARY KEY,
	Username TEXT NOT NULL UNIQUE,
    Password TEXT NOT NULL
);

INSERT INTO User (Username,Password) VALUES ('admin','admin'),('user','user');

-- MOVIE SCHEMA
DROP TABLE IF EXISTS Movie;

CREATE TABLE Movie(
    Movie_ID TEXT NOT NULL PRIMARY KEY,
    Title TEXT NOT NULL,
    Genre TEXT NOT NULL,
    Release_Date DATE,
    Director TEXT
);


--Rating Schema
DROP TABLE IF EXISTS Rating;

CREATE TABLE Rating(
	Comment_ID INTEGER NOT NULL PRIMARY KEY,
	User_ID INTEGER NOT NULL,
    Movie_ID TEXT NOT NULL,
    Comment_Text TEXT,
    Stars INTEGER,
    FOREIGN KEY(User_ID) REFERENCES User(User_ID),
    FOREIGN KEY(Movie_ID) REFERENCES Movie(Movie_ID)
);

DROP TABLE IF EXISTS Watchlist;
--Watchlist Schema
CREATE TABLE Watchlist (
    User_ID INTEGER NOT NULL,
    Movie_ID TEXT NOT NULL,
    Watchlist_ID INTEGER NOT NULL,
    PRIMARY KEY (User_ID, Movie_ID),
    FOREIGN KEY (User_ID) REFERENCES User(User_ID),
    FOREIGN KEY (Movie_ID) REFERENCES Movie(Movie_ID)
);


-- FOLLOWERS SCHEMA
DROP TABLE IF EXISTS Follower;

CREATE TABLE Follower(
    Follower_ID INTEGER NOT NULL,
    Following_ID INTEGER NOT NULL,
    PRIMARY KEY(Follower_ID, Following_ID),
    FOREIGN KEY(Follower_ID) REFERENCES User(User_ID),
    FOREIGN KEY(Following_ID) REFERENCES User(User_ID)
);

-- MOVIE HISTORY SCHEMA
DROP TABLE IF EXISTS Recommended;

CREATE TABLE Recommended(
    User_ID INTEGER NOT NULL,
    Movie_ID TEXT NOT NULL,
    Title TEXT NOT NULL,
    Genre TEXT,
    Stars INTEGER,
    Movie_History TEXT,
    FOREIGN KEY(User_ID) REFERENCES User(User_ID),
    FOREIGN KEY(Movie_ID) REFERENCES Movie(Movie_ID)
);