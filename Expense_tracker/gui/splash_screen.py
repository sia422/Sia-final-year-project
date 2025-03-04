import customtkinter as ctk
from tkinter import messagebox
import time

class SplashScreen(ctk.CTkFrame):
    def __init__(self, parent, switch_to_auth):
        super().__init__(parent)
        self.parent = parent
        self.switch_to_auth = switch_to_auth

        # Configure frame to be responsive
        self.configure(fg_color=("white", "#1a1a1a"))
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Main container
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.container.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Logo with animated effect
        self.logo_label = ctk.CTkLabel(
            self.container,
            text="💰",
            font=ctk.CTkFont(size=50),
            text_color="#2FA572"
        )
        self.logo_label.grid(row=0, column=0, pady=(40, 20))
        
        # App title
        self.title_label = ctk.CTkLabel(
            self.container,
            text="DAILY INCOME & EXPENSE TRACKER MANAGEMENT SYSTEM",
            font=ctk.CTkFont(family="Arial", size=24, weight="bold"),
            text_color=("#1a1a1a", "white")
        )
        self.title_label.grid(row=1, column=0, pady=10)

        # Tagline
        self.tagline_label = ctk.CTkLabel(
            self.container,
            text="Your Smart Money Management Solution",
            font=ctk.CTkFont(size=14),
            text_color=("gray40", "gray60")
        )
        self.tagline_label.grid(row=2, column=0, pady=5)

        # Get Started button with smooth transition
        self.get_started_btn = ctk.CTkButton(
            self.container,
            text="GET STARTED →",
            command=self.smooth_transition,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#2FA572",
            hover_color="#207244",
            corner_radius=20,
            border_width=2,
            border_color=("white", "#1a1a1a"),
            text_color="white"
        )
        self.get_started_btn.grid(row=3, column=0, pady=(20, 40), padx=20)

        # Version info
        self.version_label = ctk.CTkLabel(
            self.container,
            text="Version 1.0 · © 2025 Income & Expense Tracker",
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray70")
        )
        self.version_label.grid(row=4, column=0, pady=10)

        # Start fade-in animation
        self.fade_in()

    def fade_in(self):
        """Smooth fade-in animation."""
        for i in range(0, 11):
            self.update_idletasks()
            self.parent.attributes('-alpha', i / 10)
            time.sleep(0.05)

    def smooth_transition(self):
        """Smooth fade-out transition and switch to authentication."""
        for i in range(10, -1, -1):
            self.update_idletasks()
            self.parent.attributes('-alpha', i / 10)
            time.sleep(0.05)
        self.switch_to_auth()

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("400x500")
    root.attributes('-alpha', 0)  # Initially transparent
    
    def open_auth():
        messagebox.showinfo("Transition", "Switching to Auth Window")
    
    splash = SplashScreen(root, open_auth)
    splash.pack(fill="both", expand=True)
    root.mainloop()
