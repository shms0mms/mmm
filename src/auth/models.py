from typing import  List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from .enum import RoleEnum, SexEnum
from src.config.metadata import Base

class Account(Base):
	__tablename__ = 'account'
	account_number: Mapped[str] = mapped_column(String(length=16))
	balance: Mapped[float]
	user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
	user: Mapped[List["User"]] = relationship(uselist=True, back_populates="accounts", lazy='selectin')

class User(Base):
	__tablename__ = 'user'
	username: Mapped[str] 
	email: Mapped[str] = mapped_column(unique=True)
	password: Mapped[str | bytes] = mapped_column(String(length=1024))
	role: Mapped[RoleEnum] 
	sex: Mapped[SexEnum] 
	age: Mapped[int] 
	accounts: Mapped[List["Account"]] = relationship(uselist=True, back_populates="user", lazy='selectin')



	