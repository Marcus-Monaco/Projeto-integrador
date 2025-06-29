from database.dao_factory import DaoFactory
from database.dao_consultar_bd import DaoConsultarBD

class BoConexao:
    def __init__(self, db_type="postgresql"):
        self.conexao = None
        self.bd = None
        self.db_type = db_type
    
    def conectar(self):
        if not self.conexao:
            # Use factory to get the appropriate connection
            self.conexao = DaoFactory.get_connection(self.db_type)
            self.bd = DaoConsultarBD(self.conexao)
            self.conexao.conectar()
    
    def desconectar(self):
        if self.conexao:
            self.conexao.desconectar()
