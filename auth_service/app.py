from flask import Flask, jsonify, request
from config import Config
from services.auth_service import AuthService
from services.rate_limiting_service import RateLimitingService
from utils.decorators import token_required
import requests
import jwt

app = Flask(__name__)
app.config.from_object(Config)

auth_service = AuthService()
rate_limiting_service = RateLimitingService()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    api_key = auth_service.authenticate(data.get("username"), data.get("password"))
    if api_key:
        return jsonify({"api_key": api_key}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route('/validate', methods=['GET'])
@token_required
def validate():
    return jsonify({"message": "Access granted"}), 200

@app.route('/detect-similarity', methods=['POST'])
@token_required
def detect_similarity():
    data = request.json
    # Verificar si el cuerpo de la solicitud (data) está presente y si incluye "input"
    if not data or "input" not in data:
        return jsonify({"message": "Input are required"}), 400

    input = data["input"]

    # Decodificar el token JWT para obtener el username
    api_key = request.headers.get("Authorization")
    try:
        decoded_token = jwt.decode(api_key, Config.SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
        username = decoded_token["username"]
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 403

    # URL del microservicio de logger que luego deriva para realizar la consulta del cleinte
    target_url = app.config['LOGGER_SERVICE_URL']

    try:
        # Realizamos la solicitud HTTP al microservicio de cache
        response = requests.post(target_url, json={"input": input, "username": username})

        # Retornamos la respuesta
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"message": "Error connecting to the similarity service", "error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)