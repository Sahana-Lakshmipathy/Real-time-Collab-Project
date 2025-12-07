from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.users import User
from schemas.users import UserCreate, UserUpdate


class UserService:

    @staticmethod
    async def create_user(db: AsyncSession, data: UserCreate):
        user = User(
            id=data.id,
            username=data.username,
            email=data.email,
            avatar_url=data.avatar_url,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user


    @staticmethod
    async def get_user(db: AsyncSession, user_id: str):
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalars().first()


    @staticmethod
    async def update_user(db: AsyncSession, user_id: str, data: UserUpdate):
        user = await UserService.get_user(db, user_id)
        if not user:
            return None

        if data.username is not None:
            user.username = data.username
        if data.avatar_url is not None:
            user.avatar_url = data.avatar_url

        await db.commit()
        await db.refresh(user)
        return user
