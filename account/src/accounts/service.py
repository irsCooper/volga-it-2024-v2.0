
from typing import Optional
import uuid

from fastapi import HTTPException, status
from sqlalchemy import and_ 

from src.accounts.schemas import ROLE_DOCTOR, UserUpdate, UserUpdateAdmin, UserUpdateDB
from src.accounts.model import  UserModel
from src.authentication.utils import hash_password
from src.accounts.dao import UserDAO
from src.accounts.schemas import UserCreate, UserCreateAdmin, UserCreateDB
from src.dependencies import delete_timetable_doctor

from sqlalchemy.ext.asyncio import AsyncSession

class UserService:
    @classmethod
    async def create_user(
        cls,
        user_in: UserCreate | UserCreateAdmin,
        session: AsyncSession
    ) -> Optional[UserModel]:
        hashed_password = await hash_password(user_in.password)

        return await UserDAO.add(
            session=session,
            obj_in=UserCreateDB(
                **user_in.model_dump(exclude={"password"}),
                hashed_password=hashed_password,
            )
        )
    

    @classmethod
    async def get_user(
        cls, 
        user_id: uuid.UUID, 
        session: AsyncSession
    ) -> UserModel:
        user = await UserDAO.find_one_or_none(
            session,
            UserModel.id == user_id,
        )
        if not user or not user.active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        if not user.refresh_session:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorization"
            )
        return user
    

    @classmethod
    async def get_list_users(
        cls, 
        offset: int, 
        limit: int, 
        session: AsyncSession
    ):  
        return await UserDAO.find_all(
            session,
            UserModel.active == True,
            offset=offset,
            limit=limit
        )
    

    @classmethod
    async def update_user(
        cls,
        user_id: uuid.UUID,
        user: UserUpdate | UserUpdateAdmin,
        session: AsyncSession
    ):
        if isinstance(user, UserUpdateAdmin):
            current_user = await cls.get_user(user_id, session)
            if ROLE_DOCTOR not in current_user.roles and ROLE_DOCTOR not in [role.name_role for role in user.roles]:
                await delete_timetable_doctor(current_user.id)
                
        user_update = await UserDAO.update(
            session,
            and_(UserModel.id == user_id, UserModel.active == True),
            obj_in=UserUpdateDB(
                **user.model_dump(exclude={"password", "user_name"}),
                hashed_password=await hash_password(user.password)
            )
        )

        if not user_update:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return user_update
    

    @classmethod
    async def delete_user(
        cls,
        user_id: uuid.UUID,
        session: AsyncSession
    ):
        user = await cls.get_user(user_id, session)

        await UserDAO.update(
            session,
            UserModel.id == user.id,
            obj_in={"active": False}
        )
