from sqlalchemy import Column, String, Boolean
from app.db.base_model import BaseModel
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    """
    User model for authentication and user management.
    """
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    def verify_password(self, plain_password: str) -> bool:
        """
        Verify the password against the stored hash.
        """
        return pwd_context.verify(plain_password, self.hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Generate password hash from plain password.
        """
        return pwd_context.hash(password) 