import tkinter.messagebox as messagebox

def notify_user(message):
    messagebox.showinfo("Notification", message)

def notify_admin(message):
    messagebox.showwarning("Admin Alert", message)