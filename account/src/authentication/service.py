from sqlalchemy.ext.asyncio import AsyncSession

from account.src.accounts.dao import UserDAO
from account.src.accounts.model import UserModel
from src.accounts.service import UserService
from src.authentication.schemas import TokenInfo
from src.authentication.utils import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, validate_password
from src.dependencies import create_token_of_type
from src.exceptions.AuthExceptions import InvalidCredentialsException
from src.accounts.schemas import UserCreate


class AuthService:
    @classmethod
    async def create_token_info(cls, user: UserModel) -> TokenInfo:
        return TokenInfo(
            access_token=await create_token_of_type(ACCESS_TOKEN_TYPE, user),
            refresh_token=await create_token_of_type(REFRESH_TOKEN_TYPE, user),
        )


    @classmethod
    async def sign_in(
        cls,
        username: str,
        password: str,
        session: AsyncSession,
    ):
        user = UserDAO.find_one_or_none(
            session,
            username=username
        )

        if user and user.active and await validate_password(user_in.password, user.hashed_password):
            return cls.create_token_info(user)
        
        raise InvalidCredentialsException
    
