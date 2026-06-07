from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api.users_routes import router as users_router
from app.api.blogs_routes import router as blogs_router
from app.core.logger import logger
from fastapi.responses import JSONResponse
from app.core.exceptions import AppException
from contextlib import asynccontextmanager
from datetime import datetime
import time
from app.database.base import Base
from app.database.session import engine
from sqlalchemy import text

# Initialize database tables on startup
def init_db():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up FastAPI application")
    init_db()
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            logger.info("✓ Connected to Neon PostgreSQL database successfully")
    except Exception as e:
        logger.error(f"✗ Failed to connect to database: {e}")
    yield
    # Shutdown
    logger.info("Shutting down FastAPI application")
    engine.dispose()

app = FastAPI(
    title="Blog API", 
    description="A simple blog API with user authentication and CRUD operations for blogs.", 
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"])

app.include_router(users_router, prefix="/api/users", tags=["Users"])
app.include_router(blogs_router, prefix="/api/blogs", tags=["Blogs"])

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    logger.error(f"APIException: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Completed request: {request.method} {request.url} - Status: {response.status_code} - Time: {process_time:.2f}s")
    return response

@app.get("/health", tags=["Health"]) 
async def health_check():
    """Health check endpoint to verify API is running"""
    return {"status": "All ok", "timestamp": datetime.now().isoformat()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
