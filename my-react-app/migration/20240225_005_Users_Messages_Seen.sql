CREATE TABLE IF NOT EXISTS Users_Messages_Seen (
    user_id INTEGER NOT NULL,
    channel_id INTEGER NOT NULL,
    last_message_id_seen INTEGER NOT NULL,
    PRIMARY KEY (user_id, channel_id),
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (channel_id) REFERENCES Channels(id),
    FOREIGN KEY (last_message_id_seen) REFERENCES Messages(id)
);
