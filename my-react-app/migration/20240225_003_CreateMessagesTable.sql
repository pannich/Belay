CREATE TABLE IF NOT EXISTS Messages (
  id INTEGER PRIMARY KEY,
  channel_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  content TEXT NOT NULL,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  replies_to INTEGER,
  FOREIGN KEY(channel_id) REFERENCES Channels(id),
  FOREIGN KEY(user_id) REFERENCES Users(id),
  FOREIGN KEY (replies_to) REFERENCES Messages(id)
);
