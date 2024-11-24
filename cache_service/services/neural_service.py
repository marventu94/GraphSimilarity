import requests
from config import Config

class NeuralService:
    def process_similarity(self, input):
        response = requests.post(Config.NEURAL_SERVICE_URL, json={"input": input})
        return response.json()
