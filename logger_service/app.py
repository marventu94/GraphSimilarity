from flask import Flask, jsonify, request
from config import Config
from services.logger_service import LoggerService
from datetime import datetime
import requests

app = Flask(__name__)
app.config.from_object(Config)

logger_service = LoggerService()

@app.route('/log-and-process', methods=['POST'])
def log_and_process():
    # Extraer datos de la solicitud
    data = request.json
    username = data.get("username")
    input = data.get("input")
    
    if not username or not input:
        return jsonify({"message": "Input are required"}), 400

    # Llamada al microservicio de cache
    cache_url = app.config['CACHE_SERVICE_URL']

    # Registrar la hora de entrada
    start_time = datetime.now().strftime(app.config['DATE_FORMAT'])
    try:
        # Registrar el log de entrada
        logger_service.log_entry(username, input, start_time)

        # Hacer la solicitud al microservicio de cache
        response = requests.post(cache_url, json={"input": input})

        if response.status_code != 200:
            return jsonify({"message": "The service is not responding as expected", "error": response.reason}), 500    
        
        # Registrar la hora de salida
        end_time = datetime.now().strftime(app.config['DATE_FORMAT'])

                
        # Registrar el log de salida
        logger_service.log_exit(username, input, response, start_time, end_time)

        # Devolver la respuesta del microservicio de cache
        return jsonify(response.json()), response.status_code
        
    except requests.exceptions.RequestException as e:
        return jsonify({"message": "Error on cache or neuronal services", "error": str(e)}), 500

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True, host='0.0.0.0', port=5002)
