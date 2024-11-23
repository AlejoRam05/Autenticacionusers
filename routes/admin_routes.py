from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from db import get_session
from models.user_model import Admin, AdminDB, AdminResponse
from utils.hash_utils import HashMethod
from utils.jwt_utils import create_jwt

router = APIRouter()

@router.post("/admin", response_model=AdminResponse, status_code=201)
async def register(admin: Admin, db: Session = Depends(get_session)):
    try:
        # Verificar si ya existe un admin con el mismo email o username
        existe_user = db.query(AdminDB).filter(
            (AdminDB.email == admin.email) & 
            (AdminDB.username == admin.username)
        ).first()

        if existe_user:
            raise HTTPException(status_code=404, detail="Email / username ya registrado")
        
        # Crear el nuevo admin y guardar en la base de datos
        administrador = AdminDB(
            email=admin.email, 
            password=HashMethod.hash_password(admin.password), 
            username=admin.username
        )
        db.add(administrador)
        db.commit()
        db.refresh(administrador)
        return administrador
    except HTTPException as e:
        raise e

@router.post("/admin/login", status_code=200)
async def login(admin: Admin, db: Session = Depends(get_session)):
    try:    
        # Verificar si el admin existe con el email y el username
        existe_user = db.query(AdminDB).filter(
            (AdminDB.email == admin.email) & 
            (AdminDB.username == admin.username)
        ).first()

        if not existe_user:
            raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos.")
        
        # Verificar si la contraseña es correcta
        if not HashMethod.verify_password(admin.password, existe_user.password):
            raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos.")

        # Generar el token JWT
        token = create_jwt(existe_user.email, existe_user.roles)
        return {"access_token": token, "token_type": "bearer"}

    except HTTPException as e:
        raise e
