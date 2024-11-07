from functools import wraps
from flask import request, jsonify
from services.auth_service import AuthService
from services.rate_limiting_service import RateLimitingService

auth_service = AuthService()
rate_limiting_service = RateLimitingService()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Obtener el token de la cabecera de autorización
        token = request.headers.get('Authorization')
        
        # Verificar si el token existe
        if not token:
            return jsonify({"message": "Token is missing!"}), 403

        # Validar el token
        user_data = auth_service.validate_api_key(token)
        if not user_data:
            return jsonify({"message": "Invalid or expired token!"}), 403

        # Verificar si el usuario está dentro del límite de solicitudes
        if not rate_limiting_service.is_request_allowed(token):
            return jsonify({"message": "Request limit exceeded. Please try again later."}), 429

        # Si todo está bien, continuar con la solicitud
        return f(*args, **kwargs)
    
    return decorated
