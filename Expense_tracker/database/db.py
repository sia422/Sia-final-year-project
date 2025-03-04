import sqlite3
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Define the database path
DB_PATH = Path("expense_tracker.db")


def get_db_connection():
    """
    Create and return a database connection.
    Ensures the database file exists before connecting.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn


def initialize_db():
    """
    Initialize the database with required tables and default data.
    Ensures tables are created only if they don't exist.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Create User table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS User (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL CHECK(email LIKE '%@%.%'),
                password TEXT NOT NULL,
                user_type TEXT NOT NULL CHECK(user_type IN ('ADMIN', 'USER')),
                is_staff INTEGER DEFAULT 0,
                is_superuser INTEGER DEFAULT 0
            )
        ''')

        # Create Category table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Category (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                icon TEXT
            )
        ''')

        # Create Expense table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Expense (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                amount REAL NOT NULL,
                currency TEXT NOT NULL,
                category TEXT,
                date TEXT NOT NULL,
                description TEXT,
                receipt TEXT,
                FOREIGN KEY (user_id) REFERENCES User(id)
            )
        ''')

        # Create Income table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Income (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                source TEXT NOT NULL,
                amount REAL NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES User(id)
            )
        ''')

        # Add default categories
        default_categories = [
            ("Food", "food_icon.png"),
            ("Transport", "transport_icon.png"),
            ("Entertainment", "entertainment_icon.png"),
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO Category (name, icon) VALUES (?, ?)
        ''', default_categories)

        # Add default admin user (use hashed passwords in production)
        default_admin = [
            ("admin", "admin@example.com", "hashed_password", "ADMIN", 1, 1),  # Replace "hashed_password" with actual hash
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO User (username, email, password, user_type, is_staff, is_superuser)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', default_admin)

        # Commit changes
        conn.commit()
        logging.info("Database initialized successfully.")
    except sqlite3.Error as e:
        logging.error(f"Error initializing database: {e}")
    finally:
        conn.close()


# Ensure the database is initialized when this module is imported
if not DB_PATH.exists():  # Only initialize if the database file doesn't exist
    initialize_db()