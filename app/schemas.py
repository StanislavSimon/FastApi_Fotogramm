from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class PhotoCreate(BaseModel):
    description: str
    filename: str


class User(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class Photo(BaseModel):
    id: int
    description: str
    filename: str
    user_id: int

    class Config:
        from_attributes = True
