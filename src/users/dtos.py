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
