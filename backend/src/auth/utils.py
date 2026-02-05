import bcrypt
import jwt
from datetime import datetime, timedelta
from uuid import UUID
import os
from dotenv import load_dotenv

load_dotenv()

BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt with cost factor 12.

    Args:
        password: Plain text password

    Returns:
        Hashed password string
    """
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash using bcrypt.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password to compare against

    Returns:
        True if password matches, False otherwise
    """
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )


def create_jwt_token(user_id: UUID, email: str, expires_delta: timedelta = timedelta(days=7)) -> tuple[str, datetime]:
    """
    Create a JWT token with user claims.

    Args:
        user_id: User's UUID
        email: User's email address
        expires_delta: Token expiration duration (default 7 days)

    Returns:
        Tuple of (token string, expiration datetime)
    """
    now = datetime.utcnow()
    expires_at = now + expires_delta

    payload = {
        "sub": str(user_id),
        "email": email,
        "iat": int(now.timestamp()),
        "exp": int(expires_at.timestamp())
    }

    token = jwt.encode(payload, BETTER_AUTH_SECRET, algorithm="HS256")
    return token, expires_at


def decode_jwt_token(token: str) -> dict:
    """
    Decode and verify a JWT token.

    Args:
        token: JWT token string

    Returns:
        Decoded token payload

    Raises:
        jwt.ExpiredSignatureError: If token has expired
        jwt.InvalidTokenError: If token is invalid
    """
    return jwt.decode(token, BETTER_AUTH_SECRET, algorithms=["HS256"])


def validate_ownership(path_user_id: UUID, jwt_user_id: UUID) -> bool:
    """
    Validate that the authenticated user matches the path parameter user_id.

    Args:
        path_user_id: User ID from path parameter
        jwt_user_id: User ID from JWT token

    Returns:
        True if IDs match, False otherwise
    """
    return path_user_id == jwt_user_id
