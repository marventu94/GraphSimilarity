from pymongo import MongoClient
from config import Config
import hashlib
import datetime
import jwt

#Servicio de autenticación para manejar login, API keys y validación.
class AuthService:

    def __init__(self):
        #Inicializa conexión con MongoDB.
        self.client = MongoClient(Config.MONGO_CLIENT_URL)
        self.db = self.client[Config.MONGO_DB_NAME]
        self.users_collection = self.db[Config.MONGO_USERS_COLLECTION]

    @staticmethod
    def hash_password_md5(password):
        #Genera el hash MD5 de una contraseña.#
        return hashlib.md5(password.encode('utf-8')).hexdigest()

    def authenticate(self, username, password):
        #Autentica al usuario y genera un JWT si las credenciales son válidas.
        user = self.users_collection.find_one({"username": username})
        if not user:
            return None

        hashed_password = self.hash_password_md5(password)
        if hashed_password != user["password"]:
            return None
        
        api_key = jwt.encode(
            {
                "username": username,
                "subscription_type": user["subscription_type"],
                "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)
            },
            Config.SECRET_KEY,
            algorithm=Config.JWT_ALGORITHM
        )
        return api_key

    def validate_api_key(self, api_key):
        #Valida un JWT y devuelve su payload si es válido.
        try:
            payload = jwt.decode(api_key, Config.SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
