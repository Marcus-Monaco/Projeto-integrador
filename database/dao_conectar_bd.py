import psycopg2
from .exception_bd import ExceptionBD
from .dao_string_conexao_postgresql import DaoStringConexaoPostgreSQL

class DaoConectarBD:
    def __init__(self, vo_conexao=None, conexao=None):
        self.vo_conexao = vo_conexao
        self.conexao = conexao
    
    def conectar(self):
        # Pegar configuração padrão
        self.vo_conexao = DaoStringConexaoPostgreSQL().get_configuracao_alternativa()
        
        # Testar dados da conexão
        if (not self.vo_conexao or not self.vo_conexao.base_dados or 
            not self.vo_conexao.host or not self.vo_conexao.porta or 
            not self.vo_conexao.senha or not self.vo_conexao.sgbd or 
            not self.vo_conexao.usuario):
            raise ExceptionBD(f"Não foi possível conectar com o SGBD com as informações {self.vo_conexao}")
        
        # Realizar conexão
        conexao_config = DaoStringConexaoPostgreSQL()
        connection_string = conexao_config.get_string_conexao(self.vo_conexao)
        
        try:
            self.conexao = psycopg2.connect(connection_string)
            self.conexao.autocommit = False
            return self.conexao
        except psycopg2.Error as e:
            raise ExceptionBD(f"Erro ao conectar: {e}")
    
    def desconectar(self):
        if self.conexao:
            self.conexao.close()
