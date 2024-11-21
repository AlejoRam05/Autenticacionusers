from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Annotated
from db import create_db_and_tables

jinja2_templates = Jinja2Templates(directory='templates')

app = FastAPI()

@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    return jinja2_templates.TemplateResponse("index.html", {'request': request})

@app.post("users/login")
def login(username: Annotated[str, Form()],email: Annotated[str, Form()], password: Annotated[str, Form()]):
    return{
        "usersname": username,
        "email": email,
        "password": password}

@app.on_event("startup")
def startup_event():
    create_db_and_tables()