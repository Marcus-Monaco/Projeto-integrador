from .dao_string_conexao import DaoStringConexao
from models.vo_conexao import VoConexao

class DaoStringConexaoPostgreSQL(DaoStringConexao):
    
    def get_string_conexao(self, vo):
        url = f"host={vo.host} port={vo.porta} dbname={vo.base_dados} user={vo.usuario} password={vo.senha}"
        print(url)
        return url
    
    def get_configuracao_default(self):
        vo = VoConexao()
        vo.sgbd = "PostgreSQL"
        vo.host = "slinf30.ucs.br"
        vo.porta = "5432"
        vo.base_dados = "inf0211"
        vo.usuario = "alunos"
        vo.senha = "postgres"
        vo.class_driver = "postgresql"
        return vo
    
    def get_configuracao_alternativa(self):
        vo = VoConexao()
        vo.sgbd = "PostgreSQL"
        vo.host = "localhost"
        vo.porta = "5432"
        vo.base_dados = "livros"
        vo.usuario = "postgres"
        vo.senha = "postgres"
        vo.class_driver = "postgresql"
        return vo
