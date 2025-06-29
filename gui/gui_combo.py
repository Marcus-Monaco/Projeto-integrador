import tkinter as tk
from tkinter import ttk, messagebox
from controllers.co_combo import CoCombo

class GuiCombo:
    def __init__(self, conexao):
        self.root = tk.Tk()
        self.root.title("Sistema de Biblioteca")
        self.root.geometry("800x400")
        self.root.resizable(True, True)
        
        # Centralizar janela
        self.center_window()
        
        self.co = CoCombo(self, conexao)
        self.setup_ui()
    
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (400 // 2)
        self.root.geometry(f"800x400+{x}+{y}")
    
    def setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid for dynamic resizing
        for i in range(4):
            main_frame.grid_rowconfigure(i, weight=1)
        for i in range(3):
            main_frame.grid_columnconfigure(i, weight=1)
        
        # Title label
        title_label = tk.Label(main_frame, text="Sistema de Biblioteca", 
                              font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky="ew")
        
        # Book selection section
        book_frame = tk.LabelFrame(main_frame, text="Seleção de Livros", padx=10, pady=10)
        book_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        
        # Configure book frame grid
        book_frame.grid_columnconfigure(1, weight=1)
        
        # Label and ComboBox for books
        label_livro = tk.Label(book_frame, text="Selecione o Livro:", font=("Arial", 12))
        label_livro.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="w")
        
        self.combo_livros = ttk.Combobox(book_frame, font=("Arial", 12), width=50, state="readonly")
        self.combo_livros.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ew")
        
        self.btn_carregar_livros = tk.Button(book_frame, text="Carregar Lista", font=("Arial", 12),
                                           command=self.co.load_book_list, width=15)
        self.btn_carregar_livros.grid(row=0, column=2, padx=10, pady=10)
        
        # Query section
        query_frame = tk.LabelFrame(main_frame, text="Banco de Dados de Livros", padx=10, pady=10)
        query_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        
        # Configure query frame grid
        query_frame.grid_columnconfigure(0, weight=1)
        
        self.btn_carregar_dados = tk.Button(query_frame, text="Exibir Todos os Livros", font=("Arial", 12),
                                          command=self.co.show_all_books, width=25)
        self.btn_carregar_dados.grid(row=0, column=0, padx=10, pady=10)
        
        # Bottom buttons
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(20, 0))
        
        # Configure button frame
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)
        
        # Database info
        db_type = getattr(self.co.bo.conexao, 'db_type', 'postgresql')
        db_label = tk.Label(button_frame, text=f"Banco de Dados: {db_type.upper()}", 
                          font=("Arial", 10), fg="blue")
        db_label.grid(row=0, column=0, sticky="w")
        
        # Exit button
        btn_fechar = tk.Button(button_frame, text="Sair do Sistema", font=("Arial", 12, "bold"),
                              command=self.fechar_aplicacao, width=15)
        btn_fechar.grid(row=0, column=1)
        
        # Version info
        version_label = tk.Label(button_frame, text="v1.0.0", font=("Arial", 10))
        version_label.grid(row=0, column=2, sticky="e")
    
    def fechar_aplicacao(self):
        """Close application with confirmation"""
        if messagebox.askquestion("Confirmar Saída", "Tem certeza que deseja sair do sistema?", 
                                 parent=self.root) == 'yes':
            self.root.quit()
            self.root.destroy()
    
    def show(self):
        # Configure window to expand with screen
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Protocolo para fechar janela
        self.root.protocol("WM_DELETE_WINDOW", self.fechar_aplicacao)
        self.root.mainloop()
