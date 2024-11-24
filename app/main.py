from fastapi import FastAPI, Depends, Request, Form, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from app import models, database
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

models.Base.metadata.create_all(bind=database.engine)
UPLOAD_DIRECTORY = "uploads"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return RedirectResponse(url="/register")


@app.get("/index")
def index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
async def register(
        request: Request,
        username: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    existing_user = db.query(models.User).filter(models.User.username == username).first()

    if existing_user:
        return templates.TemplateResponse("register.html",
                                          {"request": request, "error": "Имя пользователя уже занято"})

    new_user = models.User(username=username)
    new_user.set_password(password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return RedirectResponse(url="/index", status_code=303)


@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(
        request: Request,
        username: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.username == username).first()

    if user and user.verify_password(password):
        return RedirectResponse(url="/index", status_code=303)

    return templates.TemplateResponse("login.html",
                                      {"request": request, "error": "Неправильное имя пользователя или пароль"})


@app.get("/upload")
def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/upload")
async def upload_photo(
        request: Request,
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())

    return RedirectResponse(url="/index", status_code=303)
