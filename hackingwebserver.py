import tkinter as tk 
from tkinter import messagebox

def unlock():

    root.destroy()

def show_locked_screen():
    global root
    root = tk.Tk()
    root.title("HOW FAR")
    root.attributes('-fullscreen', True)
    root.config(bg="black")
    message = tk.Label(root, text="YOUR COMPUTER IS LOCKED \nusername ***** \npassword *****", fg="white", bg="black", font=("poppins", 120))
    message.pack(expand=True)
    
    hidden_instructions = tk.Label(root , text="Press CTPL+U to Unlock", fg="black", bg="black", font=("poppins",121) )
    hidden_instructions.pack()




    root.bind('<Control-u>',lambda e:unlock())


    root.protocol('WM_DELETE_WINDOW', lambda:None)

    root.mainloop()



show_locked_screen()