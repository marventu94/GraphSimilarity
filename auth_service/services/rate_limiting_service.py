from config import Config
from time import time
import jwt

class RateLimitingService:
    def __init__(self):
        self.requests = {}

    def is_request_allowed(self, api_key):
        # Decodificamos el token JWT para obtener el nombre de usuario y el tipo de suscripción
        user_data = jwt.decode(api_key, Config.SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
        username = user_data["username"]
        subscription_type = user_data["subscription_type"]
        
        # Definimos el límite de solicitudes basado en el tipo de suscripción
        limit = Config.FREEMIUM_LIMIT if subscription_type == "FREEMIUM" else Config.PREMIUM_LIMIT

        current_time = time()
        
        # Inicializamos la lista de solicitudes si el usuario no ha hecho ninguna
        if username not in self.requests:
            self.requests[username] = []

        # Filtramos las solicitudes para conservar solo las que se realizaron en el último minuto
        self.requests[username] = [req for req in self.requests[username] if current_time - req < 60]
        
        # Verificamos si el usuario está dentro del límite de solicitudes
        if len(self.requests[username]) < limit:
            self.requests[username].append(current_time)
            return True
        return False
