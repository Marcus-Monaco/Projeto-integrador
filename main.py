import tkinter as tk
from tkinter import messagebox
from business.bo_conexao import BoConexao
from gui.gui_combo import GuiCombo

class Principal:
    def __init__(self):
        self.conexao = BoConexao()
        self.gui = None
    
    def conectar(self):
        try:
            self.conexao.conectar()
            print("conectou")
        except Exception as ex:
            messagebox.showerror("Erro", f"Erro ao conectar no banco de dados! {ex}")
    
    def desconectar(self):
        try:
            self.conexao.desconectar()
            print("desconectou")
        except Exception as ex:
            messagebox.showerror("Erro", f"Erro ao desconectar do banco de dados! {ex}")
    
    def executar(self):
        # Conectar
        self.conectar()
        
        # Criar e mostrar tela
        self.gui = GuiCombo(self.conexao)
        self.gui.show()
        
        # Desconectar
        self.desconectar()

if __name__ == "__main__":
    app = Principal()
    app.executar()
