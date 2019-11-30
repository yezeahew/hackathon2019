CREATE TABLE files(
    fileid INT NOT NULL,
    filename VARCHAR(64) NOT NULL,
    unitid VARCHAR(20) NOT NULL,
    topic VARCHAR(64) NOT NULL,
    PRIMARY KEY(fileid)
);

CREATE TABLE units(
   unitid VARCHAR(20) NOT NULL,
   unitname VARCHAR(64) NOT NULL,
   PRIMARY KEY(unitid)
);
