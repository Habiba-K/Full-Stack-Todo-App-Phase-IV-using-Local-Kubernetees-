from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from uuid import UUID
from typing import Optional


class SignupRequest(BaseModel):
    """Request schema for user signup"""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, description="User's password (minimum 8 characters)")
    name: Optional[str] = Field(None, max_length=100, description="User's display name")


class SignupResponse(BaseModel):
    """Response schema for successful signup"""
    id: UUID
    email: str
    name: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class SigninRequest(BaseModel):
    """Request schema for user signin"""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")


class UserResponse(BaseModel):
    """Response schema for user information"""
    id: UUID
    email: str
    name: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SigninResponse(BaseModel):
    """Response schema for successful signin"""
    user: UserResponse
    token: str = Field(..., description="JWT access token")
    expires_at: datetime = Field(..., description="Token expiration timestamp")
