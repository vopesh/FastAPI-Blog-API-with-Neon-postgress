# FastAPI Blog API 📝

A modern REST API for a blog application with user authentication, CRUD operations, and JWT token-based security. Built with FastAPI and Neon PostgreSQL.

## ✨ Features

- **User Authentication** - Secure JWT-based authentication with refresh tokens
- **User Management** - Register, login, and user profile management
- **Blog CRUD Operations** - Create, read, update, and delete blog posts
- **Role-Based Access Control** - User roles (user, admin)
- **Request Logging** - Comprehensive logging for all API requests
- **Error Handling** - Standardized error responses with custom exceptions
- **CORS Support** - Cross-Origin Resource Sharing enabled
- **Database Migrations** - Automatic table creation on startup
- **Health Check Endpoint** - Monitor API availability
- **Swagger Documentation** - Auto-generated API documentation

## 🛠️ Technology Stack

| Component            | Technology                   |
| -------------------- | ---------------------------- |
| **Framework**        | FastAPI 0.104+               |
| **Database**         | PostgreSQL (Neon Serverless) |
| **ORM**              | SQLAlchemy 2.0+              |
| **Authentication**   | JWT (python-jose)            |
| **Password Hashing** | Argon2 (passlib)             |
| **Server**           | Uvicorn                      |
| **Language**         | Python 3.10+                 |

## 📋 Project Structure

```
Project-FastAPI-Blog/
├── app/
│   ├── api/
│   │   ├── deps.py              # Dependency injection (DB, Auth)
│   │   ├── users_routes.py      # User endpoints
│   │   └── blogs_routes.py      # Blog endpoints
│   ├── core/
│   │   ├── config.py            # Configuration & environment variables
│   │   ├── exceptions.py        # Custom exception classes
│   │   ├── logger.py            # JSON logging setup
│   │   ├── secure.py            # Authentication & password hashing
│   │   └── validators.py        # Input validation
│   ├── database/
│   │   ├── base.py              # SQLAlchemy base model
│   │   └── session.py           # Database engine & session
│   ├── models/
│   │   └── users_and_blog.py   # User & Blog database models
│   └── schemas/
│       ├── users.py             # User Pydantic schemas
│       └── blog.py              # Blog Pydantic schemas
├── main.py                      # FastAPI application entry point
├── .env                         # Environment variables (not in git)
├── .env.example                 # Example environment file
├── .gitignore                   # Git ignore rules
└── requirements.txt             # Python dependencies
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- PostgreSQL database (or Neon serverless account)
- pip package manager

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/Project-FastAPI-Blog.git
cd Project-FastAPI-Blog
```

2. **Create virtual environment:**

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows PowerShell
# or
source .venv/bin/activate   # Linux/Mac
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Setup environment variables:**

```bash
cp .env.example .env
# Edit .env with your Neon PostgreSQL connection string and secrets
```

5. **Run the application:**

```bash
uvicorn main:app --reload
```

The API will be available at: **http://127.0.0.1:8000**

## 🔧 Environment Configuration

Create a `.env` file in the project root:

```env
# Neon PostgreSQL Connection
DATABASE_URL=postgresql://dbname:your_password@ep-xxxx.region.aws.neon.tech/neondb?sslmode=require

# JWT Security
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256

# Token Expiration (in minutes)
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_MINUTES=10080
```

**Get your Neon connection string:**

