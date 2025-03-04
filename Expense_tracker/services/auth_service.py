import sqlite3
from pathlib import Path
import logging

# Import the get_db_connection function from the database module
from database.db import get_db_connection

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class AuthService:
    def __init__(self):
        """
        Initializes the AuthService.
        """
        pass

    def register_user(self, username, email, password, user_type="USER"):
        """
        Registers a new user in the database.
        Args:
            username (str): The username of the new user.
            email (str): The email of the new user.
            password (str): The password of the new user.
            user_type (str): The type of the user ('USER' or 'ADMIN'). Defaults to 'USER'.
        Returns:
            bool: True if the user was registered successfully, False otherwise.
        """
        try:
            # Basic validation
            if not username or not email or not password:
                logging.warning("Registration failed: All fields are required.")
                return False

            if len(password) < 6:
                logging.warning("Registration failed: Password must be at least 6 characters long.")
                return False

            if "@" not in email:  # Basic email validation
                logging.warning("Registration failed: Invalid email format.")
                return False

            if user_type not in ['USER', 'ADMIN']:
                logging.warning("Registration failed: Invalid user type.")
                return False

            conn = get_db_connection()
            cursor = conn.cursor()

            # Check if the username or email already exists
            cursor.execute("SELECT id FROM User WHERE username = ? OR email = ?", (username, email))
            if cursor.fetchone():
                logging.info(f"Registration failed: Username '{username}' or email '{email}' already exists.")
                return False

            # Insert the new user into the database
            cursor.execute('''
                INSERT INTO User (username, email, password, user_type, is_staff, is_superuser)
                VALUES (?, ?, ?, ?, 0, 0)
            ''', (username, email, password, user_type))

            conn.commit()
            logging.info(f"User '{username}' registered successfully with user type '{user_type}'.")
            return True
        except sqlite3.IntegrityError as ie:
            logging.error(f"Database integrity error during registration: {ie}")
            return False
        except sqlite3.Error as e:
            logging.error(f"Database error during registration: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def login_user(self, username, password):
        """
        Authenticates a user based on their credentials.
        Args:
            username (str): The username entered by the user.
            password (str): The password entered by the user.
        Returns:
            dict: A dictionary containing user details if login is successful.
            None: If login fails.
        """
        try:
            conn = get_db_connection()
            conn.row_factory = sqlite3.Row  # Enable accessing columns by name
            cursor = conn.cursor()

            # Query the database for the user with matching credentials
            cursor.execute("SELECT id, username, email, user_type FROM User WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()

            if user:
                logging.info(f"User '{username}' logged in successfully.")
                return dict(user)  # Convert Row object to dictionary
            else:
                logging.info(f"Login failed: Invalid credentials for username '{username}'.")
                return None
        except sqlite3.Error as e:
            logging.error(f"Database error during login: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def reset_password(self, username, email, new_password):
        """
        Resets the password for a user.
        Args:
            username (str): The username of the user.
            email (str): The email of the user.
            new_password (str): The new password to set.
        Returns:
            bool: True if the password was reset successfully, False otherwise.
        """
        try:
            if not username or not email or not new_password:
                logging.warning("Password reset failed: All fields are required.")
                return False

            if len(new_password) < 6:
                logging.warning("Password reset failed: New password must be at least 6 characters long.")
                return False

            if "@" not in email:  # Basic email validation
                logging.warning("Password reset failed: Invalid email format.")
                return False

            conn = get_db_connection()
            cursor = conn.cursor()

            # Validate the user's existence
            cursor.execute("SELECT id FROM User WHERE username = ? AND email = ?", (username, email))
            if not cursor.fetchone():
                logging.info(f"Password reset failed: No user found with username '{username}' and email '{email}'.")
                return False

            # Update the password
            cursor.execute("UPDATE User SET password = ? WHERE username = ? AND email = ?", (new_password, username, email))
            conn.commit()
            logging.info(f"Password for user '{username}' reset successfully.")
            return True
        except sqlite3.Error as e:
            logging.error(f"Database error during password reset: {e}")
            return False
        finally:
            if conn:
                conn.close()


# Export the functions for use in the AuthWindow
auth_service_instance = AuthService()


def register_user(username, email, password, user_type="USER"):
    return auth_service_instance.register_user(username, email, password, user_type)


def login_user(username, password):
    return auth_service_instance.login_user(username, password)


def reset_password(username, email, new_password):
    return auth_service_instance.reset_password(username, email, new_password)