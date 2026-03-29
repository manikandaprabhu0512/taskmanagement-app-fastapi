from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    email: str
    password: str
    is_active: bool = True


class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool


class UserLoginSchema(BaseModel):
    email: str
    password: str


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str
