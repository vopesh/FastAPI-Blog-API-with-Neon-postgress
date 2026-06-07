from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# For Neon PostgreSQL with psycopg2
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,  # Verify connections before using them
    pool_size=5,
    max_overflow=10,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)