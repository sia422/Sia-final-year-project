import sqlite3
from database.db import get_db_connection


def add_income(user_id: int, source: str, amount: float, date: str) -> bool:
    """
    Adds a new income entry to the database.

    Args:
        user_id (int): The ID of the user.
        source (str): The source of the income.
        amount (float): The income amount.
        date (str): The date of the income (YYYY-MM-DD).

    Returns:
        bool: True if the income was added successfully, False otherwise.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Income (user_id, source, amount, date)
                VALUES (?, ?, ?, ?)
            """, (user_id, source, amount, date))
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(f"Database error adding income: {e}")
        return False


def get_incomes(user_id: int) -> list:
    """
    Retrieves all incomes for a specific user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        list: A list of income dictionaries.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, source, amount, date FROM Income WHERE user_id = ?", (user_id,))
            rows = cursor.fetchall()
            return [
                {
                    "id": row[0],
                    "source": row[1],
                    "amount": row[2],
                    "date": row[3],
                }
                for row in rows
            ]
    except sqlite3.Error as e:
        print(f"Database error retrieving incomes: {e}")
        return []


def get_total_income(user_id: int) -> float:
    """
    Calculates the total income for a specific user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        float: The total income amount.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM Income WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()[0]
            return float(result)
    except sqlite3.Error as e:
        print(f"Database error calculating total income: {e}")
        return 0.0


def update_income(income_id: int, source: str, amount: float, date: str) -> bool:
    """
    Updates an existing income entry in the database.

    Args:
        income_id (int): The ID of the income to update.
        source (str): The updated source of the income.
        amount (float): The updated income amount.
        date (str): The updated date of the income (YYYY-MM-DD).

    Returns:
        bool: True if the income was updated successfully, False otherwise.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Income SET source = ?, amount = ?, date = ?
                WHERE id = ?
            """, (source, amount, date, income_id))
            conn.commit()
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Database error updating income: {e}")
        return False


def delete_income(income_id: int) -> bool:
    """
    Deletes an existing income entry from the database.

    Args:
        income_id (int): The ID of the income to delete.

    Returns:
        bool: True if the income was deleted successfully, False otherwise.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Income WHERE id = ?", (income_id,))
            conn.commit()
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Database error deleting income: {e}")
        return False