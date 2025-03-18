from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """
    Base user schema with common attributes
    """
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    """
    Schema for user creation
    """
    password: str = Field(..., min_length=8)
    is_superuser: Optional[bool] = False


class UserUpdate(BaseModel):
    """
    Schema for user updates
    """
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None


class UserResponse(UserBase):
    """
    Schema for user responses
    """
    id: int
    is_superuser: bool

    class Config:
        from_attributes = True 