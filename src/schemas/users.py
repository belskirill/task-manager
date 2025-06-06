from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


class UsersRegistrationDTO(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    login: str
    email: EmailStr
    number_phone: Optional[str] = None
    password: str


class UserDTO(BaseModel):
    id: int
    first_name: str
    last_name: str
    login: str
    email: EmailStr
    number_phone: str
    created_at: datetime
    updated_at: datetime
    is_verification: bool

    model_config = ConfigDict(from_attributes=True)

