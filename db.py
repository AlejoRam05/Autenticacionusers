from sqlmodel import create_engine, SQLModel, Session
from typing import Annotated
from fastapi import Depends


dbName = 'users.db'
sql_url = f"sqlite:///./{dbName}"
connect_args = {"check_same_thread": False}
engine = create_engine(sql_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]