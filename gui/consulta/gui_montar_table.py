import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

class GuiMontarTable:
    def __init__(self, cursor):
        self.cursor = cursor
    
    def cria_tabela(self):
        return self.build_table()
    
    def build_table(self):
        try:
            # Get data from cursor
            data = self.cursor.fetchall()
            
            if not data:
                print("Empty table.")
                return None, None
            
            # Get column metadata
            columns = [desc[0] for desc in self.cursor.description]
            
            # Return columns and data
            return columns, data
            
        except Exception as e:
            messagebox.showerror("Error", f"Error building table: {e}")
            return None, None
    
    # Alias for backward compatibility
    monta_tabela = build_table
