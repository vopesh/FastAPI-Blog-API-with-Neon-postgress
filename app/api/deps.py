from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError
from app.core.secure import oauth2_scheme, decode_access_token
from app.database.session import SessionLocal
from app.models.users_and_blog import User
from app.core.exceptions import AuthenticationException
from app.core.logger import logger

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = decode_access_token(token)
        user_id = payload.get("id")
        if user_id is None:
            raise AuthenticationException("Invalid token")
    except JWTError as e:
        logger.error(f"JWTError: {e}")
        raise AuthenticationException("Invalid token")
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise AuthenticationException("Invalid token")
    logger.info(f"Authenticated user: {user} (ID: {user.id}, Email: {user.email})")
    return user

