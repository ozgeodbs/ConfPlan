INSERT INTO sqlite_master (type, name, tbl_name, rootpage, sql) VALUES ('table', 'Category', 'Category', 2, 'CREATE TABLE Category (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Title VARCHAR(100) NOT NULL
, IsDeleted BOOLEAN DEFAULT 0, CreatedDate DATETIME, ChangedDate DATETIME)');
INSERT INTO sqlite_master (type, name, tbl_name, rootpage, sql) VALUES ('table', 'sqlite_sequence', 'sqlite_sequence', 3, 'CREATE TABLE sqlite_sequence(name,seq)');
INSERT INTO sqlite_master (type, name, tbl_name, rootpage, sql) VALUES ('table', 'Conference', 'Conference', 4, 'CREATE TABLE Conference (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Title VARCHAR(200) NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    Location VARCHAR(200) NOT NULL,
    Organizer VARCHAR(100) NOT NULL
, IsDeleted BOOLEAN DEFAULT 0, CreatedDate DATETIME, ChangedDate DATETIME, PhotoUrl TEXT, VideoUrl TEXT, LogoUrl TEXT)');
INSERT INTO sqlite_master (type, name, tbl_name, rootpage, sql) VALUES ('table', 'Speaker', 'Speaker', 6, 'CREATE TABLE Speaker (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName VARCHAR(100) NOT NULL,
    LastName VARCHAR(100) NOT NULL,
    Bio VARCHAR(255),
    Email VARCHAR(100) NOT NULL UNIQUE,
    Phone VARCHAR(20),
    PhotoUrl VARCHAR(255)
, IsDeleted BOOLEAN DEFAULT 0, CreatedDate DATETIME, ChangedDate DATETIME)');
INSERT INTO sqlite_master (type, name, tbl_name, rootpage, sql) VALUES ('index', 'sqlite_autoindex_Speaker_1', 'Speaker', 7, null);
INSERT INTO sqlite_master (type, name, tbl_name, rootpage, sql) VALUES ('table', 'Similarity', 'Similarity', 10, 'CREATE TABLE Similarity (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    PaperId INTEGER NOT NULL,
    SimilarPaperId INTEGER NOT NULL,
    SimilarityScore FLOAT NOT NULL,
    PaperTitle TEXT NOT NULL,              -- Paper''ın başlığı
    SimilarPaperTitle TEXT NOT NULL, IsDeleted BOOLEAN DEFAULT 0, CreatedDate DATETIME, ChangedDate DATETIME,       -- Similar Paper''ın başlığı
    FOREIGN KEY (PaperId) REFERENCES Paper(Id),
    FOREIGN KEY (SimilarPaperId) REFERENCES Paper(Id),
    CONSTRAINT unique_similarity UNIQUE (PaperId, SimilarPaperId)  -- Her iki paper arasındaki benzerlik yalnızca bir kez kaydedilir
)');
INSERT INTO sqlite_master (type, name, tbl_name, rootpage, sql) VALUES ('index', 'sqlite_autoindex_Similarity_1', 'Similarity', 11, null);
INSERT INTO sqlite_master (type, name, tbl_name, rootpage, sql) VALUES ('table', 'Hall', 'Hall', 14, 'CREATE TABLE "Hall" (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Capacity INTEGER NOT NULL,
    ConferenceId INTEGER NOT NULL,
    Title VARCHAR(255) NOT NULL,
    IsDeleted BOOLEAN DEFAULT 0,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    ChangedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ConferenceId) REFERENCES Conference(Id)
)');
INSERT INTO sqlite_master (type, name, tbl_name, rootpage, sql) VALUES ('table', 'Paper', 'Paper', 51, 'CREATE TABLE "Paper"
(
    Id           INTEGER
        primary key autoincrement,
    Title        VARCHAR(255)      not null,
    SpeakerId    INTEGER           not null
        references Speaker,
    CategoryId   INTEGER           not null
        references Category,
    Duration     INTEGER,
    Description  TEXT,
    HallId       INTEGER default 0 not null
        references Hall,
    ConferenceId INTEGER           not null
        references Conference,
    IsDeleted    BOOLEAN default 0,
    CreatedDate  DATETIME,
    ChangedDate  DATETIME,
    StartTime    DATETIME,
    EndTime      DATETIME
)');
