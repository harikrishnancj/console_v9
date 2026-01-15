from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    name: str  # Input name, maps to username in model
    email: str


class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None  # Maps to username in model
    password: Optional[str] = None

class UserInDBBase(BaseModel):
    user_id: int
    username: str  # Match the model field name
    email: str
    is_active: bool
    tenant_id: int

    class Config:
        from_attributes = True
