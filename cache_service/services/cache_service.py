import redis
import json
from config import Config

class CacheService:
    def __init__(self):
        self.client = redis.Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, decode_responses=True)

    def get_cached_response(self, inputs):
        # Convertir los inputs a una clave única para Redis
        cache_key = self._generate_cache_key(inputs)
        response = self.client.get(cache_key)
        
        if response:
            # Convertir de JSON a un diccionario y retornar
            return json.loads(response)
        return None

    def cache_response(self, inputs, response):
        # Convertir los inputs a una clave única para Redis
        cache_key = self._generate_cache_key(inputs)
        # Almacenar la respuesta en caché con una validez de 1 día
        self.client.setex(cache_key, Config.CACHE_EXPIRY, json.dumps(response))

    def _generate_cache_key(self, inputs):
        # Genera una clave única basada en los inputs
        return f"similarity:{json.dumps(inputs, sort_keys=True)}"
