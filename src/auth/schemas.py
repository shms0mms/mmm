

from typing import List
from pydantic import BaseModel, EmailStr, Field

from src.account.schemas import Account
from .enum import RoleEnum, SexEnum

class UserTokens(BaseModel):
	refresh_token: str | bytes 
	access_token: str | bytes

class UserCreate(BaseModel):
	username: str = Field(min_length=8)
	password: str = Field(min_length=8)
	email: EmailStr 
	sex: SexEnum
	role: RoleEnum
	age: int 

class UserData(BaseModel):
	id: int
	username: str = Field(min_length=8)
	email: EmailStr 
	sex: SexEnum
	role: RoleEnum
	age: int
class UserAuth(UserData, UserTokens):
	pass

class UserLogin(BaseModel):
	email: EmailStr
	username: str = Field(min_length=8)
	password: str = Field(min_length=8)


