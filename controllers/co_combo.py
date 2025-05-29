import tkinter as tk
from tkinter import messagebox
import threading
from business.bo_combo import BoCombo
from .co_consulta import CoConsulta

class CoCombo:
    def __init__(self, gui, conexao):
        self.gui = gui
        self.bo = BoCombo(conexao)
    
    def carregar_lista_livros(self):
        """Carregar livros em thread separada"""
        # Desabilitar botão durante carregamento
        self.gui.btn_carregar_livros.config(state='disabled', text='Carregando...')
        
        # Executar em thread separada
        thread = threading.Thread(target=self._carregar_livros_thread)
        thread.daemon = True
        thread.start()
    
    def _carregar_livros_thread(self):
        """Thread para carregar livros"""
        try:
            cursor = self.bo.lista_livros()
            livros = cursor.fetchall()
            
            # Montar lista para o combobox
            titulos = [livro[0].strip() for livro in livros]
            
            # Usar after para atualizar GUI na thread principal
            self.gui.root.after(0, self._atualizar_combo, titulos)
            
        except Exception as ex:
            # Mostrar erro na thread principal
            self.gui.root.after(0, self._mostrar_erro_carregamento, str(ex))
    
    def _atualizar_combo(self, titulos):
        """Atualizar combo na thread principal"""
        # Setar no combobox
        self.gui.combo_livros['values'] = titulos
        
        # Reabilitar botão
        self.gui.btn_carregar_livros.config(state='normal', text='Carregar')
        
        # Mostrar mensagem - AGORA vai aparecer imediatamente
        messagebox.showinfo("Teste TDD", 
                           f"Carregados {len(titulos)} registros!",
                           parent=self.gui.root)
    
    def _mostrar_erro_carregamento(self, erro):
        """Mostrar erro na thread principal"""
        self.gui.btn_carregar_livros.config(state='normal', text='Carregar')
        messagebox.showerror("Erro", f"Erro ao carregar livros: {erro}",
                            parent=self.gui.root)
    
    def obter_lista(self):
        """Obter lista em thread separada"""
        # Desabilitar botão
        self.gui.btn_carregar_dados.config(state='disabled', text='Carregando...')
        
        # Executar em thread
        thread = threading.Thread(target=self._obter_lista_thread)
        thread.daemon = True
        thread.start()
    
    def _obter_lista_thread(self):
        """Thread para obter dados"""
        try:
            cursor = self.bo.pesquisa_dados_livros()
            
            # Mostrar consulta na thread principal
            self.gui.root.after(0, self._mostrar_consulta, cursor)
            
        except Exception as ex:
            self.gui.root.after(0, self._mostrar_erro_consulta, str(ex))
    
    def _mostrar_consulta(self, cursor):
        """Mostrar consulta na thread principal"""
        try:
            # Reabilitar botão
            self.gui.btn_carregar_dados.config(state='normal', text='Carregar')
            
            # Criar controlador da tela de consulta
            title = "Consultar livros"
            controller_consulta = CoConsulta(self.gui.root, True, cursor, title)
            
            # Mostrar consulta
            controller_consulta.consultar()
            
        except Exception as ex:
            self._mostrar_erro_consulta(str(ex))
    
    def _mostrar_erro_consulta(self, erro):
        """Mostrar erro de consulta"""
        self.gui.btn_carregar_dados.config(state='normal', text='Carregar')
        messagebox.showerror("Erro", f"Erro ao obter lista: {erro}",
                            parent=self.gui.root)
