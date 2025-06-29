from dao.dao_combo import DaoCombo

class BoCombo:
    def __init__(self, connection):
        self.conexao = connection
        self.dao = DaoCombo(connection)
    
    def get_books(self):
        return self.dao.lista_livros()
    
    def get_book_details(self):
        return self.dao.pesquisa_dados_livros()
    
    # Aliases for backward compatibility
    lista_livros = get_books
    pesquisa_dados_livros = get_book_details
