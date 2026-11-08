from pydantic import BaseModel

class Registration(BaseModel):
    email: str
    password: str
    username: str

class Login(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    username: str
    email: str