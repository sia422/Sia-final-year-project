import sqlite3
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Define the database path
DB_PATH = Path("finance_tracker.db")


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
    Initialize the database with required tables.
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

        # Commit changes
        conn.commit()
        logging.info("Database initialized successfully.")
    except sqlite3.Error as e:
        logging.error(f"Error initializing database: {e}")
    finally:
        if conn:
            conn.close()


def get_expenses(user_id):
    """
    Retrieve all expenses for a specific user.
    Args:
        user_id (int): The ID of the user.
    Returns:
        list: A list of expense dictionaries for the specified user.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT id, user_id, title, amount, currency, category, date
            FROM Expense
            WHERE user_id = ?
        ''', (user_id,))
        rows = cursor.fetchall()
        expenses = [
            {
                "id": row["id"],
                "user_id": row["user_id"],
                "title": row["title"],
                "amount": row["amount"],
                "currency": row["currency"],
                "category": row["category"],
                "date": row["date"]
            }
            for row in rows
        ]
        return expenses
    except sqlite3.OperationalError:
        logging.warning("Expense table does not exist. Please initialize the database.")
        return []
    except sqlite3.Error as e:
        logging.error(f"Database error retrieving expenses: {e}")
        return []
    finally:
        conn.close()


def add_expense(user_id, title, amount, currency, category, date):
    """
    Add a new expense entry to the database.
    Args:
        user_id (int): The ID of the user.
        title (str): The title of the expense.
        amount (float): The expense amount.
        currency (str): The currency of the expense.
        category (str): The category of the expense.
        date (str): The date of the expense (YYYY-MM-DD).
    Returns:
        bool: True if the expense was added successfully, False otherwise.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO Expense (user_id, title, amount, currency, category, date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, title, amount, currency, category, date))
        conn.commit()
        return True
    except sqlite3.OperationalError:
        logging.warning("Expense table does not exist. Please initialize the database.")
        return False
    except sqlite3.Error as e:
        logging.error(f"Database error adding expense: {e}")
        return False
    finally:
        conn.close()


def update_expense(expense_id, title, amount, currency, category, date):
    """
    Update an existing expense entry in the database.
    Args:
        expense_id (int): The ID of the expense to update.
        title (str): The updated title of the expense.
        amount (float): The updated expense amount.
        currency (str): The updated currency of the expense.
        category (str): The updated category of the expense.
        date (str): The updated date of the expense (YYYY-MM-DD).
    Returns:
        bool: True if the expense was updated successfully, False otherwise.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE Expense
            SET title = ?, amount = ?, currency = ?, category = ?, date = ?
            WHERE id = ?
        ''', (title, amount, currency, category, date, expense_id))
        conn.commit()
        if cursor.rowcount == 0:
            raise ValueError("No expense found with the provided ID.")
        return True
    except sqlite3.OperationalError:
        logging.warning("Expense table does not exist. Please initialize the database.")
        return False
    except sqlite3.Error as e:
        logging.error(f"Database error updating expense: {e}")
        return False
    except ValueError as ve:
        logging.error(f"Value error updating expense: {ve}")
        return False
    finally:
        conn.close()


def delete_expense(expense_id):
    """
    Delete an existing expense entry from the database.
    Args:
        expense_id (int): The ID of the expense to delete.
    Returns:
        bool: True if the expense was deleted successfully, False otherwise.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            DELETE FROM Expense
            WHERE id = ?
        ''', (expense_id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise ValueError("No expense found with the provided ID.")
        return True
    except sqlite3.OperationalError:
        logging.warning("Expense table does not exist. Please initialize the database.")
        return False
    except sqlite3.Error as e:
        logging.error(f"Database error deleting expense: {e}")
        return False
    except ValueError as ve:
        logging.error(f"Value error deleting expense: {ve}")
        return False
    finally:
        conn.close()


# Ensure the database is initialized when this module is imported
if not DB_PATH.exists():  # Only initialize if the database file doesn't exist
    initialize_db()