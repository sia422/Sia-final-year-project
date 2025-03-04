import customtkinter as ctk
from tkinter import ttk, messagebox
from services.category_service import add_category, get_categories

class CategoryWindow:
    def __init__(self):
        # Create a new top-level window for category management
        self.root = ctk.CTkToplevel()
        self.root.title("Category Management")
        self.root.geometry("600x400")

        # Category Form
        ctk.CTkLabel(self.root, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_name = ctk.CTkEntry(self.root)
        self.entry_name.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(self.root, text="Icon:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_icon = ctk.CTkEntry(self.root)
        self.entry_icon.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        ctk.CTkButton(self.root, text="Add Category", command=self.add_category).grid(
            row=2, column=0, columnspan=2, pady=10
        )

        # Category List
        self.tree = ttk.Treeview(
            self.root, columns=("Name", "Icon"), show="headings"
        )
        self.tree.heading("Name", text="Name")
        self.tree.heading("Icon", text="Icon")
        self.tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Load existing categories
        self.load_categories()

    def add_category(self):
        """Add a new category to the database and refresh the list."""
        name = self.entry_name.get().strip()
        icon = self.entry_icon.get().strip()

        # Validate inputs
        if not name:
            messagebox.showwarning("Input Error", "Please enter a category name.")
            return

        try:
            # Add the category to the database
            if add_category(name, icon):
                messagebox.showinfo("Success", "Category added successfully!")
                self.clear_form()  # Clear the form after successful addition
                self.load_categories()  # Refresh the category list
            else:
                messagebox.showerror("Error", "Failed to add category.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def load_categories(self):
        """Load and display all categories."""
        for row in self.tree.get_children():
            self.tree.delete(row)  # Clear the existing rows

        categories = get_categories()
        for category in categories:
            self.tree.insert("", "end", values=(category["name"], category["icon"]))

    def clear_form(self):
        """Clear the input fields in the category form."""
        self.entry_name.delete(0, ctk.END)
        self.entry_icon.delete(0, ctk.END)