from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from typing import Annotated
from sqlmodel import Session
from db import get_session
from models.user_model import AdminDB,ClienteDB
from utils.jwt_utils import verify_jwt

router = APIRouter(prefix="/dashboard")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/admin", status_code=200)
async def dashboard_admin(token: Annotated[str, Depends(oauth2_scheme)], db_admin: Session = (Depends(get_session))):
    try:
        data_verify = verify_jwt(token)
        if data_verify:
            data_admin = db_admin.query(AdminDB).all()
            data_clientes = db_admin.query(ClienteDB).all()
            return {"admin": data_admin, "clientes": data_clientes}
    except HTTPException as e:
        raise e

@router.get("/user/{username}", status_code=200)
async def dashboard_user(username: str, token: Annotated[str, Depends(oauth2_scheme)], db_cliente: Session = Depends(get_session)):
    try:
        data_verify = verify_jwt(token)
        if data_verify:
            data_user = db_cliente.query(ClienteDB).filter(ClienteDB.username == username).first()
            if not data_user:
                raise HTTPException(status_code=404, detail="User not found")
            return {"username": data_user.username}

    except HTTPException as e:
        raise e



