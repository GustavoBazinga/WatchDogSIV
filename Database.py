# Importando as bibliotecas necessárias
import os
import mysql.connector as mysql
from Utils import Utils

# Carregando as variáveis de ambiente
from dotenv import load_dotenv
load_dotenv()

# Classe para gerenciar a conexão com o banco de dados
class Database():
    # Método de inicialização da classe
    def __init__(self) -> None:
        Utils.log("Iniciando conexão com o banco de dados.")
        # Carregando as informações de conexão do banco de dados das variáveis de ambiente
        self.host = os.getenv("DB_HOST")     
        self.database = os.getenv("DB_DATABASE")
        self.user = os.getenv("DB_USERNAME")
        self.password = os.getenv("DB_PASSWORD")

        if not self.__test():
            raise Exception("Erro ao conectar ao banco de dados.")

    def __test(self):
        try:
            self.connect()
            self.disconnect()
        except Exception as e:
            return False
        else:
            return True


    # Método para conectar ao banco de dados
    def connect(self):
        # Estabelecendo a conexão
        self.connection = mysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        # Criando um cursor para executar consultas SQL
        self.cursor = self.connection.cursor()

    # Método para executar uma consulta SQL
    def execute(self, sql: str, type):
        try:
            # Conectando ao banco de dados
            self.connect()
            # Executando a consulta
            self.cursor.execute(sql)
            if type == "select":
                # Retornando todos os resultados
                return self.fetchall()
            elif type == "insert":
                # Commitando as alterações
                self.connection.commit()
            elif type == "one":
                # Retornando o primeiro resultado
                return self.fetchone()
        except Exception as e:
            Utils.log(f"Erro execute(): {e}")
            # Rollback em caso de erro
            self.connection.rollback()
        else:
            return True
        finally:
            # Desconecta do banco de dados
            self.disconnect()

    # Método para buscar todos os resultados de uma consulta
    def fetchall(self):
        # Retornando todos os resultados
        return self.cursor.fetchall()
    
    # Método para buscar o primeiro resultado de uma consulta
    def fetchone(self):
        # Retornando o primeiro resultado
        return self.cursor.fetchone()
        
    # Método para desconectar do banco de dados
    def disconnect(self):
        # Fechando a conexão
        self.connection.close()