from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, Request
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from src.users.dtos import UserLoginSchema, UserSchema
from src.users.models import UserModel
from src.utils.settings import settings

passhash = PasswordHash.recommended()

def register_user(body: UserSchema, db: Session):
    data = body.model_dump()

    is_user = db.query(UserModel).filter(UserModel.username == data["username"]).first()
    if is_user:
        raise HTTPException(status_code=409, detail="Username already registered")

    is_user = db.query(UserModel).filter(UserModel.email == data["email"]).first()
    if is_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    
    data["password"] = get_password_hash(data["password"])

    new_user = UserModel(
        username=data["username"],
        email=data["email"],
        hash_password=data["password"],
        is_active=data["is_active"],
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def login_user(body: UserLoginSchema, db: Session):
    data = body.model_dump()

    is_user = db.query(UserModel).filter(UserModel.email == data["email"]).first()
    if not is_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(data["password"], is_user.hash_password):
        raise HTTPException(status_code=401, detail="Invalid password")
    
    exp_time = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    token = jwt.encode({"_id" : is_user.id, "email": is_user.email, "exp" : exp_time.timestamp()}, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)

    return {"access_token": token, "token_type": "jwt"}


def isAuthenticated(request: Request, db: Session):
    try:
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(status_code=401, detail="Token not found")
        
        token = token.split(" ")[1]

        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])

        current_time = datetime.now().timestamp()
        exp_time = int(payload.get("exp"))

        if current_time > exp_time:
            raise HTTPException(status_code=401, detail="Token expired")

        is_user = db.query(UserModel).filter(UserModel.id == payload["_id"]).first()
        if not is_user:
            raise HTTPException(status_code=404, detail="User not found")

        return is_user
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token expired")


def get_password_hash(password):
    return passhash.hash(password)


def verify_password(plain_password, hashed_password):
    return passhash.verify(plain_password, hashed_password)