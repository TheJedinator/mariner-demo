import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


class PermissionBase(BaseModel):
    type: str
    display_name: str


class PermissionCreate(PermissionBase):
    type: str
    display_name = str


class Permission(PermissionBase):
    id: int
    type: str
    display_name = str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    family_name: str
    given_name: str
    birthdate: datetime.date
    email: str


class UserCreate(UserBase):
    family_name: str
    given_name: str
    birthdate: datetime.date
    email: str


class User(UserBase):
    id: int
    family_name: str
    given_name: str
    birthdate: datetime.date
    email: str
    permissions: Optional[List[Permission]]
    deleted: bool

    class Config:
        orm_mode = True


class PermissionInstance(BaseModel):
    type: str
    granted_date: datetime.date
    display_name: str
    id: int
