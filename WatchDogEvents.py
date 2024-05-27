from watchdog.events import FileSystemEvent, FileSystemEventHandler
from Utils import Utils
from Database import Database
import os
from dotenv import load_dotenv
load_dotenv()




# Classe que trata os eventos de modificação
class WatchDogEvents(FileSystemEventHandler):

    # Método de inicialização da classe
    def __init__(self) -> None:
        super().__init__()
        # Instância de conexão com Banco de Dados
        self.db = Database()
        # Variável auxiliar para evitar execução duplicada
        self.last_event = None
        self.__find_legacy()

    def __find_legacy(self):
        Utils.log("Procurando arquivos legados.")
        try:
            for root, _, files in os.walk(os.getenv("FOLDER_PATH")):
                for file in files:
                    if ".vehicleBody.jpg" in file:

                        path = os.path.join(root, file)
                        sql = Utils.filter_sql_created_file(path)
                        if self.db.execute(sql, "insert"):
                            if Utils.rename_file(path, path.replace('.vehicleBody', '')):
                                Utils.log(fr"{path.replace('.vehicleBody', '')} finalizado com sucesso.")

        except Exception as e:
            Utils.log(f"Erro __find_legacy(): {e}")
   
    # Quando um arquivo é criado, essa função é chamada
    def on_created(self, event):
        Utils.log(f"Iniciando on_created() - {event.src_path}")
        try:
            # Verifica se o evento é um arquivo e se o arquivo é uma imagem
            if not event.is_directory and self.last_event != event.src_path and ".jpg" in event.src_path:
                self.last_event = event.src_path
                # Filtra o caminho do arquivo e monta a query SQL
                sql = Utils.filter_sql_created_file(event.src_path)
                # Executa a query SQL
                if self.db.execute(sql, "insert"):
                    # Renomeia o arquivo
                    if Utils.rename_file(event.src_path, event.src_path.replace('.vehicleBody', '')):
                        Utils.log(fr"{event.src_path.replace('.vehicleBody', '')} finalizado com sucesso.")
        except Exception as e:
            Utils.log(f"Erro on_created(): {e}")
        
    def on_any_event(self, event: FileSystemEvent) -> None:
        pass