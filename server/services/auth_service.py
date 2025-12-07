from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.users import User
from utils.security import hash_password, verify_password
from utils.jwt_handler import create_access_token
from schemas.auth import SignupRequest, LoginRequest


class AuthService:

    @staticmethod
    async def signup(db: AsyncSession, data: SignupRequest):
        # Check duplicate ID
        result = await db.execute(select(User).where(User.id == data.id))
        if result.scalars().first():
            return None, "User already exists"

        user = User(
            id=data.id,
            username=data.username,
            email=data.email,
            avatar_url=data.avatar_url,
            password_hash=hash_password(data.password)
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)

        return user, None

    @staticmethod
    async def login(db: AsyncSession, data: LoginRequest):
        result = await db.execute(select(User).where(User.id == data.id))
        user = result.scalars().first()

        if not user:
            return None, "Invalid user ID"

        if not verify_password(data.password, user.password_hash):
            return None, "Invalid password"

        # Create JWT
        token = create_access_token({"sub": user.id})

        return token, None
