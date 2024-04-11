CREATE TABLE IF NOT EXISTS Reactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emoji TEXT NOT NULL,
    message_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (message_id) REFERENCES Messages(id),
    FOREIGN KEY (user_id) REFERENCES Users(id)
    -- ,UNIQUE(emoji, user_id, message_id) -- unique TO TEST
);
