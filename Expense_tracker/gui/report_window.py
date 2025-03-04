import customtkinter as ctk
from tkinter import ttk, messagebox
from services.report_service import get_monthly_report
from gui.widgets import ExpenseChart

class ReportWindow:
    def __init__(self, user_id):
        self.user_id = user_id
        # Create a new top-level window for the report
        self.root = ctk.CTkToplevel()
        self.root.title("Monthly Report")
        self.root.geometry("800x600")

        # Report Form
        ctk.CTkLabel(self.root, text="Month:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_month = ctk.CTkEntry(self.root)
        self.entry_month.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(self.root, text="Year:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_year = ctk.CTkEntry(self.root)
        self.entry_year.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkButton(self.root, text="Generate Report", command=self.generate_report).grid(
            row=2, column=0, columnspan=2, pady=10
        )

        # Report Display
        self.tree = ttk.Treeview(
            self.root, columns=("Type", "Amount", "Date"), show="headings"
        )
        self.tree.heading("Type", text="Type")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Date", text="Date")
        self.tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Chart
        self.chart = ExpenseChart(self.root, [])
        self.chart.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def generate_report(self):
        """Generate and display the monthly report."""
        try:
            month = int(self.entry_month.get().strip())
            year = int(self.entry_year.get().strip())

            if month < 1 or month > 12:
                raise ValueError("Invalid month. Please enter a value between 1 and 12.")
            if year < 1000 or year > 9999:
                raise ValueError("Invalid year. Please enter a valid 4-digit year.")

            expenses, incomes = get_monthly_report(self.user_id, month, year)

            # Clear the treeview
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Add expenses and incomes to the treeview
            for expense in expenses:
                self.tree.insert("", "end", values=("Expense", expense["amount"], expense["date"]))
            for income in incomes:
                self.tree.insert("", "end", values=("Income", income["amount"], income["date"]))

            # Update the chart
            self.chart.update_chart(expenses + incomes)

            # Show summary message
            total_expenses = sum(float(expense["amount"]) for expense in expenses)
            total_incomes = sum(float(income["amount"]) for income in incomes)
            net_balance = total_incomes - total_expenses
            messagebox.showinfo(
                "Report Summary",
                f"Month: {month}\nYear: {year}\n\nTotal Expenses: {total_expenses:.2f}\n"
                f"Total Incomes: {total_incomes:.2f}\nNet Balance: {net_balance:.2f}",
            )
        except ValueError as ve:
            messagebox.showwarning("Input Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")