from tkinter import *
import os

def show_error_window(message):
    error_window = Toplevel()
    error_window.title("Error")
    current_directory = os.path.dirname(os.path.abspath(__file__))
    error_window.iconbitmap(os.path.join(current_directory, "assets", "icon.ico"))
    error_window.resizable(False, False)
    
    Label(error_window, text=message, font=("Courier", 16, "bold"), fg="red").pack(pady=20)
    exit_btn = Button(error_window, text="OK", command=error_window.destroy, font=("Arial", 12), bg="green", fg="white", width=10)
    exit_btn.pack(pady=10)