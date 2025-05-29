import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

class GuiMontarTable:
    def __init__(self, cursor):
        self.cursor = cursor
    
    def cria_tabela(self):
        return self.monta_tabela()
    
    def monta_tabela(self):
        try:
            # Buscar dados do cursor
            dados = self.cursor.fetchall()
            
            if not dados:
                print("Tabela Vazia.")
                return None, None
            
            # Buscar metadados das colunas
            colunas = [desc[0] for desc in self.cursor.description]
            
            # Retornar colunas e dados
            return colunas, dados
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao montar tabela: {e}")
            return None, None
