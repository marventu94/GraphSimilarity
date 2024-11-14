from flask import Flask, jsonify, request
from services.cache_service import CacheService
from services.neural_service import NeuralService
import requests

app = Flask(__name__)

cache_service = CacheService()
neural_service = NeuralService()

def _validate_input(data):
    """Valida el objeto JSON entrante."""
    # Validar si el JSON tiene el atributo "input"
    if "inputs" not in data:
        return False, {"message": "Invalid input: 'input' field is required"}

    input_data = data["inputs"]

    # Validar que "input" sea un array de longitud máxima 2
    if not isinstance(input_data, list) or not (1 <= len(input_data) <= 2):
        return False, {"message": "Invalid input: 'input' must be a list with 1-2 elements"}

    # Validar cada elemento de "input"
    for idx, item in enumerate(input_data):
        if not isinstance(item, list):
            return False, {"message": f"Invalid input: element at index {idx} must be a list"}

        for sub_idx, sub_item in enumerate(item):
            if not (isinstance(sub_item, list) and len(sub_item) == 2):
                return False, {
                    "message": f"Invalid input: element at input[{idx}][{sub_idx}] must be a list of 2 elements"
                }

            # Validar que cada elemento de la lista interna sea un string
            if not all(isinstance(element, str) for element in sub_item):
                return False, {
                    "message": f"Invalid input: all elements in input[{idx}][{sub_idx}] must be strings"
                }

    return True, None

@app.route('/detect-similarity', methods=['POST'])
def detect_similarity():
    
    data = request.json
    inputs = data.get("inputs")
    
    # Llamar a la función de validación
    is_valid, error = _validate_input(data)
    if not is_valid:
        return jsonify(error), 400
    
    # Verificar si la respuesta ya está en cache
    cached_response = cache_service.get_cached_response(inputs)
    if cached_response:
        return jsonify({"cached": True, "result": cached_response}), 200
    
    # Si no está en cache, llamamos al servicio de redes neuronales
    try:
        response = neural_service.process_similarity(inputs)
        # Guardamos la respuesta en cache para futuras consultas
        cache_service.cache_response(inputs, response)
        return jsonify({"cached": False, "result": response}), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"message": "Error connecting to neural service", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
