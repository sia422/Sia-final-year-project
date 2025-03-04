import customtkinter as ctk
from tkinter import messagebox
from services.auth_service import register_user, login_user, reset_password


class AuthWindow:
    def __init__(self, root, on_login_success):
        """
        Initializes the authentication window with a professional and unique design.
        """
        self.root = root
        self.on_login_success = on_login_success

        # Configure appearance mode (Dark by default)
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Set up the main window properties
        self.root.title("Income & Expense Tracker - Authentication")
        self.root.geometry("400x500")  # Compact size
        self.root.resizable(True, True)

        # Create frames for login, registration, and password reset
        self.login_frame = ctk.CTkFrame(self.root, corner_radius=8, fg_color="#2B2B2B")
        self.register_frame = ctk.CTkFrame(self.root, corner_radius=8, fg_color="#2B2B2B")
        self.reset_password_frame = ctk.CTkFrame(self.root, corner_radius=8, fg_color="#2B2B2B")

        # Initialize the frames
        self.setup_login_frame()
        self.setup_register_frame()
        self.setup_reset_password_frame()

        # Show the login frame by default
        self.show_login_frame()

    def toggle_theme(self):
        """
        Toggles between dark and light themes based on the switch state.
        """
        if self.theme_switch.get() == 1:  # Light mode
            ctk.set_appearance_mode("Light")
            self.theme_switch.configure(text="Dark Mode")
        else:  # Dark mode
            ctk.set_appearance_mode("Dark")
            self.theme_switch.configure(text="Light Mode")

    def setup_login_frame(self):
        """
        Sets up the login frame.
        """
        # Title label
        title_label = ctk.CTkLabel(
            self.login_frame,
            text="🔒 Income & Expense Tracker",
            font=("Arial", 24, "bold"),
            justify="center",
            text_color=("black", "white")  # Adjusts color for both modes
        )
        title_label.pack(pady=(20, 10))

        # Username input
        username_label = ctk.CTkLabel(
            self.login_frame,
            text="👤 Username:",
            font=("Arial", 16),
            text_color=("gray30", "gray70")  # Adjusts color for both modes
        )
        username_label.pack(pady=(10, 5))
        self.entry_username = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Enter your username",
            font=("Arial", 14),
            corner_radius=8,
            width=250
        )
        self.entry_username.pack(pady=5)

        # Password input
        password_label = ctk.CTkLabel(
            self.login_frame,
            text="🔑 Password:",
            font=("Arial", 16),
            text_color=("gray30", "gray70")  # Adjusts color for both modes
        )
        password_label.pack(pady=(10, 5))
        self.entry_password = ctk.CTkEntry(
            self.login_frame,
            show="*",
            placeholder_text="Enter your password",
            font=("Arial", 14),
            corner_radius=8,
            width=250
        )
        self.entry_password.pack(pady=5)

        # Login button
        login_button = ctk.CTkButton(
            self.login_frame,
            text="Login 🚪",
            font=("Arial", 16, "bold"),
            command=self.login,
            fg_color="#2E8B57",
            hover_color="#3CB371",
            corner_radius=8,
            width=200
        )
        login_button.pack(pady=20)

        # Forgot Password link
        forgot_password_link = ctk.CTkButton(
            self.login_frame,
            text="Forgot Password? 🔑",
            font=("Arial", 14, "italic"),
            command=self.show_reset_password_frame,
            fg_color="transparent",
            text_color="#FF4500",
            hover_color="#FF8C00",
            corner_radius=8
        )
        forgot_password_link.pack(pady=10)

        # Switch to Register link
        register_link = ctk.CTkButton(
            self.login_frame,
            text="Not a member? Register ✍️",
            font=("Arial", 14, "italic"),
            command=self.show_register_frame,
            fg_color="transparent",
            text_color="#4682B4",
            hover_color="#5F9EA0",
            corner_radius=8
        )
        register_link.pack(pady=10)

        # Footer label
        footer_label = ctk.CTkLabel(
            self.login_frame,
            text="© 2025 Income & Expense Tracker. All rights reserved.",
            font=("Arial", 10),
            text_color=("gray30", "gray70")  # Adjusts color for both modes
        )
        footer_label.pack(pady=(20, 10))

    def setup_register_frame(self):
        """
        Sets up the registration frame.
        """
        # Title label
        title_label = ctk.CTkLabel(
            self.register_frame,
            text="✍️ Create an Account",
            font=("Arial", 24, "bold"),
            justify="center",
            text_color=("black", "white")  # Adjusts color for both modes
        )
        title_label.pack(pady=20)

        # Username input
        username_label = ctk.CTkLabel(
            self.register_frame,
            text="👤 Username:",
            font=("Arial", 16),
            text_color=("gray30", "gray70")  # Adjusts color for both modes
        )
        username_label.pack(pady=(10, 5))
        self.register_entry_username = ctk.CTkEntry(
            self.register_frame,
            placeholder_text="Enter your username",
            font=("Arial", 14),
            corner_radius=8,
            width=250
        )
        self.register_entry_username.pack(pady=5)

        # Email input
        email_label = ctk.CTkLabel(
            self.register_frame,
            text="📧 Email:",
            font=("Arial", 16),
            text_color=("gray30", "gray70")  # Adjusts color for both modes
        )
        email_label.pack(pady=(10, 5))
        self.register_entry_email = ctk.CTkEntry(
            self.register_frame,
            placeholder_text="Enter your email",
            font=("Arial", 14),
            corner_radius=8,
            width=250
        )
        self.register_entry_email.pack(pady=5)

        # Password input
        password_label = ctk.CTkLabel(
            self.register_frame,
            text="🔑 Password:",
            font=("Arial", 16),
            text_color=("gray30", "gray70")  # Adjusts color for both modes
        )
        password_label.pack(pady=(10, 5))
        self.register_entry_password = ctk.CTkEntry(
            self.register_frame,
            show="*",
            placeholder_text="Enter your password",
            font=("Arial", 14),
            corner_radius=8,
            width=250
        )
        self.register_entry_password.pack(pady=5)

        # Register button
        register_button = ctk.CTkButton(
            self.register_frame,
            text="Register ✅",
            font=("Arial", 16, "bold"),
            command=self.register,
            fg_color="#4682B4",
            hover_color="#5F9EA0",
            corner_radius=8,
            width=200
        )
        register_button.pack(pady=20)

        # Switch to Login link
        login_link = ctk.CTkButton(
            self.register_frame,
            text="Already a member? Login 🚪",
            font=("Arial", 14, "italic"),
            command=self.show_login_frame,
            fg_color="transparent",
            text_color="#2E8B57",
            hover_color="#3CB371",
            corner_radius=8
        )
        login_link.pack(pady=10)

        # Footer label
        footer_label = ctk.CTkLabel(
            self.register_frame,
            text="© 2025 Income & Expense Tracker. All rights reserved.",
            font=("Arial", 10),
            text_color=("gray30", "gray70")  # Adjusts color for both modes
        )
        footer_label.pack(pady=(20, 10))

    def setup_reset_password_frame(self):
        """
        Sets up the password reset frame.
        """
        # Title label
        title_label = ctk.CTkLabel(
            self.reset_password_frame,
            text="🔑 Reset Your Password",
            font=("Arial", 24, "bold"),
            justify="center",
            text_color=("black", "white")  # Adjusts color for both modes
        )
        title_label.pack(pady=20)

        # Username input
        username_label = ctk.CTkLabel(
            self.reset_password_frame,
            text="👤 Username:",
            font=("Arial", 16),
            text_color=("gray30", "gray70")  # Adjusts color for both modes
        )
        username_label.pack(pady=(10, 5))
        self.reset_entry_username = ctk.CTkEntry(
            self.reset_password_frame,
            placeholder_text="Enter your username",
            font=("Arial", 14),
            corner_radius=8,
            width=250
        )
        self.reset_entry_username.pack(pady=5)

        # Email input (optional)
        email_label = ctk.CTkLabel(
            self.reset_password_frame,
            text="📧 Email:",
            font=("Arial", 16),
            text_color=("gray30", "gray70")  # Adjusts color for both modes
        )
        email_label.pack(pady=(10, 5))
        self.reset_entry_email = ctk.CTkEntry(
            self.reset_password_frame,
            placeholder_text="Enter your email",
            font=("Arial", 14),
            corner_radius=8,
            width=250
        )
        self.reset_entry_email.pack(pady=5)

        # New Password input
        new_password_label = ctk.CTkLabel(
            self.reset_password_frame,
            text="🔐 New Password:",
            font=("Arial", 16),
            text_color=("gray30", "gray70")  # Adjusts color for both modes
        )
        new_password_label.pack(pady=(10, 5))
        self.reset_entry_new_password = ctk.CTkEntry(
            self.reset_password_frame,
            show="*",
            placeholder_text="Enter your new password",
            font=("Arial", 14),
            corner_radius=8,
            width=250
        )
        self.reset_entry_new_password.pack(pady=5)

        # Reset Password button
        reset_password_button = ctk.CTkButton(
            self.reset_password_frame,
            text="Reset Password ✅",
            font=("Arial", 16, "bold"),
            command=self.reset_password,
            fg_color="#FF4500",
            hover_color="#FF8C00",
            corner_radius=8,
            width=200
        )
        reset_password_button.pack(pady=20)

        # Back to Login link
        back_to_login_link = ctk.CTkButton(
            self.reset_password_frame,
            text="Back to Login 🚪",
            font=("Arial", 14, "italic"),
            command=self.show_login_frame,
            fg_color="transparent",
            text_color="#2E8B57",
            hover_color="#3CB371",
            corner_radius=8
        )
        back_to_login_link.pack(pady=10)

        # Footer label
        footer_label = ctk.CTkLabel(
            self.reset_password_frame,
            text="© 2025 Income & Expense Tracker. All rights reserved.",
            font=("Arial", 10),
            text_color=("gray30", "gray70")  # Adjusts color for both modes
        )
        footer_label.pack(pady=(20, 10))

    def show_login_frame(self):
        """
        Displays the login frame.
        """
        self.register_frame.pack_forget()
        self.reset_password_frame.pack_forget()
        self.login_frame.pack(fill="both", expand=True)

    def show_register_frame(self):
        """
        Displays the registration frame.
        """
        self.login_frame.pack_forget()
        self.reset_password_frame.pack_forget()
        self.register_frame.pack(fill="both", expand=True)

    def show_reset_password_frame(self):
        """
        Displays the password reset frame.
        """
        self.login_frame.pack_forget()
        self.register_frame.pack_forget()
        self.reset_password_frame.pack(fill="both", expand=True)

    def login(self):
        """
        Handles the login process by validating user credentials.
        """
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if not username or not password:
            messagebox.showwarning("Input Error", "❌ Please enter both username and password.")
            return

        user = login_user(username, password)
        if user:
            self.root.destroy()
            self.on_login_success(user)
        else:
            messagebox.showerror("Login Failed", "❌ Invalid username or password.")

    def register(self):
        """
        Handles the registration process by creating a new user account.
        """
        username = self.register_entry_username.get().strip()
        password = self.register_entry_password.get().strip()
        email = self.register_entry_email.get().strip()

        if not username or not password:
            messagebox.showwarning("Input Error", "❌ Please enter both username and password.")
            return

        if len(password) < 6:
            messagebox.showwarning("Password Too Short", "❌ Password must be at least 6 characters long.")
            return

        if email and "@" not in email:  # Basic email validation
            messagebox.showwarning("Invalid Email", "❌ Please enter a valid email address.")
            return

        success = register_user(username, email, password)
        if success:
            messagebox.showinfo("Success", "✅ User registered successfully! Please log in.")
            self.show_login_frame()
        else:
            messagebox.showerror("Registration Failed", "❌ Username already exists.")

    def reset_password(self):
        """
        Handles the password reset process.
        """
        username = self.reset_entry_username.get().strip()
        email = self.reset_entry_email.get().strip()
        new_password = self.reset_entry_new_password.get().strip()

        if not username or not new_password:
            messagebox.showwarning("Input Error", "❌ Please enter your username and new password.")
            return

        if len(new_password) < 6:
            messagebox.showwarning("Password Too Short", "❌ New password must be at least 6 characters long.")
            return

        if email and "@" not in email:  # Basic email validation
            messagebox.showwarning("Invalid Email", "❌ Please enter a valid email address.")
            return

        success = reset_password(username, email, new_password)
        if success:
            messagebox.showinfo("Success", "✅ Password reset successfully! Please log in.")
            self.show_login_frame()
        else:
            messagebox.showerror("Reset Failed", "❌ Failed to reset password. Please check your details.")

# Example usage (for testing purposes)
if __name__ == "__main__":
    def on_login_success(user):
        print(f"Logged in as {user}")

    app = ctk.CTk()
    auth_window = AuthWindow(app, on_login_success)
    app.mainloop()