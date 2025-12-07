from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from schemas.auth import SignupRequest, LoginRequest, TokenResponse
from services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup")
async def signup(data: SignupRequest, db: AsyncSession = Depends(get_db)):
    user, error = await AuthService.signup(db, data)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"message": "User created successfully"}


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    token, error = await AuthService.login(db, data)
    if error:
        raise HTTPException(status_code=401, detail=error)
    return TokenResponse(access_token=token)
