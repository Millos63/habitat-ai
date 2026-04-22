import re

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.models.user import UserRole


class RegisterRequest(BaseModel):
    """Payload for user registration."""

    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=2, max_length=255)
    phone: str | None = Field(default=None, max_length=20)
    role: UserRole = UserRole.CLIENT

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        normalized = " ".join(value.strip().split())
        if len(normalized) < 2:
            raise ValueError("Full name must be at least 2 characters")
        return normalized

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one number")
        return value


class LoginRequest(BaseModel):
    """Payload for user login."""

    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    @field_validator("password")
    @classmethod
    def validate_login_password_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Password cannot be blank")
        return value


class AuthResponse(BaseModel):
    """JWT token response."""

    access_token: str
    token_type: str = "bearer"
    user_id: str
