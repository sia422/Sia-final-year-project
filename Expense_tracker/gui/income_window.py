import customtkinter as ctk
from tkinter import ttk, messagebox
from services.income_service import add_income, get_incomes

class IncomeWindow:
    def __init__(self, user_id):
        self.user_id = user_id
        # Create a new top-level window for income management
        self.root = ctk.CTkToplevel()
        self.root.title("Income Management")
        self.root.geometry("600x400")

        # Income Form
        ctk.CTkLabel(self.root, text="Source:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.combo_source = ttk.Combobox(self.root, values=["Salary", "Freelance", "Investment", "Rental", "Other"])
        self.combo_source.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(self.root, text="Amount:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_amount = ctk.CTkEntry(self.root)
        self.entry_amount.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(self.root, text="Date (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_date = ctk.CTkEntry(self.root)
        self.entry_date.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        
        ctk.CTkButton(self.root, text="Add Income", command=self.add_income).grid(
            row=4, column=0, columnspan=2, pady=10
        )

        # Income List
        self.tree = ttk.Treeview(
            self.root, columns=("Source", "Amount", "Date"), show="headings"
        )
        self.tree.heading("Source", text="Source")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Date", text="Date")
        self.tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        # Load existing incomes
        self.load_incomes()

    def add_income(self):
        """Add a new income to the database and refresh the list."""
        source = self.combo_source.get().strip()
        amount = self.entry_amount.get().strip()
        date = self.entry_date.get().strip()
        

        if not source:
            messagebox.showwarning("Input Error", "Please select an income source.")
            return
        if not amount or not amount.replace('.', '', 1).isdigit():
            messagebox.showwarning("Input Error", "Please enter a valid amount (numeric value).")
            return
        if not date:
            messagebox.showwarning("Input Error", "Please enter a valid date in YYYY-MM-DD format.")
            return

        try:
            amount = float(amount)
            if add_income(self.user_id, source, amount, date):
                messagebox.showinfo("Success", "Income added successfully!")
                self.clear_form()
                self.load_incomes()
            else:
                messagebox.showerror("Error", "Failed to add income.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def load_incomes(self):
        """Load and display all incomes for the current user."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        incomes = get_incomes(self.user_id)
        for income in incomes:
            self.tree.insert("", "end", values=(income["source"], income["amount"], income["date"]))

    def clear_form(self):
        """Clear the input fields in the income form."""
        self.combo_source.set("")
        self.entry_amount.delete(0, ctk.END)
        self.entry_date.delete(0, ctk.END)
      