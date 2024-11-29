"""MODELO DE QUE DATOS ESTARIA ESPERANDO PARA PROCESAR """
from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import validator

class Cliente(BaseModel):

    username: str
    email: EmailStr
    password: str
    roles: bool = Field(default=False)

    @validator('username')
    def validate_username(cls, username):
        if any(char in username for char in ['<', '>','&', '"', "'"]):
            raise ValueError('El nombre de usuario no puede contener caracteres especiales.')
        return username
class Admin(BaseModel):

    username: str
    email: EmailStr
    password: str


class ClienteResponse(BaseModel):

    username: str
    email: EmailStr
    


class AdminResponse(BaseModel):

    username: str
    email: EmailStr
    roles: bool


class ClienteDB(SQLModel, table = True):

    id: Optional[int] = Field(primary_key=True, default=None)
    username: str = Field(unique=True)
    email: str = Field(index=True, unique=True)
    password: str  
    roles: bool = Field(default= False)

class AdminDB(SQLModel, table = True):

    id: Optional[int] = Field(primary_key=True, default=None)
    username: str = Field(unique=True)
    email: str = Field(index=True, unique=True)
    password: str  
    roles: bool = Field(default= True)