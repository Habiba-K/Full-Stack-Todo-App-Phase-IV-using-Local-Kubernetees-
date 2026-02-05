from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.auth.schemas import SignupRequest, SignupResponse, SigninRequest, SigninResponse, UserResponse
from src.auth.utils import hash_password, verify_password, create_jwt_token
from src.auth.dependencies import verify_jwt, get_current_user_id
from src.models.user import User
from src.database import get_session
from typing import Annotated
from uuid import UUID

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/signup", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    signup_data: SignupRequest,
    session: Annotated[AsyncSession, Depends(get_session)]
):
    """
    Register a new user account.

    - **email**: Valid email address (must be unique)
    - **password**: Minimum 8 characters
    - **name**: Optional display name

    Returns the created user information (without password).
    """
    # Check if email already exists
    result = await session.execute(
        select(User).where(User.email == signup_data.email)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Hash password
    password_hash = hash_password(signup_data.password)

    # Create new user
    new_user = User(
        email=signup_data.email,
        password_hash=password_hash,
        name=signup_data.name
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return SignupResponse(
        id=new_user.id,
        email=new_user.email,
        name=new_user.name,
        created_at=new_user.created_at
    )


@router.post("/signin", response_model=SigninResponse)
async def signin(
    signin_data: SigninRequest,
    session: Annotated[AsyncSession, Depends(get_session)]
):
    """
    Authenticate user and issue JWT token.

    - **email**: User's email address
    - **password**: User's password

    Returns user information and JWT access token.
    """
    # Find user by email
    result = await session.execute(
        select(User).where(User.email == signin_data.email)
    )
    user = result.scalar_one_or_none()

    # Verify credentials (don't reveal if email exists)
    if not user or not verify_password(signin_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate JWT token
    token, expires_at = create_jwt_token(user.id, user.email)

    return SigninResponse(
        user=UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at,
            updated_at=user.updated_at
        ),
        token=token,
        expires_at=expires_at
    )


@router.post("/logout")
async def logout(
    current_user_id: Annotated[UUID, Depends(get_current_user_id)]
):
    """
    Logout user (invalidate session).

    Requires valid JWT token in Authorization header.
    Note: JWT tokens are stateless, so logout is handled client-side by removing the token.
    """
    return {"message": "Logout successful"}


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    current_user_id: Annotated[UUID, Depends(get_current_user_id)],
    session: Annotated[AsyncSession, Depends(get_session)]
):
    """
    Get current authenticated user information.

    Requires valid JWT token in Authorization header.
    """
    result = await session.execute(
        select(User).where(User.id == current_user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        created_at=user.created_at,
        updated_at=user.updated_at
    )
