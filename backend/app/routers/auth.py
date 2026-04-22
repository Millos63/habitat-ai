from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.auth import AuthResponse, LoginRequest, RegisterRequest
from app.schemas.user import UserProfileUpdate, UserResponse
from app.services.auth_service import (
    authenticate_user,
    get_user_by_id,
    register_user,
    update_user_profile,
)
from app.utils.exceptions import UnauthorizedError
from app.utils.security import decode_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])
security = HTTPBearer(auto_error=False)


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> User:
    """Resolve current authenticated user from bearer token."""
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise UnauthorizedError()

    payload = decode_access_token(credentials.credentials)
    if not payload or "sub" not in payload:
        raise UnauthorizedError()

    try:
        user_id = UUID(str(payload["sub"]))
    except ValueError as exc:
        raise UnauthorizedError() from exc

    user = await get_user_by_id(db, user_id)
    if not user or not user.is_active:
        raise UnauthorizedError()

    return user


@router.post("/register", response_model=AuthResponse, status_code=201)
async def register_endpoint(
    data: RegisterRequest,
    db: AsyncSession = Depends(get_db),
) -> AuthResponse:
    """Register user and return access token."""
    return await register_user(db, data)


@router.post("/login", response_model=AuthResponse)
async def login_endpoint(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db),
) -> AuthResponse:
    """Authenticate user and return access token."""
    return await authenticate_user(db, data)


@router.get("/me", response_model=UserResponse)
async def me_endpoint(current_user: User = Depends(get_current_user)) -> UserResponse:
    """Get profile for the authenticated user."""
    return UserResponse.model_validate(current_user)


@router.put("/profile", response_model=UserResponse)
async def update_profile_endpoint(
    data: UserProfileUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """Update current authenticated user profile."""
    updated_user = await update_user_profile(db, current_user, data)
    return UserResponse.model_validate(updated_user)
