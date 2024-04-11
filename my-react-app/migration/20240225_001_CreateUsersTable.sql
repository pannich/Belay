CREATE TABLE IF NOT EXISTS Users (
  id INTEGER PRIMARY KEY,
  username TEXT UNIQUE,
  password TEXT,
  session_token VARCHAR(40)
);
