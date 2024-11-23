import secrets
from fastapi import HTTPException, status

# Función para generar un token CSRF
def generate_csrf_token():
    return secrets.token_urlsafe(32)

# Función para verificar el token CSRF
def verify_csrf_token(token: str, expected_token: str):
    if token != expected_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="CSRF token no válido."
        )
