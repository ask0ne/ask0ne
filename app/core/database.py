import os
from tortoise import Tortoise
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = f"postgres://{os.getenv('DB_USER', 'postgres')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', 5432)}/{os.getenv('DB_NAME', 'blog_db')}"

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": os.getenv('DB_HOST', 'localhost'),
                "port": int(os.getenv('DB_PORT', 5432)),
                "user": os.getenv('DB_USER', 'postgres'),
                "password": os.getenv('DB_PASSWORD', 'password'),
                "database": os.getenv('DB_NAME', 'blog_db'),
                "statement_cache_size": 0,  # Disable prepared statements for pgbouncer compatibility
            }
        }
    },
    "apps": {
        "models": {
            "models": ["app.models.blog"],
            "default_connection": "default",
        },
    },
}

async def init_db():
    """Initialize Tortoise ORM"""
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()

async def close_db():
    """Close database connections"""
    await Tortoise.close_connections()