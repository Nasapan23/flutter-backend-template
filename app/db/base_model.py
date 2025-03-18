from datetime import datetime
from typing import Any, Dict
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declared_attr
from app.db.session import Base


class BaseModel(Base):
    """
    Base model for all database models.
    Provides common fields and functionality.
    """
    __abstract__ = True

    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Use class name in lowercase as table name
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    
    def dict(self) -> Dict[str, Any]:
        """
        Convert model instance to dictionary.
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns} 