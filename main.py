from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import random

app = FastAPI()
templates = Jinja2Templates(directory="templates")

#TODO Вынести в файл config
ADMIN_NAME = "admin"
PASSWORD = "admin"
UNAUTHENTICATED = "unauthenticated"
AUTHENTICATED = "authenticated"

#TODO Вынести в файл messages
ERROR_MESSAGE = "Неверный логин или пароль"

cookies = {ADMIN_NAME: UNAUTHENTICATED}


def authenticate_user(username: str, password: str):
    return username == ADMIN_NAME and password == PASSWORD


@app.get("/", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    global cookies
    if cookies.get(ADMIN_NAME) == AUTHENTICATED:
        cookies[ADMIN_NAME] = UNAUTHENTICATED
        return templates.TemplateResponse("login.html", {"request": request})

    if not authenticate_user(username, password):
        return templates.TemplateResponse("login.html", {"request": request, "error": ERROR_MESSAGE})

    cookies[ADMIN_NAME] = AUTHENTICATED

    random_code = random.randint(a=1000, b=9999)
    return templates.TemplateResponse("random_code.html", {"request": request, "random_code": random_code})
