import tkinter as tk
from tkinter import messagebox
import os
import sys
import ctypes
import keyboard

# Global variables
attempts = 3  # Maximum allowed attempts
unlock_time = 60  # Time (in seconds) before forced unlock

# Constants
HWND_TOPMOST = -1
SWP_NOSIZE = 0x0001
SWP_NOMOVE = 0x0002
SWP_SHOWWINDOW = 0x0040

# Set window always on top
def set_always_on_top(window_id):
    ctypes.windll.user32.SetWindowPos(window_id, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOSIZE | SWP_NOMOVE | SWP_SHOWWINDOW)

# Disable Task Manager (Windows Only)
def disable_task_manager():
    os.system("reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v DisableTaskMgr /t REG_DWORD /d 1 /f")

# Re-enable Task Manager (Windows Only)
def enable_task_manager():
    os.system("reg delete HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v DisableTaskMgr /f")

# Function to restart the program
def restart_program():
    os.execl(sys.executable, sys.executable, *sys.argv)

# Function to check password
def check_password():
    global attempts
    password = password_entry.get()
    if password == "123456":  # Replace with your desired password
        enable_task_manager()  # Re-enable Task Manager on unlock
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
    enable_task_manager()  # Re-enable Task Manager on auto-unlock
    root.destroy()

# Main locked screen function
def show_locked_screen():
    global root, password_entry

    # Disable Task Manager
    disable_task_manager()

    # Create root window
    root = tk.Tk()
    root.title("LOCKED")
    root.attributes('-fullscreen', True)  # Fullscreen mode
    root.config(bg="black")

    # Set always on top
    root_id = ctypes.windll.user32.GetForegroundWindow()
    set_always_on_top(root_id)

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
    root.bind('<Control-u>', lambda e: [enable_task_manager(), root.destroy()])

    # Prevent closing with Alt+F4 or the window close button
    root.protocol('WM_DELETE_WINDOW', restart_program)

    # Auto-unlock after timeout
    root.after(unlock_time * 1000, auto_unlock)

    # Block system keys (Windows key, Alt+Tab, Ctrl+Esc)
    keyboard.block_key("windows")
    keyboard.add_hotkey("alt+tab", lambda: None)  # Block Alt+Tab
    keyboard.add_hotkey("ctrl+esc", lambda: None)  # Block Ctrl+Esc

    root.mainloop()

# Run the locked screen
try:
    show_locked_screen()
finally:
    # Ensure Task Manager is re-enabled if something goes wrong
    enable_task_manager()
    keyboard.unhook_all()  # Unblock all keys
