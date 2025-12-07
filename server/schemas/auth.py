from pydantic import BaseModel


class SignupRequest(BaseModel):
    id: str
    username: str
    email: str
    avatar_url: str | None = None
    password: str


class LoginRequest(BaseModel):
    login: str              # <-- can be username OR email
    password: str           # required


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
