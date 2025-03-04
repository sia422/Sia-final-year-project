import sqlite3
from database.db import get_db_connection

def get_monthly_report(user_id, month, year):
    """
    Retrieve the monthly report for a user, including expenses and incomes.

    Args:
        user_id (int): The ID of the user.
        month (int): The month for which the report is generated (1-12).
        year (int): The year for which the report is generated.

    Returns:
        tuple: A tuple containing two lists:
               - A list of expense dictionaries.
               - A list of income dictionaries.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Validate inputs
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("User ID must be a positive integer.")
        if not isinstance(month, int) or month < 1 or month > 12:
            raise ValueError("Month must be an integer between 1 and 12.")
        if not isinstance(year, int) or year < 1000 or year > 9999:
            raise ValueError("Year must be a valid 4-digit integer.")

        # Query expenses for the given month and year
        cursor.execute('''
            SELECT id, user_id, title, amount, currency, category_id, date, description
            FROM Expense
            WHERE user_id = ? AND strftime('%m', date) = ? AND strftime('%Y', date) = ?
        ''', (user_id, f"{month:02d}", str(year)))
        expense_rows = cursor.fetchall()

        # Convert expense rows to a list of dictionaries
        expenses = [
            {
                "id": row[0],
                "user_id": row[1],
                "title": row[2],
                "amount": row[3],
                "currency": row[4],
                "category_id": row[5],
                "date": row[6],
                "description": row[7],
            }
            for row in expense_rows
        ]

        # Query incomes for the given month and year
        cursor.execute('''
            SELECT id, user_id, source, amount, date, description
            FROM Income
            WHERE user_id = ? AND strftime('%m', date) = ? AND strftime('%Y', date) = ?
        ''', (user_id, f"{month:02d}", str(year)))
        income_rows = cursor.fetchall()

        # Convert income rows to a list of dictionaries
        incomes = [
            {
                "id": row[0],
                "user_id": row[1],
                "source": row[2],
                "amount": row[3],
                "date": row[4],
                "description": row[5],
            }
            for row in income_rows
        ]

        return expenses, incomes
    except sqlite3.Error as e:
        print(f"Database error retrieving monthly report: {e}")
        return [], []
    except ValueError as ve:
        print(f"Value error retrieving monthly report: {ve}")
        return [], []
    finally:
        conn.close()