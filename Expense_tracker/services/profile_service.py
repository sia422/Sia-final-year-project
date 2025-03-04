import sqlite3
from database.db import get_db_connection

def update_profile(user_id, currency, income, theme):
    """
    Update the user's profile in the database.

    Args:
        user_id (int): The ID of the user.
        currency (str): The default currency preference.
        income (float): The monthly income of the user.
        theme (str): The theme preference ('light' or 'dark').

    Returns:
        bool: True if the profile was updated successfully, False otherwise.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Validate inputs
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("User ID must be a positive integer.")
        if not isinstance(currency, str) or not currency.strip():
            raise ValueError("Currency must be a non-empty string.")
        if income is not None and not isinstance(income, (int, float)):
            raise ValueError("Income must be a number or None.")
        if not isinstance(theme, str) or theme.strip() not in ["light", "dark"]:
            raise ValueError("Theme must be either 'light' or 'dark'.")

        # Update the user's profile in the database
        cursor.execute('''
            UPDATE UserProfile
            SET default_currency = ?, monthly_income = ?, theme_preference = ?
            WHERE user_id = ?
        ''', (currency.strip(), income, theme.strip(), user_id))
        conn.commit()

        # Check if any rows were affected
        if cursor.rowcount == 0:
            print(f"No profile found for user ID {user_id}.")
            return False

        return True
    except sqlite3.IntegrityError as ie:
        print(f"Integrity error updating profile: {ie}")
        return False
    except sqlite3.Error as e:
        print(f"Database error updating profile: {e}")
        return False
    except ValueError as ve:
        print(f"Value error updating profile: {ve}")
        return False
    finally:
        conn.close()

def get_profile(user_id):
    """
    Retrieve the user's profile from the database.

    Args:
        user_id (int): The ID of the user.

    Returns:
        dict: A dictionary containing the user's profile details, or None if no profile exists.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Validate input
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("User ID must be a positive integer.")

        # Query the database for the user's profile
        cursor.execute('''
            SELECT id, user_id, default_currency, monthly_income, theme_preference
            FROM UserProfile
            WHERE user_id = ?
        ''', (user_id,))
        row = cursor.fetchone()

        # Convert the row to a dictionary if it exists
        if row:
            return {
                "id": row[0],
                "user_id": row[1],
                "default_currency": row[2],
                "monthly_income": row[3],
                "theme_preference": row[4],
            }
        else:
            print(f"No profile found for user ID {user_id}.")
            return None
    except sqlite3.Error as e:
        print(f"Database error retrieving profile: {e}")
        return None
    except ValueError as ve:
        print(f"Value error retrieving profile: {ve}")
        return None
    finally:
        conn.close()