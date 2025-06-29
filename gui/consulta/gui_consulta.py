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
        
        # Create window
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title(title)
        self.window.geometry("1000x700")
        self.window.resizable(True, True)
        
        # Center window
        self.center_window()
        
        # Configure modality
        if parent:
            self.window.transient(parent)
        if modal:
            self.window.grab_set()
        
        self.setup_ui()
    
    def center_window(self):
        """Center window on screen"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.window.winfo_screenheight() // 2) - (700 // 2)
        self.window.geometry(f"1000x700+{x}+{y}")
    
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configure frame for dynamic resizing
        main_frame.grid_rowconfigure(1, weight=1)  # Table row
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Title and instruction
        title_frame = tk.Frame(main_frame)
        title_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        # Configure title frame
        title_frame.grid_columnconfigure(0, weight=1)
        
        # Title label
        title_label = tk.Label(title_frame, text=self.title, 
                             font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, sticky="w")
        
        # Instruction label
        label_info = tk.Label(title_frame, 
                             text="Clique duplo em uma linha para ver detalhes",
                             font=("Arial", 11), fg="blue")
        label_info.grid(row=1, column=0, sticky="w", pady=(5, 0))
        
        # Table frame with border
        table_frame = tk.LabelFrame(main_frame, text="Resultados da Consulta")
        table_frame.grid(row=1, column=0, sticky="nsew")
        
        # Configure table frame for resizing
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Create frame for treeview and vertical scrollbar
        tree_frame = tk.Frame(table_frame)
        tree_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Configure tree frame
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Configure style for treeview
        style = ttk.Style()
        style.theme_use("default")
        
        # Configure tag colors for alternating rows
        style.configure("Treeview", 
                       background="#f0f0f0",
                       foreground="black",
                       rowheight=25,
                       fieldbackground="#f0f0f0",
                       font=("Arial", 10))
        
        # Configure selected row style
        style.map('Treeview', 
                 background=[('selected', '#3a7ebf')],
                 foreground=[('selected', 'white')])
        
        # Treeview for table display
        self.tree = ttk.Treeview(tree_frame, show="headings", style="Treeview")
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=v_scrollbar.set)
        
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        self.tree.configure(xscrollcommand=h_scrollbar.set)
        
        # Status and button frame
        status_frame = tk.Frame(main_frame)
        status_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        
        # Configure status frame
        status_frame.grid_columnconfigure(1, weight=1)
        
        # Total records label
        self.label_total = tk.Label(status_frame, text="", font=("Arial", 10))
        self.label_total.grid(row=0, column=0, sticky="w")
        
        # Close button
        btn_fechar = tk.Button(status_frame, text="Fechar Janela", font=("Arial", 12, "bold"),
                              command=self.fechar, width=15)
        btn_fechar.grid(row=0, column=2, sticky="e")
        
        # Bind for table click
        self.tree.bind('<Double-1>', self.on_item_select)
        self.tree.bind('<ButtonRelease-1>', self.highlight_row)
    
    def set_data(self, cursor):
        """Configure data in the table"""
        try:
            # Build table using GuiMontarTable
            montador = GuiMontarTable(cursor)
            colunas, dados = montador.cria_tabela()
            
            if not colunas or not dados:
                self.label_total.config(text="Nenhum dado encontrado")
                return
            
            self.colunas = colunas
            self.dados = dados
            
            # Configure columns
            self.tree["columns"] = colunas
            
            # Configure headers with better column names
            column_display_names = {
                "titulo": "TÍTULO",
                "nome": "AUTOR",
                "numero": "EDIÇÃO",
                "ano": "ANO"
            }
            
            # Set column headers and widths
            for col in colunas:
                display_name = column_display_names.get(col, col.upper())
                self.tree.heading(col, text=display_name, anchor=tk.CENTER)
                
                # Set appropriate column width based on content
                if col in ["titulo", "nome"]:
                    width = 350  # Wider for text columns
                else:
                    width = 100  # Narrower for number columns
                    
                self.tree.column(col, width=width, minwidth=100)
            
            # Define tags for alternating row colors
            self.tree.tag_configure('oddrow', background='#E8E8E8')
            self.tree.tag_configure('evenrow', background='white')
            
            # Insert data
            for i, row in enumerate(dados):
                # Clean data (trim)
                clean_row = []
                for item in row:
                    if isinstance(item, str):
                        clean_row.append(item.strip())
                    else:
                        clean_row.append(str(item) if item is not None else "")
                
                # Apply alternating row colors
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                self.tree.insert("", tk.END, iid=i, values=clean_row, tags=(tag,))
            
            # Update total label
            self.label_total.config(text=f"Total de registros: {len(dados)}")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao configurar dados: {e}",
                               parent=self.window)
    
    def on_item_select(self, event):
        """Handle item selection"""
        try:
            selection = self.tree.selection()
            if not selection:
                return
            
            # Get selected item
            item_id = selection[0]
            linha = int(item_id)
            
            if linha < 0 or linha >= len(self.dados):
                return
            
            # Create query object with selected row data
            dados_selecionados = []
            for item in self.dados[linha]:
                if isinstance(item, str):
                    dados_selecionados.append(item.strip())
                else:
                    dados_selecionados.append(str(item) if item is not None else "")
            
            # Call callback if defined
            if self.selection_callback:
                self.selection_callback(dados_selecionados)
            
            self.retorno = True
            self.objeto_consulta = dados_selecionados
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na seleção: {e}",
                               parent=self.window)
    
    def highlight_row(self, event):
        """Highlight the selected row"""
        try:
            selection = self.tree.selection()
            if selection:
                # Get selected item
                item_id = selection[0]
                
                # Ensure the row is visible
                self.tree.see(item_id)
                
                # Highlight the row (already handled by ttk.Treeview selection)
        except Exception:
            pass
    
    def set_selection_callback(self, callback):
        """Set callback for selection"""
        self.selection_callback = callback
    
    def fechar(self):
        """Close window"""
        self.retorno = False
        self.window.destroy()
    
    def show(self):
        """Show window"""
        self.window.protocol("WM_DELETE_WINDOW", self.fechar)
        self.window.mainloop()
    
    def set_selecao_tabela(self, selecao):
        """Enable or disable table selection"""
        if selecao:
            self.tree.bind('<Double-1>', self.on_item_select)
        else:
            self.tree.unbind('<Double-1>')
