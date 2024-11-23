from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from db import create_db_and_tables
from routes import auth_routes, admin_routes, dashboard

jinja2_templates = Jinja2Templates(directory='templates')

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