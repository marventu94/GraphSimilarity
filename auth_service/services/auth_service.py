import jwt
from config import Config
from models import users_db
import datetime

class AuthService:
    def authenticate(self, username, password):
        user = users_db.get(username)
        if user and user.password == password:
            api_key = jwt.encode(
                {"username": username, "subscription_type": user.subscription_type, "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)},
                Config.SECRET_KEY,
                algorithm=Config.JWT_ALGORITHM
            )
            return api_key
        return None

    def validate_api_key(self, api_key):
        try:
            payload = jwt.decode(api_key, Config.SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
            return payload  # Returns payload with username and subscription type
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
