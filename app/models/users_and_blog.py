from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.base import Base

class User(Base):
    __tablename__ = "blog_users"
    id = Column(Integer, primary_key=True, index=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    email = Column(String(255), unique=True, index=True,nullable=False)
    role = Column(String(255), nullable=False, default="user")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    blogs = relationship("Blog", back_populates="author", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<User(id='{self.id}', email='{self.email}', role='{self.role}')>"


class Blog(Base):
    __tablename__ = "Users_Blogs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("blog_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    author = relationship("User", back_populates="blogs")
    
    def __repr__(self) -> str:
        return f"<Blog(title='{self.title}', slug='{self.slug}')>"
