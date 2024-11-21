"""MODELO DE QUE DATOS ESTARIA ESPERANDO PARA PROCESAR """
from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field
from typing import Optional

class Cliente(BaseModel):

    username: str
    email: EmailStr
    password: str

class ClienteDB(SQLModel, table = True):

    id: Optional[int] = Field(primary_key=True, default=None)
    username: str
    email: str = Field(index=True, unique=True)
    password: str  
    roles: bool = Field(default= False)