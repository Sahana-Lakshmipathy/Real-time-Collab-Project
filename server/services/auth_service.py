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
        login_value = data.login

        # Try to match username OR email
        stmt = (
            select(User)
            .where((User.username == login_value) | (User.email == login_value))
        )
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            return None, "Invalid credentials"

        # Check password
        if not verify_password(data.password, user.password_hash):
            return None, "Invalid credentials"

        # Generate JWT
        token = create_access_token({"sub": user.id})
        return token, None


