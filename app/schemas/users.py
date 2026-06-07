from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    Password: str
    
class Userout(BaseModel):
    id: int
    email: EmailStr
    role: str
    created_at: datetime
    updated_at: datetime
    

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer")
    user_id: int
    email: str
    role: str
    
 