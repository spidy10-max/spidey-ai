"""
Spidey AI — Database Models / Schemas
Defines all database tables and their structure
"""

# ============================================================
#  TABLE: users
#  Stores user information and preferences
# ============================================================
CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL DEFAULT 'User',
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# ============================================================
#  TABLE: conversations
#  Stores conversation metadata
# ============================================================
CREATE_CONVERSATIONS_TABLE = """
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conv_id TEXT UNIQUE NOT NULL,
    title TEXT DEFAULT 'New Conversation',
    user_id INTEGER DEFAULT 1,
    provider TEXT DEFAULT 'groq',
    model TEXT DEFAULT 'llama-3.1-8b-instant',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    message_count INTEGER DEFAULT 0,
    is_archived INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
"""

# ============================================================
#  TABLE: messages
#  Stores individual chat messages
# ============================================================
CREATE_MESSAGES_TABLE = """
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conv_id TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('system', 'user', 'assistant')),
    content TEXT NOT NULL,
    tokens_used INTEGER DEFAULT 0,
    provider TEXT,
    model TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conv_id) REFERENCES conversations(conv_id)
);
"""

# ============================================================
#  TABLE: user_preferences
#  Stores things Spidey should remember about user
# ============================================================
CREATE_PREFERENCES_TABLE = """
CREATE TABLE IF NOT EXISTS user_preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER DEFAULT 1,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    category TEXT DEFAULT 'general',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(user_id, key)
);
"""

# ============================================================
#  TABLE: notes
#  Personal notes that Spidey remembers
# ============================================================
CREATE_NOTES_TABLE = """
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER DEFAULT 1,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    category TEXT DEFAULT 'general',
    is_important INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
"""

# ============================================================
#  All tables list — for easy initialization
# ============================================================
ALL_TABLES = [
    ("users", CREATE_USERS_TABLE),
    ("conversations", CREATE_CONVERSATIONS_TABLE),
    ("messages", CREATE_MESSAGES_TABLE),
    ("user_preferences", CREATE_PREFERENCES_TABLE),
    ("notes", CREATE_NOTES_TABLE),
]
