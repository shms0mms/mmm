

from enum import Enum
from pydantic import BaseModel
from src.config.config import JWT_SECRET


class AuthSettings(BaseModel):
	secret_key: str  = JWT_SECRET
	algorithm: str = "HS256"


class Config(AuthSettings):
	pass 

config = AuthSettings()