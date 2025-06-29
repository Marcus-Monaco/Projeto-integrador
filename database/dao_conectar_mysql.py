import mysql.connector
from .exception_bd import ExceptionBD
from .dao_string_conexao_mysql import DaoStringConexaoMySQL

class DaoConectarMySQL:
    def __init__(self, vo_conexao=None, conexao=None):
        self.vo_conexao = vo_conexao
        self.conexao = conexao
    
    def conectar(self):
        # Pegar configuração padrão
        self.vo_conexao = DaoStringConexaoMySQL().get_configuracao_alternativa()
        
        # Testar dados da conexão
        if (not self.vo_conexao or not self.vo_conexao.base_dados or 
            not self.vo_conexao.host or not self.vo_conexao.porta or 
            not self.vo_conexao.senha or not self.vo_conexao.sgbd or 
            not self.vo_conexao.usuario):
            raise ExceptionBD(f"Não foi possível conectar com o MySQL com as informações {self.vo_conexao}")
        
        # Realizar conexão
        conexao_config = DaoStringConexaoMySQL()
        connection_params = conexao_config.get_string_conexao(self.vo_conexao)
        
        try:
            self.conexao = mysql.connector.connect(**connection_params)
            self.conexao.autocommit = False
            return self.conexao
        except mysql.connector.Error as e:
            raise ExceptionBD(f"Erro ao conectar ao MySQL: {e}")
    
    def desconectar(self):
        if self.conexao:
            self.conexao.close() 