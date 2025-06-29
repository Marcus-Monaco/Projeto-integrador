from .dao_conectar_bd import DaoConectarBD
from .dao_conectar_mysql import DaoConectarMySQL

class DaoFactory:
    """Factory class to create database connections based on the type"""
    
    @staticmethod
    def get_connection(db_type="postgresql"):
        """
        Get database connection based on type
        
        Args:
            db_type (str): Type of database ('postgresql' or 'mysql')
            
        Returns:
            Connection object for the specified database
        """
        if db_type.lower() == "mysql":
            return DaoConectarMySQL()
        else:
            # Default to PostgreSQL
            return DaoConectarBD() 