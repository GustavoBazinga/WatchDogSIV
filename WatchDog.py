# Importando as bibliotecas necessárias
import time
from watchdog.observers.polling import PollingObserver
from watchdog.observers import Observer
from WatchDogEvents import WatchDogEvents
import os
from Utils import Utils

from dotenv import load_dotenv
load_dotenv()

# Função principal
def main():
    # Pasta que será monitorada
    folder = os.getenv("FOLDER_PATH")

    # Definições Biblioteca watchdog
    observer = Observer()
    watch_dog = WatchDogEvents()
    observer.schedule(watch_dog, folder, recursive=True)
    Utils.log(f"Iniciando monitoramento da pasta {folder}.")
    observer.start()
    # Loop para manter a execução permanente
    try:
        while True:
            time.sleep(1)  # Verifica por eventos a cada segundo
            
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

if __name__ == '__main__':
    Utils.log("Iniciando WatchDog.")
    main()