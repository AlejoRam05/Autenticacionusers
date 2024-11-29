from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session
from db import get_session
from models.user_model import ClienteDB, Cliente, ClienteResponse
from utils.hash_utils import HashMethod
from utils.jwt_utils import create_jwt
from utils.csrf_token import generate_csrf_token
import uuid
from datetime import datetime, timedelta

router = APIRouter()
failed_attempts = {}

@router.post("/register", response_model=ClienteResponse, status_code=201)
async def register(cliente: Cliente, db: Session = Depends(get_session)):
    try:
        # Verificar si ya existe un usuario con el mismo email o username
        existe_user = db.query(ClienteDB).filter(
            (ClienteDB.email == cliente.email) & 
            (ClienteDB.username == cliente.username)
        ).first()

        if existe_user:
            raise HTTPException(status_code=404, detail="Email / username ya registrado")

        # Crear el nuevo usuario y guardar en la base de datos
        user = ClienteDB(
            email=cliente.email, 
            password=HashMethod.hash_password(cliente.password), 
            username=cliente.username
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except HTTPException as e:
        raise e
    
@router.post("/login")
async def login(cliente: Cliente, db: Session = Depends(get_session)):
    try:    
        # Verificar si el usuario existe con el email y el username
        existe_user = db.query(ClienteDB).filter(
            (ClienteDB.email == cliente.email) & 
            (ClienteDB.username == cliente.username)
        ).first()

        if not existe_user:
            raise HTTPException(status_code=401, detail="Usuario incorrecto.")
        
        # Verificar si la contraseña es correcta
        if not HashMethod.verify_password(cliente.password, existe_user.password):
            raise HTTPException(status_code=401, detail="Contraseña incorrecta.")

        # Verificar si el usuario está bloqueado debido a intentos fallidos
        if cliente.email in failed_attempts and failed_attempts[cliente.email]["attempts"] >= 5:
            if datetime.now() - failed_attempts[cliente.email]["last_attempt"] < timedelta(minutes=15):
                raise HTTPException(status_code=403, detail="Cuenta bloqueada temporalmente")

            # Resetear el contador de intentos después de 15 minutos
            failed_attempts[cliente.email] = {"attempts": 0, "last_attempt": datetime.now()}

        # Inicializar el diccionario de intentos fallidos para el usuario si no existe
        failed_attempts.setdefault(cliente.email, {"attempts": 0, "last_attempt": datetime.now()})

        # Generar el token JWT
        token = create_jwt(existe_user.email, existe_user.roles)
        session_id = str(uuid.uuid4())
        csrf_token = generate_csrf_token()

        # Crear la respuesta con el token de acceso y establecer la cookie HTTP-only
        response = JSONResponse(content={"access_token": token, "token_type": "bearer"})
        response.set_cookie(key="session_id", value=session_id, httponly=True, secure=True, samesite="Strict")

        # Asignar el token CSRF al usuario
        failed_attempts[cliente.email]["csrf_token"] = csrf_token

        return response
    except HTTPException as e:
        raise e
