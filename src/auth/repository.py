
from datetime import datetime, timedelta
import bcrypt
from fastapi import Depends, HTTPException
import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession 

from .models import User
from .utils import  get_user_data_by_id, get_validated_token, hash_password
from .schemas import UserAuth, UserCreate, UserData, UserLogin, UserTokens
from src.config.settings import config
from src.config.database import get_async_session


class AuthRepository:

	@classmethod
	async def register(cls, user: UserCreate, session: AsyncSession):
		old_user = await session.scalar(select(User).where(User.email == user['email']))
		
		
		if old_user != None:
			raise HTTPException(status_code=403, detail={"http_code": 403, 
																"message": "user already exists"})
		
		hashed_password = hash_password(password=user['password'])
		
		new_user = {**user,
				  "password": hashed_password}
		user_db = User(**new_user)
		session.add(user_db)
		await session.commit()
		tokens = await cls.issue_tokens(id=user_db.id)
		return {**user, "id": user_db.id, **tokens}
	# Get Current User Method
	@classmethod
	async def login(cls, user: UserLogin, session: AsyncSession) -> UserAuth:
		stmt = select(User).where(User.email == user['email'])
		suitable_user = await session.scalar(stmt)
		if suitable_user == None:
			raise HTTPException(status_code=404, detail={"message": "User not found", "http_code": 404}) 
		elif bcrypt.checkpw(
			hashed_password=suitable_user.password.encode('utf-8'),
			password=user['password'].encode('utf-8')
		): 
			tokens = await  cls.issue_tokens(id=suitable_user.id)
			return {
				"username": suitable_user.username,
			 	"id": suitable_user.id,
			   "sex": suitable_user.sex,
				"role": suitable_user.role,
				"email": suitable_user.email,
				"age": suitable_user.age, 
				**tokens
				}
		else: 
			raise HTTPException(status_code=403, detail={"message": "password is wrong", "http_code": 403})
		
	@classmethod
	async def auth(cls, access_token: str) -> UserData:
		is_validated_token = get_validated_token(token=access_token, type_is_token="access")
		id = is_validated_token['_id']
		user = await get_user_data_by_id(id=id)
		return user
	
	@classmethod
	async def get_new_tokens(cls, refresh_token: str) -> UserTokens:
		is_validated_token = get_validated_token(token=refresh_token, type_is_token="refresh")
		id = is_validated_token['_id']
		return await cls.issue_tokens(id=id)
	@staticmethod
	async def issue_tokens(id: int) -> UserTokens:
		data = {"_id": id}
		access_token = jwt.encode(algorithm=config.algorithm, key=config.secret_key, payload={**data, "exp": datetime.utcnow() + timedelta(minutes=15), "is_token": "access"})
		refresh_token = jwt.encode(algorithm=config.algorithm, key=config.secret_key, payload={**data, "exp": datetime.utcnow() + timedelta(days=7), "is_token": "refresh"})
		return  { "access_token": access_token, "refresh_token": refresh_token }


		