from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas.users import UserCreate, Userout, TokenResponse
from app.models.users_and_blog import User
from app.api.deps import get_db, get_current_user
from app.core.secure import create_access_token, verify_password, hash_password
from app.core.logger import logger
from app.core.exceptions import ConflictException, ValidationException, AuthenticationException
from app.core.validators import EmailValidators, PasswordValidators

router = APIRouter(tags=["Authentication"])

@router.post("/register", response_model=Userout, status_code=status.HTTP_201_CREATED)
def register_user(user_create: UserCreate, db: Session=Depends(get_db)) -> Userout:
    # Validate email and password
    if not EmailValidators.validate_email(user_create.email):
        logger.warning(f"Invalid email format: {user_create.email}")
        raise ValidationException("Invalid email format")
    
    if not PasswordValidators.validate_password(user_create.Password):
        logger.warning(f"Weak password provided for email: {user_create.email}")
        raise ValidationException("Password must be at least 8 characters long and include uppercase, lowercase, number, and special character")
    
    # Hash the password
    hashed_password = hash_password(user_create.Password)
    
    new_user = User(email=user_create.email, password=hashed_password)
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info(f"User registered successfully: {new_user} (ID: {new_user.id}, Email: {new_user.email})")
        return Userout.from_orm(new_user)
    except IntegrityError:
        db.rollback()
        logger.error(f"Email already exists: {user_create.email}")
        raise ConflictException("Email already exists")
    

@router.post("/login", response_model=TokenResponse)
def login_user(user_create: UserCreate, db: Session=Depends(get_db)) -> TokenResponse:
    user = db.query(User).filter(User.email == user_create.email).first()
    if not user:
        logger.warning(f"Login failed - user not found: {user_create.email}")
        raise AuthenticationException("Invalid email or password")
    
    if not verify_password(user_create.Password, user.password):
        logger.warning(f"Login failed - incorrect password for email: {user_create.email}")
        raise AuthenticationException("Invalid email or password")
    
    access_token = create_access_token(data={"id": user.id, "email": user.email, "role": user.role})
    logger.info(f"User logged in successfully: {user} (ID: {user.id}, Email: {user.email})")
    return TokenResponse(access_token=access_token, token_type="bearer", user_id=user.id, email=user.email, role=user.role)

@router.get("/me", response_model=Userout)
def get_current_user_info(current_user: User = Depends(get_current_user)) -> Userout:
    logger.info(f"Retrieved current user info: {current_user} (ID: {current_user.id}, Email: {current_user.email})")
    return Userout.from_orm(current_user)
