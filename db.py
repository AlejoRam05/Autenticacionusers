from sqlmodel import create_engine, SQLModel, Session, text
from typing import Annotated
from fastapi import Depends
from models.user_model import ClienteDB, AdminDB


dbName = 'users.db'
sql_url = f"sqlite:///./{dbName}"
connect_args = {"check_same_thread": False}
engine = create_engine(sql_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    try:
        # Asegurarse de que el modelo TiendaDB está registrado
        SQLModel.metadata.create_all(engine)
        
        # Verificar qué tablas fueron creadas
        with Session(engine) as session:
            tables = session.exec(text("SELECT name FROM sqlite_master WHERE type='table';")).all()
            print("Tablas creadas:", tables)
    
    except Exception as e:
        # Imprimir el error detallado
        print("Error al interactuar con la base de datos:", e)
        raise

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]