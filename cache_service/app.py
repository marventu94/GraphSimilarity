from flask import Flask, jsonify, request
from services.cache_service import CacheService
from services.neural_service import NeuralService
import requests

app = Flask(__name__)

cache_service = CacheService()
neural_service = NeuralService()

@app.route('/detect-similarity', methods=['POST'])
def detect_similarity():
    data = request.json
    inputs = data.get("inputs")
    
    if not inputs:
        return jsonify({"message": "Inputs are required"}), 400

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
    app.run(debug=True, port=5001)
