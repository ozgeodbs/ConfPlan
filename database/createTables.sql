CREATE TABLE Category (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Title TEXT NOT NULL,
    IsDeleted BOOLEAN DEFAULT 0,
    CreatedDate TEXT DEFAULT CURRENT_TIMESTAMP,
    CreatedBy INTEGER DEFAULT 1,
    ChangedDate TEXT DEFAULT CURRENT_TIMESTAMP,
    ChangedBy INTEGER DEFAULT 1
);

CREATE TABLE Speaker (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    Bio TEXT,
    Email TEXT NOT NULL UNIQUE,
    Phone TEXT,
    PhotoUrl TEXT,
    IsDeleted BOOLEAN DEFAULT 0,
    CreatedDate TEXT DEFAULT CURRENT_TIMESTAMP,
    CreatedBy INTEGER DEFAULT 1,
    ChangedDate TEXT DEFAULT CURRENT_TIMESTAMP,
    ChangedBy INTEGER DEFAULT 1
);

CREATE TABLE Conference (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Title TEXT NOT NULL,
    StartDate TEXT NOT NULL,
    EndDate TEXT NOT NULL,
    Location TEXT NOT NULL,
    Organizer TEXT NOT NULL,
    IsDeleted BOOLEAN DEFAULT 0,
    CreatedDate TEXT DEFAULT CURRENT_TIMESTAMP,
    CreatedBy INTEGER DEFAULT 1,
    ChangedDate TEXT DEFAULT CURRENT_TIMESTAMP,
    ChangedBy INTEGER DEFAULT 1
);

CREATE TABLE Hall (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Capacity INTEGER NOT NULL,
    IsDeleted BOOLEAN DEFAULT 0,
    CreatedDate TEXT DEFAULT CURRENT_TIMESTAMP,
    CreatedBy INTEGER DEFAULT 1,
    ChangedDate TEXT DEFAULT CURRENT_TIMESTAMP,
    ChangedBy INTEGER DEFAULT 1
);

CREATE TABLE Paper (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Title TEXT NOT NULL,
    SpeakerId INTEGER NOT NULL,
    CategoryId INTEGER NOT NULL,
    Duration INTEGER,
    Description TEXT,
    HallId INTEGER NOT NULL,
    ConferenceId INTEGER NOT NULL,
    IsDeleted BOOLEAN DEFAULT 0,
    CreatedDate TEXT DEFAULT CURRENT_TIMESTAMP,
    CreatedBy INTEGER DEFAULT 1,
    ChangedDate TEXT DEFAULT CURRENT_TIMESTAMP,
    ChangedBy INTEGER DEFAULT 1,
    FOREIGN KEY (SpeakerId) REFERENCES Speaker(Id),
    FOREIGN KEY (CategoryId) REFERENCES Category(Id),
    FOREIGN KEY (HallId) REFERENCES Hall(Id),
    FOREIGN KEY (ConferenceId) REFERENCES Conference(Id)
);
