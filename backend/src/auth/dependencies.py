from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated
import jwt
from src.auth.utils import decode_jwt_token
from uuid import UUID

security = HTTPBearer()


async def verify_jwt(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> dict:
    """
    Verify JWT token and return payload.

    Args:
        credentials: HTTP Bearer credentials from Authorization header

    Returns:
        Decoded JWT payload containing user information

    Raises:
        HTTPException: 401 if token is invalid or expired
    """
    try:
        payload = decode_jwt_token(credentials.credentials)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


async def get_current_user_id(
    payload: Annotated[dict, Depends(verify_jwt)]
) -> UUID:
    """
    Extract user ID from JWT payload.

    Args:
        payload: Decoded JWT payload

    Returns:
        User UUID from token
    """
    return UUID(payload["sub"])
