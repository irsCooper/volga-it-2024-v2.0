from typing import Optional
import uuid
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession

import jwt

from src.accounts.dao import UserDAO
from src.accounts.service import UserService
from src.accounts.model import UserModel
from src.authentication.utils import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, TOKEN_TYPE_FIELD, decode_jwt, encode_jwt
from src.core.config import settings
from src.core.db_helper import db


http_bearer = HTTPBearer(auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/Authentication/SignIn")


async def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int 
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)

    return await encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes
    )


async def create_token_of_type(
    token_type: str, 
    user: UserModel,
    refresh_id: uuid.UUID | None
) -> str:
    
    jwt_payload = {
        "sub": str(user.id),
    }

    if token_type == ACCESS_TOKEN_TYPE:
        jwt_payload.update({
            "user_name": user.user_name,
            "active": user.active,
        })

        expire_minutes = settings.auth_jwt.access_token_expire_minutes 
        
    else:
        jwt_payload.update({
            "id": refresh_id, 
        })

        expire_minutes: int = settings.auth_jwt.refresh_token_expire_days * 60 * 24

    return await create_jwt(
        token_type=token_type,
        token_data=jwt_payload,
        expire_minutes=expire_minutes
    )


async def validate_token_type(
    payload: dict, 
    token_type: str
) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True 
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type {current_token_type!r} expected {token_type!r}"
    )


# async def get_current_token_payload(token: str):
#     try:
#         payload = await decode_jwt(token)
#     except jwt.InvalidTokenError as e:
#         print(e)
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="invalid token error"
#         )
#     return payload  


async def get_user_by_token_sub(
    payload: dict, 
    session: AsyncSession
) -> Optional[UserModel]:
    user_id = payload.get("sub")
    user: UserModel = await UserService.get_user(user_id=user_id, session=session) 
    if user:
        return user 
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid token"
    )


async def get_current_auth_user_of_type_token(
    token: str,
    token_type: str,
    session: AsyncSession
):
    try:
        payload: dict = await decode_jwt(token)

        await validate_token_type(
            payload=payload,
            token_type=token_type
        )

        return await get_user_by_token_sub(
            payload=payload,
            session=session
        )
        
    except jwt.InvalidTokenError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token error"
        )

    


async def get_from_oauth2_current_auth_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db.session_dependency)
) -> Optional[UserModel]:
    return await get_current_auth_user_of_type_token(
        token=token,
        token_type=ACCESS_TOKEN_TYPE,
        session=session
    )


