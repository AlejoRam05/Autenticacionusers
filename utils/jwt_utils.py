from datetime import datetime, timedelta
import jwt
import os 

SECRET_KEY = os.getenv('secret_key')  # Asegúrate de que esté bien definida
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_jwt(email: str, is_admin: bool) -> str:
    payload = {
        "sub": email,
        "is_admin": is_admin,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # Ajusta el tiempo de expiración aquí
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_jwt(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.PyJWTError:
        return None
