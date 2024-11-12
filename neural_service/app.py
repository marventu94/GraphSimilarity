from flask import Flask, jsonify, request
from model import predict_similarity, initialization_model

app = Flask(__name__)

# Inicializar model y triples_factory en el momento que se ejecuta el microservicio
initialization_model()

@app.route('/process', methods=['POST'])
def process():
    data = request.json

    # Verificar si el cuerpo de la solicitud (data) está presente y si incluye "inputs"
    if not data or "inputs" not in data:
        return jsonify({"message": "Inputs are required"}), 400

    inputs = data["inputs"]

    # Llamar al modelo simulado para obtener la probabilidad de similitud
    response = predict_similarity(inputs)
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True, port=5003)
