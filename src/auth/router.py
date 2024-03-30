

from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
import bcrypt
from sqlalchemy import select
from .models import User
from .utils import get_user_data_by_id, get_validated_token, hash_password, issue_tokens
from src.config.database import get_async_session
from .schemas import UserCreate, UserData, UserLogin, UserAuth, UserTokens
from src.config.routes import routes
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

bearer = HTTPBearer()


router = APIRouter(tags=['auth'])


@router.post(routes['login'], response_model=UserAuth)
async def login(user: UserLogin, session: AsyncSession = Depends(get_async_session)):
		user = user.model_dump()
		stmt = select(User).where(User.email == user['email'])
		suitable_user = await session.scalar(stmt)
		if suitable_user == None:
			raise HTTPException(status_code=404, detail={"message": "User not found", "http_code": 404}) 
		elif bcrypt.checkpw(
			hashed_password=suitable_user.password.encode('utf-8'),
			password=user['password'].encode('utf-8')
		): 
			tokens = await issue_tokens(id=suitable_user.id)
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
		
@router.post(routes['register'], response_model=UserAuth)
async def register(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
		user = user.model_dump()
		old_user = await session.scalar(select(User).where(User.email == user['email']))
		
		if old_user != None:
			raise HTTPException(status_code=403, detail={"http_code": 403, 
																"message": "user already exists"})
		
		hashed_password = await hash_password(password=user['password'])
		new_user = {**user,
				  "password": hashed_password}
		
		user_db = User(**new_user)
		session.add(user_db)
		await session.commit() 
		tokens = await issue_tokens(id=user_db.id)
		
		return {**user, "id": user_db.id, **tokens}


@router.post(routes['auth-by-access-token'], response_model=UserData)
async def auth(access_token:HTTPAuthorizationCredentials = Depends(bearer), session: AsyncSession = Depends(get_async_session)): # access_token: Annotated[str | None, Header()]
		is_validated_token = get_validated_token(token=access_token.credentials, type_is_token="access")
		id = is_validated_token['_id']
		user = await get_user_data_by_id(id=id, session=session)
		return user

@router.post(routes['get-new-tokens'], response_model=UserTokens)
async def get_new_tokens(refresh_token:HTTPAuthorizationCredentials = Depends(bearer)):#refresh_token: Annotated[str | None, Header()]
		is_validated_token = get_validated_token(token=refresh_token.credentials, type_is_token="refresh")
		id = is_validated_token['_id']
		return  await issue_tokens(id=id)
