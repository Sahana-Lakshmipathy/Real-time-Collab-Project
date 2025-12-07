from pydantic import BaseModel


class SignupRequest(BaseModel):
    id: str
    username: str
    email: str | None = None
    avatar_url: str | None = None
    password: str


class LoginRequest(BaseModel):
    id: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
