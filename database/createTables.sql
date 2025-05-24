create table Category
(
    Id          INTEGER
        primary key autoincrement,
    Title       VARCHAR(100) not null,
    IsDeleted   BOOLEAN default 0,
    CreatedDate DATETIME,
    ChangedDate DATETIME
);

create table Conference
(
    Id          INTEGER
        primary key autoincrement,
    Title       VARCHAR(200) not null,
    StartDate   DATE         not null,
    EndDate     DATE         not null,
    Location    VARCHAR(200) not null,
    Organizer   VARCHAR(100) not null,
    IsDeleted   BOOLEAN default 0,
    CreatedDate DATETIME,
    ChangedDate DATETIME,
    PhotoUrl    TEXT,
    VideoUrl    TEXT,
    LogoUrl     TEXT
);

create table Hall
(
    Id           INTEGER
        primary key autoincrement,
    Capacity     INTEGER      not null,
    ConferenceId INTEGER      not null
        references Conference,
    Title        VARCHAR(255) not null,
    IsDeleted    BOOLEAN  default 0,
    CreatedDate  DATETIME default CURRENT_TIMESTAMP,
    ChangedDate  DATETIME default CURRENT_TIMESTAMP
);

create table Speaker
(
    Id          INTEGER
        primary key autoincrement,
    FirstName   VARCHAR(100) not null,
    LastName    VARCHAR(100) not null,
    Bio         VARCHAR(255),
    Email       VARCHAR(100) not null
        unique,
    Phone       VARCHAR(20),
    PhotoUrl    VARCHAR(255),
    IsDeleted   BOOLEAN default 0,
    CreatedDate DATETIME,
    ChangedDate DATETIME
);

create table Paper
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
);

create table Similarity
(
    Id                INTEGER
        primary key autoincrement,
    PaperId           INTEGER not null
        references Paper,
    SimilarPaperId    INTEGER not null
        references Paper,
    SimilarityScore   FLOAT   not null,
    PaperTitle        TEXT    not null,
    SimilarPaperTitle TEXT    not null,
    IsDeleted         BOOLEAN default 0,
    CreatedDate       DATETIME,
    ChangedDate       DATETIME,
    constraint unique_similarity
        unique (PaperId, SimilarPaperId)
);

create table sqlite_master
(
    type     TEXT,
    name     TEXT,
    tbl_name TEXT,
    rootpage INT,
    sql      TEXT
);

create table sqlite_sequence
(
    name,
    seq
);

