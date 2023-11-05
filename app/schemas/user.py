from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(..., min_length=6)


class GetUser(BaseModel):
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True
