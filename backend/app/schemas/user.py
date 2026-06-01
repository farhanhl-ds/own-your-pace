import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator


class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        if not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError("Username hanya boleh huruf, angka, underscore, dan dash")
        if len(v) < 3 or len(v) > 50:
            raise ValueError("Username harus 3-50 karakter")
        return v.lower()

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password minimal 8 karakter")
        return v


class UserResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    email: str
    username: str
    timezone: str
    unit_preference: str
    created_at: datetime


class UserUpdate(BaseModel):
    timezone: str | None = None
    unit_preference: str | None = None
