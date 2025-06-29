class DaoCombo:
    def __init__(self, connection):
        self.conexao = connection
    
    def get_books(self):
        sql = "select titulo from livros"
        cursor = self.conexao.bd.consulta(sql)
        return cursor
    
    def get_book_details(self):
        sql = """select l.titulo, a.nome, e.numero, e.ano
                from livros l inner join livroautor la on l.codigo = la.codigolivro 
                inner join autor a on a.codigo = la.codigoautor
                inner join edicao e on e.codigolivro = l.codigo"""
        cursor = self.conexao.bd.consulta(sql)
        return cursor
    
    # Aliases for backward compatibility
    lista_livros = get_books
    pesquisa_dados_livros = get_book_details
