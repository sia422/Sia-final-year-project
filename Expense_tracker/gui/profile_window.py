import customtkinter as ctk
from tkinter import messagebox
from services.profile_service import update_profile, get_profile

class ProfileWindow:
    def __init__(self, user_id):
        self.user_id = user_id
        # Create a new top-level window for profile management
        self.root = ctk.CTkToplevel()
        self.root.title("Profile Management")
        self.root.geometry("400x300")

        # Profile Form
        ctk.CTkLabel(self.root, text="Default Currency:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_currency = ctk.CTkEntry(self.root)
        self.entry_currency.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(self.root, text="Monthly Income:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_income = ctk.CTkEntry(self.root)
        self.entry_income.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(self.root, text="Theme Preference:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.combo_theme = ctk.CTkOptionMenu(self.root, values=["light", "dark"])
        self.combo_theme.grid(row=2, column=1, padx=10, pady=5)

        ctk.CTkButton(self.root, text="Update Profile", command=self.update_profile).grid(
            row=3, column=0, columnspan=2, pady=10
        )

        # Load existing profile data
        self.load_profile()

    def load_profile(self):
        """Load and display the user's profile data."""
        profile = get_profile(self.user_id)
        if profile:
            self.entry_currency.delete(0, ctk.END)
            self.entry_currency.insert(0, profile["default_currency"])

            self.entry_income.delete(0, ctk.END)
            if profile["monthly_income"] is not None:
                self.entry_income.insert(0, str(profile["monthly_income"]))

            self.combo_theme.set(profile["theme_preference"])
        else:
            # If no profile exists, set default values
            self.entry_currency.insert(0, "USD")
            self.entry_income.insert(0, "")
            self.combo_theme.set("light")

    def update_profile(self):
        """Update the user's profile in the database."""
        currency = self.entry_currency.get().strip()
        income = self.entry_income.get().strip()
        theme = self.combo_theme.get().strip()

        # Validate inputs
        if not currency:
            messagebox.showwarning("Input Error", "Please enter a default currency.")
            return
        if income and not income.replace('.', '', 1).isdigit():
            messagebox.showwarning("Input Error", "Please enter a valid monthly income (numeric value).")
            return
        if not theme or theme not in ["light", "dark"]:
            messagebox.showwarning("Input Error", "Please select a valid theme preference.")
            return

        try:
            # Convert income to float if provided
            income = float(income) if income else None

            # Update the profile in the database
            if update_profile(self.user_id, currency, income, theme):
                messagebox.showinfo("Success", "Profile updated successfully!")
            else:
                messagebox.showerror("Error", "Failed to update profile.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")