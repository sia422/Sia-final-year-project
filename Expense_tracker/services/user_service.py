import sqlite3
from database.db import get_db_connection

def get_all_users():
    """
    Retrieve all users from the User table.

    Returns:
        list: A list of user dictionaries, where each dictionary contains user details.
              If no users exist or an error occurs, an empty list is returned.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Query the database for all users
        cursor.execute('''
            SELECT id, username, email, user_type, is_staff, is_superuser
            FROM User
        ''')
        rows = cursor.fetchall()

        # Convert rows to a list of dictionaries
        users = [
            {
                "id": row[0],
                "username": row[1],
                "email": row[2],
                "user_type": row[3],
                "is_staff": bool(row[4]),
                "is_superuser": bool(row[5]),
            }
            for row in rows
        ]
        return users
    except sqlite3.Error as e:
        print(f"Database error retrieving users: {e}")
        return []
    finally:
        conn.close()