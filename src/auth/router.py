

from typing import Annotated
from src.config.database import get_async_session
from src.auth.repository import AuthRepository
from src.auth.schemas import UserCreate, UserData, UserLogin, UserAuth, UserTokens
from src.config.routes import routes
from fastapi import APIRouter, Header, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

bearer = HTTPBearer()


router = APIRouter(tags=['auth'])


@router.post(routes['login'], response_model=UserAuth)
async def login(user: UserLogin, session=Depends(get_async_session)):
	return await AuthRepository.login(user=user.model_dump(), session=session)

@router.post(routes['register'], response_model=UserAuth)
async def register(user: UserCreate, session=Depends(get_async_session)):
	return await AuthRepository.register(user=user.model_dump(), session=session)


@router.post(routes['auth-by-access-token'], response_model=UserData)
async def auth(access_token:HTTPAuthorizationCredentials = Depends(bearer)): # access_token: Annotated[str | None, Header()]
	return await AuthRepository.auth(access_token=access_token.credentials)


@router.post(routes['get-new-tokens'], response_model=UserTokens)
async def get_new_tokens(refresh_token:HTTPAuthorizationCredentials = Depends(bearer)):#refresh_token: Annotated[str | None, Header()]
	return await AuthRepository.get_new_tokens(refresh_token=refresh_token.credentials)
