from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
import re

# Convert SQLAlchemy URL to async version if needed
def get_async_database_url():
    db_url = settings.DATABASE_URL
    
    # For SQLite, convert to aiosqlite
    if db_url.startswith("sqlite:"):
        return db_url.replace("sqlite:", "sqlite+aiosqlite:", 1)
    
    # For PostgreSQL, convert to asyncpg
    if db_url.startswith("postgresql:"):
        return db_url.replace("postgresql:", "postgresql+asyncpg:", 1)
    
    # For MySQL, convert to aiomysql
    if db_url.startswith(("mysql:", "mysql+pymysql:")):
        pattern = r"^mysql(\+pymysql)?:"
        return re.sub(pattern, "mysql+aiomysql:", db_url)
    
    return db_url

async_engine = create_async_engine(
    get_async_database_url(),
    echo=False,
    future=True,
)

AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


async def get_db():
    """
    Dependency for getting async database session.
    """
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()


async def init_db():
    """
    Initialize database connection.
    """
    async with async_engine.begin() as conn:
        # Apply any pending migrations or create tables
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all) 