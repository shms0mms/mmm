



from fastapi import Depends, HTTPException
from sqlalchemy import select
from .models import User
from src.config.database import async_session, get_async_session
from .schemas import UserData
from .enum import IsTokenEnum
from src.config.settings import config
from sqlalchemy.ext.asyncio import AsyncSession
import jwt
import bcrypt 


def get_validated_token(token: str, type_is_token: IsTokenEnum, algorithm: str = config.algorithm, secret_key: str = config.secret_key):
	is_token = jwt.decode(jwt=token, algorithms=[algorithm], key=secret_key)
	if is_token:
		if is_token['is_token'] != type_is_token: 
			raise HTTPException(status_code=403, detail={
			"message": "Token is not a valid",
			"http_code": 403
		})
	
	return is_token

def hash_password(password: str):
	return bcrypt.hashpw(salt=bcrypt.gensalt(), password=password.encode('utf-8')).decode('utf-8')





async def get_user_data_by_id(id: int, session: AsyncSession = Depends(get_async_session)) -> UserData:
	stmt = select(User).where(User.id == id)
	user = await session.scalar(stmt)
	if user == None:
		raise HTTPException(status_code=404, detail={"message": "User not found", "http_code": 404}) 
	return {"username": user.username, "email": user.email, "sex": user.sex, "role": user.role, "id": user.id, "age": user.age }
 