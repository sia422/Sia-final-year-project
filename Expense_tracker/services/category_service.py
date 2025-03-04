import sqlite3

# Database configuration
DATABASE_FILE = 'expense_tracker.db'

def get_db_connection():
    """Create and return a SQLite database connection."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row  # Enable dictionary-style row access
    return conn

def add_category(name, icon):
    """
    Add a new category to the database.
    Args:
        name (str): The name of the category.
        icon (str): The icon associated with the category.
    Returns:
        bool: True if the category was added successfully, False otherwise.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Validate inputs
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Category name must be a non-empty string.")
        if not isinstance(icon, str):
            raise ValueError("Icon must be a string.")

        # Insert the category into the database
        cursor.execute('''
            INSERT INTO Category (name, icon)
            VALUES (?, ?)
        ''', (name.strip(), icon.strip()))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print(f"Error adding category: A category with the name '{name}' already exists.")
        return False
    except sqlite3.Error as e:
        print(f"Database error adding category: {str(e)}")
        return False
    except ValueError as ve:
        print(f"Value error adding category: {str(ve)}")
        return False
    finally:
        conn.close()

def get_categories():
    """
    Retrieve all categories from the database.
    Returns:
        list: A list of category dictionaries with id, name, and icon.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, name, icon
            FROM Category
            ORDER BY name ASC
        ''')
        return [dict(row) for row in cursor.fetchall()]  # Convert rows to dictionaries
    except sqlite3.Error as e:
        print(f"Database error retrieving categories: {str(e)}")
        return []
    finally:
        conn.close()