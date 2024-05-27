import datetime
import os

class Utils():

    # Função para registrar logs
    @staticmethod
    def log(msg):
        now = datetime.datetime.now()
        with open("log.log", "a") as file:
            file.write(f"{now} - {msg}\n")
        print(f"{now} - {msg}")

    # Função que será executada quando houver modificações
    @staticmethod
    def filter_sql_created_file(file_path: str):
        try:
            if 'LPR' in file_path:
                path = file_path.split(fr'LPR', 1)[1]
                path = path[1:]
                subpath = path.split('\\')
        
                if len(subpath) >= 2:
                    plate = subpath[0]
                    date_and_color = subpath[1].split('&')
        
                    if len(date_and_color) >= 2:
                        date = date_and_color[0]
                        color = date_and_color[1].replace(".vehicleBody.jpg", "")
                        return Utils.mount_sql(["plate", "color", "entry_date", "file"], [plate, color, date, path.replace("\\", "/")])
                    else:
                        raise Exception("Data e cor em formato incorretos.")
                else:
                    raise Exception("Erro no filtro do caminho.")
            else:
                raise Exception("Erro no filtro do caminho.")
        except Exception as e:
            Utils.log(f"Erro filter_sql_created_file(): {e}")
            return None

    # Função que envia os valores para o banco de dados
    @staticmethod
    def mount_sql(keys:tuple[str], values:tuple[str]):
        try:
            # Monta a query SQL
            sql = f"INSERT INTO parkings ({', '.join(keys)}) VALUES ({', '.join([f'"{value}"' for value in values])})"
            sql = sql.replace('.vehicleBody', '')
        except Exception as e:
            Utils.log(f"Erro mount_sql(): {e}")
        else:
            return sql
        
    # Função para renomear um arquivo
    @staticmethod
    def rename_file(old_name: str, new_name: str):
        try:
            os.rename(old_name, new_name)
        except Exception as e:
            Utils.log(f"Erro rename_file(): {e}")
        else:
            return True
