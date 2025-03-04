import customtkinter as ctk
from tkinter import messagebox
from services.budget_service import add_budget, get_budgets, update_budget, delete_budget


class BudgetWindow:
    def __init__(self, user_id):
        """
        Initializes the budget management window.
        """
        self.user_id = user_id

        # Create a new top-level window for budget management
        self.root = ctk.CTkToplevel()
        self.root.title("Budget Management")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # Configure grid layout for responsiveness
        self.root.grid_rowconfigure(5, weight=1)  # Make the budget list expandable
        self.root.grid_columnconfigure((0, 1), weight=1)

        # Budget Form Section
        form_frame = ctk.CTkFrame(self.root, corner_radius=8, fg_color="#2B2B2B")
        form_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

        ctk.CTkLabel(
            form_frame,
            text="Add New Budget",
            font=("Arial", 18, "bold"),
            text_color="white"
        ).grid(row=0, column=0, columnspan=2, pady=(20, 10), padx=10, sticky="w")

        # Category Dropdown
        ctk.CTkLabel(form_frame, text="Category:", font=("Arial", 14), text_color="white").grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )
        self.combo_category = ctk.CTkOptionMenu(
            form_frame,
            values=["Food", "Transport", "Entertainment", "Other"],
            font=("Arial", 14),
            corner_radius=8,
            dropdown_fg_color="#3B3B3B",
            button_color="#4A4A4A",
            button_hover_color="#333333"
        )
        self.combo_category.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Amount Input
        ctk.CTkLabel(form_frame, text="Amount:", font=("Arial", 14), text_color="white").grid(
            row=2, column=0, padx=10, pady=5, sticky="w"
        )
        self.entry_amount = ctk.CTkEntry(
            form_frame,
            font=("Arial", 14),
            corner_radius=8,
            width=200
        )
        self.entry_amount.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Start Date Input
        ctk.CTkLabel(form_frame, text="Start Date (YYYY-MM-DD):", font=("Arial", 14), text_color="white").grid(
            row=3, column=0, padx=10, pady=5, sticky="w"
        )
        self.entry_start_date = ctk.CTkEntry(
            form_frame,
            font=("Arial", 14),
            corner_radius=8,
            width=200
        )
        self.entry_start_date.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # End Date Input
        ctk.CTkLabel(form_frame, text="End Date (YYYY-MM-DD):", font=("Arial", 14), text_color="white").grid(
            row=4, column=0, padx=10, pady=5, sticky="w"
        )
        self.entry_end_date = ctk.CTkEntry(
            form_frame,
            font=("Arial", 14),
            corner_radius=8,
            width=200
        )
        self.entry_end_date.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # Add Budget Button
        ctk.CTkButton(
            form_frame,
            text="➕ Add Budget",
            font=("Arial", 14),
            command=self.add_budget,
            fg_color="#2E8B57",
            hover_color="#3CB371",
            corner_radius=8
        ).grid(row=5, column=0, columnspan=2, pady=10)

        # Budget List Section
        list_frame = ctk.CTkFrame(self.root, corner_radius=8, fg_color="#3B3B3B")
        list_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

        # Budget Treeview
        columns = ("ID", "Category", "Amount", "Start Date", "End Date")
        self.tree = ctk.CTkTreeview(
            list_frame,
            columns=columns,
            show="headings",
            height=20
        )
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Load existing budgets
        self.load_budgets()

        # CRUD Buttons for Budgets
        button_frame = ctk.CTkFrame(self.root, corner_radius=8, fg_color="#3B3B3B")
        button_frame.grid(row=6, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        ctk.CTkButton(
            button_frame,
            text="📝 Edit Budget",
            font=("Arial", 14),
            command=self.edit_budget,
            fg_color="#FFA500",
            hover_color="#FF8C00",
            corner_radius=8
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="🗑️ Delete Budget",
            font=("Arial", 14),
            command=self.delete_budget,
            fg_color="#FF4500",
            hover_color="#FF0000",
            corner_radius=8
        ).pack(side="left", padx=5)

    def add_budget(self):
        """Add a new budget to the database and refresh the list."""
        category = self.combo_category.get().strip()
        amount = self.entry_amount.get().strip()
        start_date = self.entry_start_date.get().strip()
        end_date = self.entry_end_date.get().strip()

        # Validate inputs
        if not category:
            messagebox.showwarning("Input Error", "❌ Please select a category.")
            return
        if not amount or not amount.replace('.', '', 1).isdigit():
            messagebox.showwarning("Input Error", "❌ Please enter a valid amount (numeric value).")
            return
        if not start_date or not end_date:
            messagebox.showwarning("Input Error", "❌ Please enter both start and end dates in YYYY-MM-DD format.")
            return
        try:
            # Convert amount to float
            amount = float(amount)
            # Add the budget to the database
            if add_budget(self.user_id, category, amount, start_date, end_date):
                messagebox.showinfo("Success", "✅ Budget added successfully!")
                self.clear_form()  # Clear the form after successful addition
                self.load_budgets()  # Refresh the budget list
            else:
                messagebox.showerror("Error", "❌ Failed to add budget.")
        except Exception as e:
            messagebox.showerror("Error", f"❌ An error occurred: {str(e)}")

    def load_budgets(self):
        """Load and display all budgets for the current user."""
        for row in self.tree.get_children():
            self.tree.delete(row)  # Clear the existing rows

        budgets = get_budgets(self.user_id)
        for budget in budgets:
            self.tree.insert("", "end", values=(
                budget["id"],
                budget["category"],
                budget["amount"],
                budget["start_date"],
                budget["end_date"]
            ))

    def clear_form(self):
        """Clear the input fields in the budget form."""
        self.combo_category.set("")
        self.entry_amount.delete(0, ctk.END)
        self.entry_start_date.delete(0, ctk.END)
        self.entry_end_date.delete(0, ctk.END)

    def edit_budget(self):
        """Edit an existing budget."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "❌ Please select a budget to edit.")
            return

        item = self.tree.item(selected_item)
        budget_id = item["values"][0]

        # Open a dialog to edit the budget
        category = askstring("Edit Budget", "Enter new category:")
        if not category:
            return

        amount = self._get_numeric_input("Enter new amount:", "Edit Budget")
        if amount is None:
            return

        start_date = askstring("Edit Budget", "Enter new start date (YYYY-MM-DD):")
        if not start_date:
            return

        end_date = askstring("Edit Budget", "Enter new end date (YYYY-MM-DD):")
        if not end_date:
            return

        try:
            if update_budget(budget_id, category, float(amount), start_date, end_date):
                messagebox.showinfo("Success", "✅ Budget updated successfully!")
                self.load_budgets()  # Refresh the budget list
            else:
                messagebox.showerror("Error", "❌ Failed to update budget.")
        except Exception as e:
            messagebox.showerror("Error", f"❌ An error occurred: {str(e)}")

    def delete_budget(self):
        """Delete an existing budget."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "❌ Please select a budget to delete.")
            return

        item = self.tree.item(selected_item)
        budget_id = item["values"][0]

        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this budget?")
        if confirm:
            try:
                if delete_budget(budget_id):
                    messagebox.showinfo("Success", "✅ Budget deleted successfully!")
                    self.load_budgets()  # Refresh the budget list
                else:
                    messagebox.showerror("Error", "❌ Failed to delete budget.")
            except Exception as e:
                messagebox.showerror("Error", f"❌ An error occurred: {str(e)}")

    def _get_numeric_input(self, prompt, title):
        """Helper method to get numeric input from the user."""
        value = askstring(title, prompt)
        if not value or not value.replace('.', '', 1).isdigit():
            messagebox.showerror("Error", "❌ Invalid input. Please enter a valid number.")
            return None
        return value


# Example usage (for testing purposes)
if __name__ == "__main__":
    app = ctk.CTk()
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    budget_window = BudgetWindow(user_id=1)
    app.mainloop()