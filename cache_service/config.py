import os

class Config:
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    NEURAL_SERVICE_URL = os.getenv("NEURAL_SERVICE_URL", "http://localhost:5003/process")
    CACHE_EXPIRY = 86400  # 1 día en segundos
