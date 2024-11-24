import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecret')
    JWT_ALGORITHM = 'HS256'
    FREEMIUM_LIMIT = 5  # Requests per minute
    PREMIUM_LIMIT = 50  # Requests per minute  
    LOGGER_SERVICE_URL = os.getenv("LOGGER_SERVICE_URL", "http://localhost:5002/log-and-process")
    MONGO_USERNAME = os.getenv('MONGO_USERNAME', 'root')
    MONGO_PASSWORD = os.getenv('MONGO_PASSWORD', 'rootpassword')
    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT = os.getenv("MONGO_PORT", "27017")
    MONGO_CLIENT_URL = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"
    MONGO_DB_NAME = "graph_similarity"
    MONGO_USERS_COLLECTION = "users"