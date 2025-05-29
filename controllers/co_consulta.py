import tkinter as tk
from tkinter import messagebox
from gui.consulta.gui_consulta import GuiConsulta

class CoConsulta:
    def __init__(self, parent, modal, cursor, title):
        self.cursor = cursor
        self.parent = parent
        self.gui = GuiConsulta(parent, modal, title)
        self.retorno = False
        self.objeto_consulta = None
    
    def consultar(self):
        """Monta a tela de consulta e mostra para o usuário"""
        try:
            self.retorno = False
            
            # Configurar dados na GUI
            self.gui.set_data(self.cursor)
            
            # Configurar callback para seleção
            self.gui.set_selection_callback(self.on_selection)
            
            # Mostrar tela
            self.gui.show()
                
        except Exception as ex:
            messagebox.showerror("Erro", 
                               f"Não foi possível consultar os dados no banco de dados!\n{ex}",
                               parent=self.parent)
    
    def on_selection(self, dados_selecionados):
        """Callback quando item é selecionado"""
        self.retorno = True
        self.objeto_consulta = dados_selecionados
        
        # Mostrar dados selecionados - AGORA vai aparecer imediatamente
        messagebox.showinfo("Consultar livros", 
                           f"Dados selecionados:\n{dados_selecionados}",
                           parent=self.gui.window)
    
    def set_selecao_tabela(self, selecao):
        """Método para permitir ou inibir a seleção na tabela de consulta"""
        self.gui.set_selecao_tabela(selecao)
    
    def is_retorno(self):
        return self.retorno
    
    def get_objeto_consulta(self):
        return self.objeto_consulta
