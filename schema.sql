-- users (simplified)
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);

-- disclosure profile
CREATE TABLE disclosures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    diagnosis TEXT,
    medications TEXT,
    therapy_type TEXT,
    notes TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

-- recipients (psychiatrist, therapist, disability office)
CREATE TABLE recipients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    name TEXT,
    role TEXT, -- psychiatrist | therapist | disability_office
    phone TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

-- shared disclosures
CREATE TABLE shares (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    disclosure_id INTEGER,
    recipient_id INTEGER,
    fields TEXT, -- comma-separated list of fields shared
    FOREIGN KEY(disclosure_id) REFERENCES disclosures(id),
    FOREIGN KEY(recipient_id) REFERENCES recipients(id)
);
