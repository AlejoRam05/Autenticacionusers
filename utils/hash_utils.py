# Funcion de Hash para usarlo en la DB
import hashlib
from bcrypt import checkpw

def hsh_password(password: str) -> str:
    password_bytes = password.encode('utf-8') 
    pass_hash = hashlib.sha256(password_bytes)
    return pass_hash.hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    
    verificacion = checkpw(password.encode(), hashed.encode())
    return verificacion