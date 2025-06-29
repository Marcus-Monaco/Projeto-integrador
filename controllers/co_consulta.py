import tkinter as tk
from tkinter import messagebox, ttk
from gui.consulta.gui_consulta import GuiConsulta

class CoConsulta:
    def __init__(self, parent, modal, cursor, title):
        self.cursor = cursor
        self.parent = parent
        self.gui = GuiConsulta(parent, modal, title)
        self.return_value = False
        self.selected_data = None
    
    def consultar(self):
        """Build the query screen and show it to the user"""
        try:
            self.return_value = False
            
            # Configure data in GUI
            self.gui.set_data(self.cursor)
            
            # Configure callback for selection
            self.gui.set_selection_callback(self.on_selection)
            
            # Show screen
            self.gui.show()
                
        except Exception as ex:
            messagebox.showerror("Erro", 
                               f"Não foi possível consultar dados do banco!\n{ex}",
                               parent=self.parent)
    
    def on_selection(self, selected_data):
        """Callback when item is selected"""
        self.return_value = True
        self.selected_data = selected_data
        
        # Show detailed information in a custom window
        self.show_book_details(selected_data)
    
    def show_book_details(self, book_data):
        """Show detailed book information in a custom window"""
        # Create a new window
        details_window = tk.Toplevel(self.gui.window)
        details_window.title("Detalhes do Livro")
        details_window.geometry("700x450")
        details_window.resizable(True, True)
        details_window.transient(self.gui.window)
        
        # Center the window
        details_window.update_idletasks()
        x = (details_window.winfo_screenwidth() // 2) - (700 // 2)
        y = (details_window.winfo_screenheight() // 2) - (450 // 2)
        details_window.geometry(f"700x450+{x}+{y}")
        
        # Main frame
        main_frame = tk.Frame(details_window, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Book title
        title_frame = tk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(title_frame, text="Detalhes do Livro", font=("Arial", 16, "bold"))
        title_label.pack(anchor="center")
        
        # Book info frame
        info_frame = tk.LabelFrame(main_frame, text="Informações", padx=15, pady=15)
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid
        info_frame.columnconfigure(0, weight=0)
        info_frame.columnconfigure(1, weight=1)
        
        # Extract book data
        titulo = book_data[0] if len(book_data) > 0 else "N/A"
        autor = book_data[1] if len(book_data) > 1 else "N/A"
        edicao = book_data[2] if len(book_data) > 2 else "N/A"
        ano = book_data[3] if len(book_data) > 3 else "N/A"
        
        # Display fields with better formatting
        fields = [
            ("Título:", titulo),
            ("Autor:", autor),
            ("Edição:", edicao),
            ("Ano de Publicação:", ano)
        ]
        
        # Add fields to grid
        for i, (label_text, value) in enumerate(fields):
            # Label
            label = tk.Label(info_frame, text=label_text, font=("Arial", 12, "bold"), anchor="w")
            label.grid(row=i, column=0, sticky="w", padx=(0, 10), pady=10)
            
            # Value (with scrollable text for long values)
            if label_text == "Título:" or label_text == "Autor:":
                # For potentially long text, use Text widget with scrollbar
                frame = tk.Frame(info_frame)
                frame.grid(row=i, column=1, sticky="ew")
                
                # Configure frame for text expansion
                frame.columnconfigure(0, weight=1)
                
                text = tk.Text(frame, wrap=tk.WORD, height=4, width=60, font=("Arial", 12))
                text.insert("1.0", value)
                text.config(state="disabled")
                text.grid(row=0, column=0, sticky="ew")
                
                # Add scrollbar if needed
                scrollbar = tk.Scrollbar(frame, command=text.yview)
                text.config(yscrollcommand=scrollbar.set)
                
                # Only show scrollbar if text is long
                if len(value) > 80:
                    scrollbar.grid(row=0, column=1, sticky="ns")
            else:
                # For shorter values, use Label
                value_label = tk.Label(info_frame, text=value, font=("Arial", 12), anchor="w")
                value_label.grid(row=i, column=1, sticky="w", pady=10)
        
        # Add cover image placeholder
        img_frame = tk.LabelFrame(main_frame, text="Capa", padx=10, pady=10)
        img_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Placeholder for book cover (could be replaced with actual image in future)
        cover_label = tk.Label(img_frame, text="📚", font=("Arial", 36))
        cover_label.pack(pady=10)
        
        # Button frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Close button
        close_button = tk.Button(button_frame, text="Fechar", font=("Arial", 12, "bold"),
                              command=details_window.destroy, width=15)
        close_button.pack(side=tk.RIGHT)
        
        # Aguardar a janela ser renderizada antes de tentar fazer grab_set
        details_window.update()
        
        # Agora é seguro fazer grab_set
        try:
            details_window.grab_set()
        except Exception:
            # Se ainda houver erro, ignoramos o grab_set
            pass
    
    def set_table_selection(self, enable):
        """Method to enable or disable selection in the query table"""
        self.gui.set_selecao_tabela(enable)
    
    def has_return(self):
        return self.return_value
    
    def get_selected_data(self):
        return self.selected_data
    
    # Alias methods for backward compatibility
    set_selecao_tabela = set_table_selection
    is_retorno = has_return
    get_objeto_consulta = get_selected_data
