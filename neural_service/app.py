from flask import Flask, jsonify, request
from model import initialization_model, predict_similarity

app = Flask(__name__)

# Inicializar model y triples_factory en el momento que se ejecuta el microservicio
initialization_model()

@app.route('/process', methods=['POST'])
def process():
    data = request.json

    # Verificar si el cuerpo de la solicitud (data) está presente y si incluye "input"
    if not data or "input" not in data:
        return jsonify({"message": "Input are required"}), 400

    intput_entity = data["input"]

    try:
        # Llamar al modelo simulado para obtener la probabilidad de similitud
        response = predict_similarity(intput_entity)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"message": "Error connecting to cache service", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
