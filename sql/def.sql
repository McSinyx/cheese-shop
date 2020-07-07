DROP DATABASE IF EXISTS cheese_shop;
CREATE DATABASE cheese_shop;
USE cheese_shop;

CREATE TABLE contacts (
  email varchar(255) PRIMARY KEY,
  name varchar(255));

CREATE TABLE releases (
  id smallint AUTO_INCREMENT PRIMARY KEY,
  project varchar(32),
  version varchar(32),
  summary varchar(255),
  homepage varchar(2083),
  email varchar(255),
  CONSTRAINT integrity UNIQUE (project, version),
  FOREIGN KEY (email) REFERENCES contacts(email));

CREATE TABLE troves (
  id smallint AUTO_INCREMENT PRIMARY KEY,
  classifier varchar(255) UNIQUE);

CREATE TABLE classifiers (
  release_id smallint,
  trove_id smallint,
  PRIMARY KEY (release_id, trove_id),
  FOREIGN KEY (release_id) REFERENCES releases(id),
  FOREIGN KEY (trove_id) REFERENCES troves(id));

CREATE TABLE keywords (
  release_id smallint,
  term varchar(32),
  PRIMARY KEY (release_id, term),
  FOREIGN KEY (release_id) REFERENCES releases(id));

CREATE TABLE dependencies (
  release_id smallint,
  dependency varchar(64),
  PRIMARY KEY (release_id, dependency),
  FOREIGN KEY (release_id) REFERENCES releases(id));

CREATE TABLE distributions (
  release_id smallint,
  filename varchar(255),
  size int,
  url varchar(255),
  dist_type varchar(16),
  python_version varchar(8),
  requires_python varchar(32),
  sha256 char(64),
  md5 char(32),
  PRIMARY KEY (release_id, filename),
  FOREIGN KEY (release_id) REFERENCES releases(id));
 
CREATE INDEX contacts_name_idx
ON contacts (name);

CREATE INDEX releases_summary_idx
ON releases (summary);

CREATE VIEW authorships
AS SELECT name as author, project
FROM contacts NATURAL JOIN releases
GROUP BY author, project;

DELIMITER //
CREATE PROCEDURE browse(class varchar(255))
BEGIN
  SELECT project, version
  FROM releases, classifiers
  WHERE id = release_id AND trove_id = (
    SELECT id
    FROM troves
    WHERE classifier = class);
END//

CREATE PROCEDURE release_data(project varchar(32), version varchar(32))
BEGIN
  DECLARE i smallint;
  SET i = (
    SELECT id
    FROM releases
    WHERE releases.project = project AND releases.version = version);
  SELECT project, version, homepage, name as author, email, summary
  FROM releases NATURAL JOIN contacts
  WHERE id = i;

  SELECT term as keyword
  FROM keywords
  WHERE release_id = i;

  SELECT classifier
  FROM classifiers, troves
  WHERE release_id = i AND trove_id = troves.id;

  SELECT dependency
  FROM dependencies
  WHERE release_id = i;
END//
DELIMITER ;
