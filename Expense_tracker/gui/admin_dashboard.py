import customtkinter as ctk
from tkinter import messagebox
from services.income_service import get_all_incomes, get_total_income
from services.expense_service import get_all_expenses, get_total_expenses
from services.user_service import get_all_users


class AdminDashboard:
    def __init__(self, root):
        """
        Initializes the admin dashboard with a professional and responsive design.
        """
        self.root = root
        self.root.title("Income & Expense Tracker - Admin Dashboard")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)

        # Configure appearance mode (Dark by default)
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Configure grid layout for responsiveness
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Sidebar (Fixed width)
        self.sidebar = ctk.CTkFrame(self.root, width=250, corner_radius=8, fg_color="#2B2B2B")
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Header in Sidebar
        ctk.CTkLabel(
            self.sidebar,
            text="Admin Panel",
            font=("Arial", 18, "bold"),
            text_color="white"
        ).pack(pady=(20, 10), padx=10)

        # Light/Dark Mode Toggle
        self.mode_toggle = ctk.CTkSwitch(
            self.sidebar,
            text="☀️ Light Mode",
            command=self.toggle_mode,
            font=("Arial", 14),
            onvalue="light",
            offvalue="dark"
        )
        self.mode_toggle.pack(pady=10, padx=10)

        # Sidebar Buttons with Font Awesome Icons
        buttons = [
            ("👥 View All Users", self.show_users),
            ("📈 View All Incomes", self.show_incomes),
            ("📉 View All Expenses", self.show_expenses),
            ("🚪 Logout", self.logout)
        ]
        for text, command in buttons:
            ctk.CTkButton(
                self.sidebar,
                text=text,
                font=("Arial", 14),
                corner_radius=8,
                command=command,
                fg_color="#4A4A4A",
                hover_color="#333333"
            ).pack(fill="x", padx=10, pady=5)

        # Main Content Area
        self.main_content = ctk.CTkFrame(self.root, corner_radius=8, fg_color="#2B2B2B")
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Load default view
        self.show_dashboard()

    def toggle_mode(self):
        """Toggle between light and dark modes."""
        mode = self.mode_toggle.get()
        ctk.set_appearance_mode("Light" if mode == "light" else "Dark")
        self.mode_toggle.configure(text="🌙 Dark Mode" if mode == "light" else "☀️ Light Mode")

    def show_dashboard(self):
        """Display the admin dashboard with analytics."""
        for widget in self.main_content.winfo_children():
            widget.destroy()

        # Fetch data
        total_incomes = get_total_income()
        total_expenses = get_total_expenses()
        all_users = get_all_users()

        # Dashboard Title
        ctk.CTkLabel(
            self.main_content,
            text="📊 Admin Dashboard Overview",
            font=("Arial", 20, "bold"),
            text_color="white"
        ).pack(pady=(20, 10))

        # Analytics Section
        analytics_frame = ctk.CTkFrame(self.main_content, corner_radius=8, fg_color="#3B3B3B")
        analytics_frame.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkLabel(
            analytics_frame,
            text=f"💰 Total Incomes: ${total_incomes:.2f}",
            font=("Arial", 16),
            text_color="white"
        ).pack(pady=10, padx=10)

        ctk.CTkLabel(
            analytics_frame,
            text=f"💸 Total Expenses: ${total_expenses:.2f}",
            font=("Arial", 16),
            text_color="white"
        ).pack(pady=10, padx=10)

        ctk.CTkLabel(
            analytics_frame,
            text=f"👥 Total Users: {len(all_users)}",
            font=("Arial", 16),
            text_color="white"
        ).pack(pady=10, padx=10)

    def show_users(self):
        """Display all users."""
        for widget in self.main_content.winfo_children():
            widget.destroy()

        users = get_all_users()
        if not users:
            ctk.CTkLabel(
                self.main_content,
                text="❌ No users found.",
                font=("Arial", 16),
                text_color="white"
            ).pack(pady=50)
            return

        treeview_frame = ctk.CTkFrame(self.main_content, corner_radius=8, fg_color="#3B3B3B")
        treeview_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("ID", "Username", "Email", "Registered On")
        self.tree = ctk.CTkTreeview(
            treeview_frame,
            columns=columns,
            show="headings",
            height=20
        )
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Populate the treeview
        for user in users:
            self.tree.insert("", "end", values=(
                user["id"],
                user["username"],
                user["email"],
                user["registered_on"]
            ))

    def show_incomes(self):
        """Display all incomes."""
        for widget in self.main_content.winfo_children():
            widget.destroy()

        incomes = get_all_incomes()
        if not incomes:
            ctk.CTkLabel(
                self.main_content,
                text="❌ No incomes found.",
                font=("Arial", 16),
                text_color="white"
            ).pack(pady=50)
            return

        treeview_frame = ctk.CTkFrame(self.main_content, corner_radius=8, fg_color="#3B3B3B")
        treeview_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("ID", "User ID", "Category", "Amount", "Date")
        self.tree = ctk.CTkTreeview(
            treeview_frame,
            columns=columns,
            show="headings",
            height=20
        )
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Populate the treeview
        for income in incomes:
            self.tree.insert("", "end", values=(
                income["id"],
                income["user_id"],
                income["category_name"],
                income["amount"],
                income["date"]
            ))

    def show_expenses(self):
        """Display all expenses."""
        for widget in self.main_content.winfo_children():
            widget.destroy()

        expenses = get_all_expenses()
        if not expenses:
            ctk.CTkLabel(
                self.main_content,
                text="❌ No expenses found.",
                font=("Arial", 16),
                text_color="white"
            ).pack(pady=50)
            return

        treeview_frame = ctk.CTkFrame(self.main_content, corner_radius=8, fg_color="#3B3B3B")
        treeview_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("ID", "User ID", "Category", "Amount", "Date")
        self.tree = ctk.CTkTreeview(
            treeview_frame,
            columns=columns,
            show="headings",
            height=20
        )
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Populate the treeview
        for expense in expenses:
            self.tree.insert("", "end", values=(
                expense["id"],
                expense["user_id"],
                expense["category_name"],
                expense["amount"],
                expense["date"]
            ))

    def logout(self):
        """Log out the admin and return to the authentication window."""
        self.root.destroy()
        from main import open_auth_window
        open_auth_window()


# Example usage (for testing purposes)
if __name__ == "__main__":
    app = ctk.CTk()
    dashboard = AdminDashboard(app)
    app.mainloop()