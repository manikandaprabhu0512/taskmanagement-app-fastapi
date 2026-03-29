from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from src.users import controller
from src.users.dtos import (TokenResponseSchema, UserLoginSchema,
                            UserResponseSchema, UserSchema)
from src.utils.db import get_db

user_routes = APIRouter(prefix="/users")


@user_routes.post(
    "/register",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def register_user(body: UserSchema, db: Session = Depends(get_db)):
    return controller.register_user(body, db)


@user_routes.post(
    "/login",
    response_model=TokenResponseSchema,
    status_code=status.HTTP_200_OK,
)
def login_user(body: UserLoginSchema, db: Session = Depends(get_db)):
    return controller.login_user(body, db)

@user_routes.get("/is-authenticated", response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
def is_authenticated(request: Request, db: Session = Depends(get_db)):
    return controller.isAuthenticated(request, db)