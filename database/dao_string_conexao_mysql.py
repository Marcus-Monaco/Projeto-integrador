from .dao_string_conexao import DaoStringConexao
from models.vo_conexao import VoConexao

class DaoStringConexaoMySQL(DaoStringConexao):
    
    def get_string_conexao(self, vo):
        # Format MySQL connection string
        # For MySQL we return parameters for mysql.connector
        return {
            'host': vo.host,
            'port': vo.porta,
            'database': vo.base_dados,
            'user': vo.usuario,
            'password': vo.senha
        }
    
    def get_configuracao_default(self):
        vo = VoConexao()
        vo.sgbd = "MySQL"
        vo.host = "localhost"
        vo.porta = "3306"
        vo.base_dados = "livros"
        vo.usuario = "biblioteca"
        vo.senha = "biblioteca123"
        vo.class_driver = "mysql"
        return vo
    
    def get_configuracao_alternativa(self):
        vo = VoConexao()
        vo.sgbd = "MySQL"
        vo.host = "localhost"
        vo.porta = "3306"
        vo.base_dados = "livros"
        vo.usuario = "biblioteca"
        vo.senha = "biblioteca123"
        vo.class_driver = "mysql"
        return vo 