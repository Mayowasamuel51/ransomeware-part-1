import tkinter as tk
from tkinter import messagebox
import os
import sys

# Global variables
attempts = 3  # Maximum allowed attempts
unlock_time = 60  # Time (in seconds) before forced unlock

# Function to restart the program
def restart_program():
    os.execl(sys.executable, sys.executable, *sys.argv)

# Function to check password
def check_password():
    global attempts
    password = password_entry.get()
    if password == "123456":  # Replace with your desired password
        root.destroy()  # Unlock the screen
    else:
        attempts -= 1
        if attempts <= 0:
            messagebox.showerror("Error", "Too many incorrect attempts. System locked.")
        else:
            messagebox.showwarning("Warning", f"Incorrect password! {attempts} attempts left.")

# Function to automatically unlock after the timer expires
def auto_unlock():
    messagebox.showinfo("Info", "Time expired. Unlocking automatically.")
    root.destroy()

# Main locked screen function
def show_locked_screen():
    global root, password_entry

    # Create root window
    root = tk.Tk()
    root.title("LOCKED")
    root.attributes('-fullscreen', True)  # Fullscreen mode
    root.config(bg="black")

    # Locked message
    message = tk.Label(
        root,
        text="YOUR COMPUTER IS LOCKED\nEnter the password to unlock.",
        fg="white",
        bg="black",
        font=("Poppins", 50)
    )
    message.pack(pady=20)

    # Password entry
    password_entry = tk.Entry(root, show="*", font=("Poppins", 30), width=20)
    password_entry.pack(pady=20)

    # Submit button
    submit_button = tk.Button(root, text="Unlock", command=check_password, font=("Poppins", 30))
    submit_button.pack(pady=20)

    # Hidden instructions
    hidden_instructions = tk.Label(
        root,
        text="Press CTRL+U to unlock without password",
        fg="black",  # Hidden text
        bg="black",
        font=("Poppins", 10)
    )
    hidden_instructions.pack()

    # Bind CTRL+U to unlock directly
    root.bind('<Control-u>', lambda e: root.destroy())

    # Prevent closing with Alt+F4 or the window close button
    root.protocol('WM_DELETE_WINDOW', restart_program)

    # Auto-unlock after timeout
    root.after(unlock_time * 1000, auto_unlock)

    root.mainloop()

# Run the locked screen
show_locked_screen()
