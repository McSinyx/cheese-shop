DROP DATABASE IF EXISTS cheese_shop;
CREATE DATABASE cheese_shop;
USE cheese_shop;

CREATE TABLE IF NOT EXISTS releases (
  id smallint AUTO_INCREMENT PRIMARY KEY,
  project varchar(32),
  version varchar(32));

CREATE TABLE IF NOT EXISTS information (
  release_id smallint PRIMARY KEY,
  summary varchar(255),
  homepage varchar(2083),
  email varchar(255));

CREATE TABLE IF NOT EXISTS contacts (
  email varchar(255) PRIMARY KEY,
  name varchar(255));

CREATE TABLE IF NOT EXISTS classifiers (
  release_id smallint,
  trove_id smallint,
  PRIMARY KEY (release_id, trove_id));

CREATE TABLE IF NOT EXISTS troves (
  id smallint AUTO_INCREMENT PRIMARY KEY,
  classifier varchar(255));

CREATE TABLE IF NOT EXISTS keywords (
  release_id smallint,
  term varchar(32),
  PRIMARY KEY (release_id, term));

CREATE TABLE IF NOT EXISTS distributions (
  release_id smallint,
  filename varchar(255),
  url varchar(255),
  python_version varchar(8),
  requires_python varchar(32),
  requires_dist varchar(64),
  size int,
  sha256 char(64),
  md5 char(32),
  PRIMARY KEY (release_id, filename));
