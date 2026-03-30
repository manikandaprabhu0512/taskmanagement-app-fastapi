from datetime import datetime

import jwt
from fastapi import Depends, HTTPException, Request
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from src.users.models import UserModel
from src.utils.db import get_db
from src.utils.settings import settings


def isAuthenticated(request: Request, db: Session = Depends(get_db)):
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