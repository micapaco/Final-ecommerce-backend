"""
Authentication schemas for login and registration.
"""
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """Schema for login request."""
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., min_length=4, description="User password")


class RegisterRequest(BaseModel):
    """Schema for registration request."""
    name: str = Field(..., min_length=1, max_length=100, description="First name")
    lastname: str = Field(..., min_length=1, max_length=100, description="Last name")
    email: EmailStr = Field(..., description="Email address")
    password: str = Field(..., min_length=4, description="Password")
    telephone: Optional[str] = Field(None, description="Phone number")


class AuthResponse(BaseModel):
    """Schema for authentication response."""
    id: int
    name: str
    lastname: str
    email: str
    telephone: Optional[str] = None
    is_admin: bool = False
    message: str = "Autenticación exitosa"


class RegisterResponse(BaseModel):
    """Schema for registration response."""
    id: int
    name: str
    lastname: str
    email: str
    is_admin: bool = False
    message: str = "Usuario registrado exitosamente"
