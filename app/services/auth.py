import hashlib
import hmac
import os
from dataclasses import dataclass
from typing import Optional

from sqlalchemy.orm import Session

from ..models import User


class AuthenticationError(Exception):
    """Raised when authentication fails."""


@dataclass
class AuthService:
    """Service handling user authentication and creation."""

    def _hash_password(self, password: str, salt: Optional[bytes] = None) -> str:
        """Hash a password with PBKDF2."""
        if salt is None:
            salt = os.urandom(16)
        hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
        return f"{salt.hex()}:{hashed.hex()}"

    def _verify_password(self, password: str, stored_hash: str) -> bool:
        """Verify a password against the stored hash."""
        try:
            salt_hex, hash_hex = stored_hash.split(":")
        except ValueError as exc:
            raise AuthenticationError("Invalid stored password format") from exc
        salt = bytes.fromhex(salt_hex)
        hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
        return hmac.compare_digest(hashed.hex(), hash_hex)

    def create_user(self, db: Session, email: str, password: str) -> User:
        """Create a new user with a hashed password."""
        if db.query(User).filter(User.email == email).first() is not None:
            raise ValueError("Email already registered")
        hashed_password = self._hash_password(password)
        user = User(email=email, hashed_password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def authenticate_user(self, db: Session, email: str, password: str) -> User:
        """Authenticate a user with the provided credentials."""
        user = db.query(User).filter(User.email == email).first()
        if user is None or not self._verify_password(password, user.hashed_password):
            raise AuthenticationError("Invalid credentials")
        return user
