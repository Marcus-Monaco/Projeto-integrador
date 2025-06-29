import tkinter as tk
from tkinter import messagebox
import argparse
from business.bo_conexao import BoConexao
from gui.gui_combo import GuiCombo

class Main:
    def __init__(self, db_type="postgresql"):
        self.connection = BoConexao(db_type)
        self.gui = None
    
    def connect(self):
        try:
            self.connection.conectar()
            print(f"Conectado ao banco de dados {self.connection.db_type}")
        except Exception as ex:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados! {ex}")
    
    def disconnect(self):
        try:
            self.connection.desconectar()
            print(f"Desconectado do banco de dados {self.connection.db_type}")
        except Exception as ex:
            messagebox.showerror("Erro", f"Erro ao desconectar do banco de dados! {ex}")
    
    def run(self):
        # Connect
        self.connect()
        
        # Create and show screen
        self.gui = GuiCombo(self.connection)
        self.gui.show()
        
        # Disconnect
        self.disconnect()

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Sistema de Gerenciamento de Biblioteca')
    parser.add_argument('--db', choices=['postgresql', 'mysql'], 
                        default='postgresql',
                        help='Tipo de banco de dados (postgresql ou mysql)')
    
    args = parser.parse_args()
    
    app = Main(db_type=args.db)
    app.run()
