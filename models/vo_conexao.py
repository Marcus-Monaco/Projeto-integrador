class VoConexao:
    def __init__(self, sgbd=None, host=None, porta=None, base_dados=None, 
                 usuario=None, senha=None, class_driver=None):
        self.sgbd = sgbd
        self.host = host
        self.porta = porta
        self.base_dados = base_dados
        self.usuario = usuario
        self.senha = senha
        self.class_driver = class_driver
    
    def __str__(self):
        return f"VO_Conexao [sgbd={self.sgbd} baseDados={self.base_dados}, " \
               f"host={self.host}, porta={self.porta}, senha={self.senha}, " \
               f"usuario={self.usuario}, ClassDriver={self.class_driver}]"
    
    def __eq__(self, other):
        if not isinstance(other, VoConexao):
            return False
        return (self.sgbd == other.sgbd and self.host == other.host and 
                self.porta == other.porta and self.base_dados == other.base_dados and
                self.usuario == other.usuario and self.senha == other.senha and
                self.class_driver == other.class_driver)
