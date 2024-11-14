import logging
import os

class LoggerService:
    def __init__(self, log_file="logs/service.log"):
        # Crear la carpeta de logs si no existe
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        # Configurar el logger
        self.logger = logging.getLogger("LoggerService")
        self.logger.setLevel(logging.INFO)

        # Crear un FileHandler para guardar los logs en un archivo
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)

        # Formato de los mensajes de log
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Añadir el handler al logger
        self.logger.addHandler(file_handler)

    def log_entry(self, username, inputs, start_time):
        self.logger.info(f"Request received - User: {username}, Inputs: {inputs}, Start Time: {start_time}")

    def log_exit(self, username, inputs,response , start_time, end_time):
        self.logger.info(f"Request processed - User: {username}, Inputs: {inputs}, Response: {response.json()} Start Time: {start_time}, End Time: {end_time}")
