from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
import re
from app.schemas.blog import BlogCreate, BlogOut, PaginationParams, PaginationResponse, DeleteBlogResponse
from app.models.users_and_blog import Blog
from app.api.deps import get_db, get_current_user
from app.core.logger import logger
from app.core.exceptions import ConflictException, ValidationException, AuthenticationException

router = APIRouter(tags=["Blogs"])

@router.post("/blogs", response_model=BlogOut, status_code=status.HTTP_201_CREATED)
def create_blog(blog_create: BlogCreate, db: Session=Depends(get_db), current_user=Depends(get_current_user)) -> BlogOut:
    # Validate title and content
    if not blog_create.title or not blog_create.content:
        logger.warning(f"Validation failed - title and content are required for user ID: {current_user.id}")
        raise ValidationException("Title and content are required")
    
    # Generate slug from title
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', blog_create.title.lower()).strip('-')
    
    new_blog = Blog(title=blog_create.title, content=blog_create.content, slug=slug, author_id=current_user.id)
    
    try:
        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)
        logger.info(f"Blog created successfully: {new_blog} (ID: {new_blog.id}, Title: {new_blog.title}) by User ID: {current_user.id}")
        return BlogOut.from_orm(new_blog)
    except IntegrityError:
        db.rollback()
        logger.error(f"Blog creation failed - slug already exists: {slug} for user ID: {current_user.id}")
        raise ConflictException("A blog with the same title already exists")

@router.get("/blogs", response_model=PaginationResponse)
def list_blogs(pagination: PaginationParams = Depends(), db: Session=Depends(get_db)) -> PaginationResponse:
    total_blogs = db.query(Blog).count()
    blogs = db.query(Blog).offset(pagination.skip).limit(pagination.limit).all()
    has_more = pagination.skip + pagination.limit < total_blogs
    logger.info(f"Listed blogs - Total: {total_blogs}, Page: {pagination.page}, Limit: {pagination.limit}")
    return PaginationResponse(
        total=total_blogs,
        items=[BlogOut.from_orm(blog) for blog in blogs],
        page=pagination.page,
        limit=pagination.limit,
        skip=pagination.skip,
        has_more=has_more
    )



