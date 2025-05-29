from dao.dao_combo import DaoCombo

class BoCombo:
    def __init__(self, conexao):
        self.conexao = conexao
        self.dao = DaoCombo(conexao)
    
    def lista_livros(self):
        return self.dao.lista_livros()
    
    def pesquisa_dados_livros(self):
        return self.dao.pesquisa_dados_livros()
