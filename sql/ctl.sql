USE mysql;

DROP USER IF EXISTS wensleydale@localhost;

CREATE USER wensleydale@localhost
IDENTIFIED BY '';

GRANT ALL PRIVILEGES ON cheese_shop.*
TO wensleydale@localhost;

UPDATE user
SET plugin='mysql_native_password'
WHERE User='wensleydale';

FLUSH PRIVILEGES;
