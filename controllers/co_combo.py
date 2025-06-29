import tkinter as tk
from tkinter import messagebox
import threading
from business.bo_combo import BoCombo
from .co_consulta import CoConsulta

class CoCombo:
    def __init__(self, gui, conexao):
        self.gui = gui
        self.bo = BoCombo(conexao)
    
    def load_book_list(self):
        """Load books in separate thread"""
        # Disable button during loading
        self.gui.btn_carregar_livros.config(state='disabled', text='Carregando...')
        
        # Execute in separate thread
        thread = threading.Thread(target=self._load_books_thread)
        thread.daemon = True
        thread.start()
    
    def _load_books_thread(self):
        """Thread for loading books"""
        try:
            cursor = self.bo.get_books()
            livros = cursor.fetchall()
            
            # Build list for combobox
            titles = [livro[0].strip() for livro in livros]
            
            # Use after to update GUI in main thread
            self.gui.root.after(0, self._update_combo, titles)
            
        except Exception as ex:
            # Show error in main thread
            self.gui.root.after(0, self._show_loading_error, str(ex))
    
    def _update_combo(self, titles):
        """Update combo in main thread"""
        # Set combobox values
        self.gui.combo_livros['values'] = titles
        
        # Re-enable button
        self.gui.btn_carregar_livros.config(state='normal', text='Carregar Lista')
        
        # Show message
        messagebox.showinfo("Sistema de Biblioteca", 
                           f"Carregados {len(titles)} livros!",
                           parent=self.gui.root)
    
    def _show_loading_error(self, error):
        """Show error in main thread"""
        self.gui.btn_carregar_livros.config(state='normal', text='Carregar Lista')
        messagebox.showerror("Erro", f"Erro ao carregar livros: {error}",
                            parent=self.gui.root)
    
    def show_all_books(self):
        """Get list in separate thread"""
        # Disable button
        self.gui.btn_carregar_dados.config(state='disabled', text='Carregando...')
        
        # Execute in thread
        thread = threading.Thread(target=self._get_list_thread)
        thread.daemon = True
        thread.start()
    
    def _get_list_thread(self):
        """Thread for getting data"""
        try:
            cursor = self.bo.get_book_details()
            
            # Show query in main thread
            self.gui.root.after(0, self._show_query, cursor)
            
        except Exception as ex:
            self.gui.root.after(0, self._show_query_error, str(ex))
    
    def _show_query(self, cursor):
        """Show query in main thread"""
        try:
            # Re-enable button
            self.gui.btn_carregar_dados.config(state='normal', text='Exibir Todos os Livros')
            
            # Create query screen controller
            title = "Consulta de Livros"
            controller_consulta = CoConsulta(self.gui.root, True, cursor, title)
            
            # Show query
            controller_consulta.consultar()
            
        except Exception as ex:
            self._show_query_error(str(ex))
    
    def _show_query_error(self, error):
        """Show query error"""
        self.gui.btn_carregar_dados.config(state='normal', text='Exibir Todos os Livros')
        messagebox.showerror("Erro", f"Erro ao obter lista de livros: {error}",
                            parent=self.gui.root)

    # Alias methods for backward compatibility
    carregar_lista_livros = load_book_list
    obter_lista = show_all_books
