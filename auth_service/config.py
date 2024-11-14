import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecret')
    JWT_ALGORITHM = 'HS256'
    FREEMIUM_LIMIT = 5  # Requests per minute
    PREMIUM_LIMIT = 50  # Requests per minute  
    LOGGER_SERVICE_URL = os.getenv("LOGGER_SERVICE_URL", "http://localhost:5002/log-and-process")
