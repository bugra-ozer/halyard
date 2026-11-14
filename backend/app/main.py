import datetime
from fastapi import FastAPI
from app.constant import constant as con
from app.core import logger
import logging
from sqlalchemy.orm import Session
from app.schemas.auth import Registration, UserResponse, Login
from app.db.session import get_db
from app.db.crud import create_user, get_user_by_username, get_user_by_email
from fastapi import Depends
from passlib.context import CryptContext
from fastapi import HTTPException
from jose import jwt

app=FastAPI()
log_handler=logger.LogHandler()
logger=logging.getLogger(__name__)

@app.get(con.HEALTH_ROUTE)
def health():
    return {con.KEY_STATUS: con.KEY_OK}


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "secret-key"
ALGORITHM = "HS256"

def create_access_token(username: str):
    payload = {"sub": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(days = 30)}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

@app.post("/register", response_model=UserResponse)
def register_user(registration: Registration, db: Session = Depends(get_db)):
    user = get_user_by_username(db, registration.username)
    email = get_user_by_email(db, registration.email)
    if user:
        raise HTTPException(status_code=400, detail="Username already registered")
    if email:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(registration.password)
    created_user = create_user(db, registration, hashed_password)
    return created_user


@app.post("/login")
def login_user(login: Login, db: Session = Depends(get_db)):
    user = get_user_by_username(db, login.username)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not pwd_context.verify(login.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = create_access_token(user.username)
    return {"access_token": token, "token_type": "bearer"}