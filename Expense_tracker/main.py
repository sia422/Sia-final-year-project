import customtkinter as ctk
from gui.auth_window import AuthWindow
from gui.splash_screen import SplashScreen


def open_auth_window():
    """
    Opens the authentication window.
    """
    root = ctk.CTk()
    root.geometry("800x600")  # ✅ Set window size properly
    auth_window = AuthWindow(root, on_login_success)
    root.mainloop()


def on_login_success(user):
    """
    Callback function after successful login.
    """
    if "id" not in user or "username" not in user:
        raise ValueError("User object must contain 'id' and 'username' keys.")

    root = ctk.CTk()
    root.geometry("1200x800")  # ✅ Set window size correctly
    
    from gui.user_dashboard import UserDashboard
    UserDashboard(root, user["id"], user["username"])
    
    root.mainloop()  # ✅ Removed incorrect arguments


if __name__ == "__main__":
    # Main application configuration
    app = ctk.CTk()
    app.geometry("1200x800")
    app.title("Daily Income & Expenses Tracker Management System")
    app.minsize(400, 300)  # ✅ Corrected minimum window size

    # Set custom theme
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    # Create and show splash screen
    splash_root = ctk.CTk()
    splash_root.geometry("1200x600")
    splash_root.title("Daily Income & Expense Tracker Management System")
    splash_root.minsize(400, 300)
    splash_root.resizable(False, False)

    splash = SplashScreen(splash_root, open_auth_window)
    splash.pack(fill="both", expand=True)

    splash_root.mainloop()
