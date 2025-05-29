class DaoCombo:
    def __init__(self, conexao):
        self.conexao = conexao
    
    def lista_livros(self):
        sql = "select titulo from livros"
        cursor = self.conexao.bd.consulta(sql)
        return cursor
    
    def pesquisa_dados_livros(self):
        sql = """select l.titulo, a.nome, e.numero, e.ano
                from livros l inner join livroAutor la on l.codigo = la.codigoLivro 
                inner join autor a on a.codigo = la.codigoAutor
                inner join edicao e on a.codigo = e.codigoLivro"""
        cursor = self.conexao.bd.consulta(sql)
        return cursor
