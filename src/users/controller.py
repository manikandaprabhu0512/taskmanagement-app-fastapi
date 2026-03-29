from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.users.dtos import UserSchema
from src.users.models import UserModel
from pwdlib import PasswordHash

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


def get_password_hash(password):
    return passhash.hash(password)