import tkinter as tk
from tkinter import ttk, messagebox
from services.expense_service import add_expense, get_expenses
from gui.widgets import ExpenseChart
from utils.exporters import export_to_csv

class MainWindow:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("Expense Tracker")
        self.root.geometry("800x600")  # Set a default window size

        # Expense Form
        tk.Label(root, text="Title:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_title = tk.Entry(root)
        self.entry_title.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(root, text="Amount:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_amount = tk.Entry(root)
        self.entry_amount.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(root, text="Currency:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.combo_currency = ttk.Combobox(root, values=["USD", "NLe", "EUR", "GBP"])
        self.combo_currency.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(root, text="Add Expense", command=self.add_expense).grid(
            row=3, column=0, columnspan=2, pady=10
        )

        # Expense List
        self.tree = ttk.Treeview(
            root, columns=("Title", "Amount", "Currency"), show="headings"
        )
        self.tree.heading("Title", text="Title")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Currency", text="Currency")
        self.tree.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Chart
        self.chart = ExpenseChart(root, get_expenses(self.user_id))
        self.chart.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        # Export Button
        tk.Button(root, text="Export to CSV", command=self.export_expenses).grid(
            row=6, column=0, columnspan=2, pady=10
        )

        # Load existing expenses
        self.load_expenses()

    def add_expense(self):
        """Add a new expense to the database and refresh the list."""
        title = self.entry_title.get().strip()
        amount = self.entry_amount.get().strip()
        currency = self.combo_currency.get().strip()

        # Validate inputs
        if not title:
            messagebox.showwarning("Input Error", "Please enter a title.")
            return
        if not amount or not amount.replace('.', '', 1).isdigit():
            messagebox.showwarning("Input Error", "Please enter a valid amount (numeric value).")
            return
        if not currency:
            messagebox.showwarning("Input Error", "Please select a currency.")
            return

        try:
            # Convert amount to float
            amount = float(amount)

            # Add the expense to the database
            if add_expense(self.user_id, title, amount, currency):
                messagebox.showinfo("Success", "Expense added successfully!")
                self.clear_form()  # Clear the form after successful addition
                self.load_expenses()  # Refresh the expense list and chart
            else:
                messagebox.showerror("Error", "Failed to add expense.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def load_expenses(self):
        """Load and display all expenses for the current user."""
        for row in self.tree.get_children():
            self.tree.delete(row)  # Clear the existing rows

        expenses = get_expenses(self.user_id)
        for expense in expenses:
            self.tree.insert("", "end", values=(expense["title"], expense["amount"], expense["currency"]))

        # Update the chart with the latest data
        self.chart.update_chart(expenses)

    def export_expenses(self):
        """Export expenses to a CSV file."""
        expenses = get_expenses(self.user_id)
        if not expenses:
            messagebox.showinfo("Info", "No expenses to export.")
            return

        if export_to_csv(expenses, "expenses.csv"):
            messagebox.showinfo("Success", "Expenses exported to expenses.csv")
        else:
            messagebox.showerror("Error", "Failed to export expenses.")

    def clear_form(self):
        """Clear the input fields in the expense form."""
        self.entry_title.delete(0, tk.END)
        self.entry_amount.delete(0, tk.END)
        self.combo_currency.set("")