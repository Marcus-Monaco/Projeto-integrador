from abc import ABC, abstractmethod

class DaoStringConexao(ABC):
    
    @abstractmethod
    def get_string_conexao(self, vo):
        pass
    
    @abstractmethod
    def get_configuracao_default(self):
        pass
    
    @abstractmethod
    def get_configuracao_alternativa(self):
        pass
