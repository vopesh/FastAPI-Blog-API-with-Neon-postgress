from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, Field
from typing import Optional

class BlogCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    content: str = Field(..., min_length=3, max_length=500)

class BlogOut(BaseModel):
    id: int
    title: str
    slug: str
    content: str
    author_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaginationParams(BaseModel):
    skip: int = Field(default=0, ge=0)
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100)
    
class PaginationResponse(BaseModel):
    total: int
    items: list
    page: int
    limit: int
    skip: int
    has_more: bool


class DeleteBlogResponse(BaseModel):
    message: str
    deleted_blog: BlogOut



