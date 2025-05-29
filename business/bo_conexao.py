from database.dao_conectar_bd import DaoConectarBD
from database.dao_consultar_bd import DaoConsultarBD

class BoConexao:
    def __init__(self):
        self.conexao = None
        self.bd = None
    
    def conectar(self):
        if not self.conexao:
            self.conexao = DaoConectarBD()
            self.bd = DaoConsultarBD(self.conexao)
            self.conexao.conectar()
    
    def desconectar(self):
        if self.conexao:
            self.conexao.desconectar()
