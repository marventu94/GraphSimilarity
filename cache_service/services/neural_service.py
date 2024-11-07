import requests
from config import Config

class NeuralService:
    def process_similarity(self, inputs):
        response = requests.post(Config.NEURAL_SERVICE_URL, json={"inputs": inputs})
        return response.json()
