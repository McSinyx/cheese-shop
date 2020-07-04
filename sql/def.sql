DROP DATABASE IF EXISTS cheese_shop;
CREATE DATABASE cheese_shop;
USE cheese_shop;

CREATE TABLE releases (
  id smallint AUTO_INCREMENT PRIMARY KEY,
  project varchar(32),
  version varchar(32));

CREATE TABLE contacts (
  email varchar(255) PRIMARY KEY,
  name varchar(255));

CREATE TABLE information (
  release_id smallint PRIMARY KEY,
  summary varchar(255),
  homepage varchar(2083),
  email varchar(255),
  FOREIGN KEY (release_id) REFERENCES releases(id),
  FOREIGN KEY (email) REFERENCES contacts(email));

CREATE TABLE troves (
  id smallint AUTO_INCREMENT PRIMARY KEY,
  classifier varchar(255));

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

CREATE TABLE distributions (
  release_id smallint,
  filename varchar(255),
  url varchar(255),
  python_version varchar(8),
  requires_python varchar(32),
  requires_dist varchar(64),
  size int,
  sha256 char(64),
  md5 char(32),
  PRIMARY KEY (release_id, filename),
  FOREIGN KEY (release_id) REFERENCES releases(id));