1. Visit [Neon Console](https://console.neon.tech)
2. Select your project
3. Click "Connection String"
4. Select "psycopg2" driver
5. Copy the full connection string

## 📚 API Documentation

### Swagger UI (Interactive)

- **URL:** http://127.0.0.1:8000/docs
- Click "Try it out" to test endpoints directly

### ReDoc (Alternative UI)

- **URL:** http://127.0.0.1:8000/redoc

### Health Check

```bash
curl http://127.0.0.1:8000/health
```

## 👤 User Endpoints

### Register User

```http
POST /api/users/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password",
  "role": "user"
}
```

### Login

```http
POST /api/users/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=secure_password
```

Response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Get Current User

```http
GET /api/users/me
Authorization: Bearer {access_token}
```

## 📝 Blog Endpoints

### Create Blog Post

```http
POST /api/blogs/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "My First Blog Post",
  "slug": "my-first-blog-post",
  "content": "This is the content of my blog post..."
}
```

### Get All Blog Posts

```http
GET /api/blogs/
```

### Get Single Blog Post

```http
GET /api/blogs/{blog_id}
```

### Update Blog Post

```http
PUT /api/blogs/{blog_id}
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "Updated Title",
  "content": "Updated content..."
}
```

### Delete Blog Post

```http
DELETE /api/blogs/{blog_id}
Authorization: Bearer {access_token}
```

## 🔐 Authentication

The API uses **JWT (JSON Web Tokens)** for authentication:

1. User registers and logs in
2. Server returns `access_token` and `token_type`
3. Client includes token in Authorization header: `Bearer {token}`
4. Server validates token and returns protected resources

**Token includes:**

- User ID
- Expiration time (30 minutes default)
- Signature verification

## 🗄️ Database Schema

### Users Table

```sql
CREATE TABLE blog_users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  role VARCHAR(255) DEFAULT 'user',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Blogs Table

```sql
CREATE TABLE users_blogs (
  id SERIAL PRIMARY KEY,
  title VARCHAR NOT NULL,
  slug VARCHAR UNIQUE NOT NULL,
  content TEXT NOT NULL,
  author_id INTEGER FOREIGN KEY REFERENCES blog_users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

## 📊 Logging

All requests and errors are logged in JSON format:

```json
{
  "timestamp": "2026-06-07T10:30:45.123456",
  "level": "INFO",
  "message": "Incoming request: POST /api/users/register",
  "module": "main",
  "funcName": "log_requests",
  "lineno": 65
}
```

Logs are stored in:

- **Console:** Real-time output
- **File:** `logs/{YYYY-MM-DD}.log` (rotated daily)


- **Heroku**: Add `Procfile` with gunicorn command
- **Railway**: Connect GitHub repo directly
- **Render**: Use Docker or Python buildpack
- **AWS/Azure**: Use EC2/App Service with gunicorn

## 🔒 Security Best Practices

✅ **Implemented:**

- Password hashing with Argon2
- JWT token-based authentication
- Refresh token support
- CORS configuration
- Error handling without exposing internals
- Environment variable protection

⚠️ **Before Production:**

- [ ] Use strong `SECRET_KEY` (generate with `openssl rand -hex 32`)
- [ ] Enable HTTPS/SSL
- [ ] Restrict CORS origins (replace `*` with specific domains)
- [ ] Set secure database user with minimal permissions
- [ ] Enable database encryption
- [ ] Implement rate limiting
- [ ] Add request validation & sanitization
- [ ] Set up monitoring & alerting

## 📦 Dependencies

```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
passlib[argon2]==1.7.4
python-jose[cryptography]==3.3.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
```

Install all: `pip install -r requirements.txt`

## 🐛 Troubleshooting

### Database Connection Error

- **Issue:** `password authentication failed`
- **Solution:** Verify `DATABASE_URL` in `.env` with correct credentials from Neon Console

### Module Not Found Errors

- **Issue:** `ModuleNotFoundError: No module named 'app'`
- **Solution:** Run from project root and ensure virtual environment is activated

### Port Already in Use

- **Issue:** `OSError: Address already in use`
- **Solution:** Change port: `uvicorn main:app --port 8001`

### .env Not Loading

- **Issue:** Environment variables not recognized
- **Solution:** Restart the application after updating `.env`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -m "Add new feature"`
4. Push to branch: `git push origin feature/new-feature`
5. Submit a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💼 Author

**Your Name** - [GitHub](https://github.com/vopesh) | [LinkedIn](https://www.linkedin.com/in/vopeshchandra/)



For issues, questions, or suggestions:

- Open an [Issue](https://github.com/yourusername/Project-FastAPI-Blog/issues)
- Contact: letsrock10_vicky@live.com

---

**Happy Coding and practice! 🚀**

_Made with ❤️ using FastAPI and PostgreSQL_
