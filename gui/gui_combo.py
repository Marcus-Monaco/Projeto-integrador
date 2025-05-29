import tkinter as tk
from tkinter import ttk, messagebox
from controllers.co_combo import CoCombo

class GuiCombo:
    def __init__(self, conexao):
        self.root = tk.Tk()
        self.root.title("TDD: teste com combobox e table")
        self.root.geometry("800x400")
        self.root.resizable(True, True)
        
        # Centralizar janela
        self.center_window()
        
        self.co = CoCombo(self, conexao)
        self.setup_ui()
    
    def center_window(self):
        """Centralizar janela na tela"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (400 // 2)
        self.root.geometry(f"800x400+{x}+{y}")
    
    def setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configurar grid
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Label e ComboBox para livros
        label_livro = tk.Label(main_frame, text="Livro:", font=("Arial", 16, "bold"))
        label_livro.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="w")
        
        self.combo_livros = ttk.Combobox(main_frame, font=("Arial", 12), width=50, state="readonly")
        self.combo_livros.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ew")
        
        self.btn_carregar_livros = tk.Button(main_frame, text="Carregar", font=("Arial", 12, "bold"),
                                           command=self.co.carregar_lista_livros, width=10)
        self.btn_carregar_livros.grid(row=0, column=2, padx=10, pady=10)
        
        # Label e botão para dados dos livros
        label_dados = tk.Label(main_frame, text="Livros e seus dados:", font=("Arial", 16, "bold"))
        label_dados.grid(row=1, column=0, padx=(0, 10), pady=10, sticky="w")
        
        self.btn_carregar_dados = tk.Button(main_frame, text="Carregar", font=("Arial", 12, "bold"),
                                          command=self.co.obter_lista, width=15)
        self.btn_carregar_dados.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        # Separador
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.grid(row=2, column=0, columnspan=3, sticky="ew", pady=20)
        
        # Botão fechar
        btn_fechar = tk.Button(main_frame, text="Fechar", font=("Arial", 12, "bold"),
                              command=self.fechar_aplicacao, width=10)
        btn_fechar.grid(row=3, column=1, pady=20)
    
    def fechar_aplicacao(self):
        """Fechar aplicação com confirmação"""
        if messagebox.askquestion("Confirmar", "Deseja realmente sair?", 
                                 parent=self.root) == 'yes':
            self.root.quit()
            self.root.destroy()
    
    def show(self):
        # Protocolo para fechar janela
        self.root.protocol("WM_DELETE_WINDOW", self.fechar_aplicacao)
        self.root.mainloop()
