import tkinter as tk
from tkinter import ttk, messagebox
from .gui_montar_table import GuiMontarTable

class GuiConsulta:
    def __init__(self, parent, modal, title):
        self.parent = parent
        self.modal = modal
        self.title = title
        self.retorno = False
        self.objeto_consulta = None
        self.dados = None
        self.colunas = None
        self.selection_callback = None
        
        # Criar janela
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title(title)
        self.window.geometry("1000x700")
        self.window.resizable(True, True)
        
        # Centralizar janela
        self.center_window()
        
        # Configurar modalidade
        if parent:
            self.window.transient(parent)
        if modal:
            self.window.grab_set()
        
        self.setup_ui()
    
    def center_window(self):
        """Centralizar janela"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.window.winfo_screenheight() // 2) - (700 // 2)
        self.window.geometry(f"1000x700+{x}+{y}")
    
    def setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Label de instruções
        label_info = tk.Label(main_frame, 
                             text="Double-click em uma linha para selecionar",
                             font=("Arial", 11), fg="blue")
        label_info.pack(pady=(0, 10))
        
        # Frame para a tabela
        table_frame = tk.Frame(main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview para simular JTable
        self.tree = ttk.Treeview(table_frame, show="headings", height=20)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=v_scrollbar.set)
        
        h_scrollbar = ttk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.configure(xscrollcommand=h_scrollbar.set)
        
        # Frame para botões
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Botão Fechar
        btn_fechar = tk.Button(button_frame, text="Fechar", font=("Arial", 12, "bold"),
                              command=self.fechar, width=12)
        btn_fechar.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Label com total de registros
        self.label_total = tk.Label(button_frame, text="", font=("Arial", 10))
        self.label_total.pack(side=tk.LEFT)
        
        # Bind para clique na tabela
        self.tree.bind('<Double-1>', self.on_item_select)
    
    def set_data(self, cursor):
        """Configura os dados na tabela"""
        try:
            # Montar tabela usando GuiMontarTable
            montador = GuiMontarTable(cursor)
            colunas, dados = montador.cria_tabela()
            
            if not colunas or not dados:
                self.label_total.config(text="Nenhum dado encontrado")
                return
            
            self.colunas = colunas
            self.dados = dados
            
            # Configurar colunas
            self.tree["columns"] = colunas
            
            # Configurar cabeçalhos
            for col in colunas:
                self.tree.heading(col, text=col.upper())
                self.tree.column(col, width=200, anchor=tk.W, minwidth=100)
            
            # Inserir dados
            for i, row in enumerate(dados):
                # Limpar dados (trim)
                clean_row = []
                for item in row:
                    if isinstance(item, str):
                        clean_row.append(item.strip())
                    else:
                        clean_row.append(str(item) if item is not None else "")
                
                self.tree.insert("", tk.END, iid=i, values=clean_row)
            
            # Atualizar label de total
            self.label_total.config(text=f"Total de registros: {len(dados)}")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao configurar dados: {e}",
                               parent=self.window)
    
    def on_item_select(self, event):
        """Handle item selection - CORRIGIDO"""
        try:
            selection = self.tree.selection()
            if not selection:
                return
            
            # Pegar item selecionado
            item_id = selection[0]
            linha = int(item_id)
            
            if linha < 0 or linha >= len(self.dados):
                return
            
            # Criar objeto consulta com os dados da linha selecionada
            dados_selecionados = []
            for item in self.dados[linha]:
                if isinstance(item, str):
                    dados_selecionados.append(item.strip())
                else:
                    dados_selecionados.append(str(item) if item is not None else "")
            
            # Chamar callback se definido
            if self.selection_callback:
                self.selection_callback(dados_selecionados)
            
            self.retorno = True
            self.objeto_consulta = dados_selecionados
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na seleção: {e}",
                               parent=self.window)
    
    def set_selection_callback(self, callback):
        """Definir callback para seleção"""
        self.selection_callback = callback
    
    def fechar(self):
        """Fechar janela"""
        self.retorno = False
        self.window.destroy()
    
    def show(self):
        """Mostrar janela"""
        self.window.protocol("WM_DELETE_WINDOW", self.fechar)
        self.window.mainloop()
    
    def set_selecao_tabela(self, selecao):
        """Permitir ou inibir seleção na tabela"""
        if selecao:
            self.tree.bind('<Double-1>', self.on_item_select)
        else:
            self.tree.unbind('<Double-1>')
