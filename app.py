from fastapi import FastAPI
from db import create_db_and_tables
from routes import auth_routes, admin_routes, dashboard


app = FastAPI()

app.include_router(auth_routes.router)
app.include_router(admin_routes.router)
app.include_router(dashboard.router)

@app.get("/")
def home():
    return {"message": "Welcome to the AuthApp"}

@app.on_event("startup")
def startup_event():
    create_db_and_tables()