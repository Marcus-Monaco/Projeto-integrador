import psycopg2
from .exception_bd import ExceptionBD

class DaoConsultarBD:
    def __init__(self, bd):
        self.bd = bd
        self.conexao = None
    
    def get_cursor(self, sql):
        self.conexao = self.bd.conexao
        cursor = self.conexao.cursor()
        return cursor
    
    def executa_sql(self, cursor):
        cursor.execute()
        self.conexao.commit()
    
    def consulta(self, sql):
        self.conexao = self.bd.conexao
        cursor = self.conexao.cursor()
        cursor.execute(sql)
        return cursor
    
    def consulta_cursor(self, cursor):
        return cursor
    
    def executa_sql_string(self, sql):
        self.conexao = self.bd.conexao
        cursor = self.conexao.cursor()
        cursor.execute(sql)
        self.conexao.commit()
