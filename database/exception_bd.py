import tkinter as tk
from tkinter import messagebox

class ExceptionBD(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.show_message()
    
    def show_message(self):
        root = tk.Tk()
        root.withdraw()  # Oculta a janela principal
        messagebox.showerror("Exceção gerada no acesso ao SGBD", str(self))
        root.destroy()
