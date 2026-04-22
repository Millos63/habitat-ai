from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.auth import AuthResponse, LoginRequest, RegisterRequest
from app.schemas.user import UserProfileUpdate
from app.utils.exceptions import ConflictError, UnauthorizedError
from app.utils.security import create_access_token, hash_password, verify_password


async def register_user(db: AsyncSession, data: RegisterRequest) -> AuthResponse:
    """Create a new user account and return a JWT token."""
    existing_user = await db.scalar(select(User).where(User.email == data.email.lower()))
    if existing_user:
        raise ConflictError("Email is already registered")

    user = User(
        email=data.email.lower(),
        password_hash=hash_password(data.password),
        full_name=data.full_name,
        phone=data.phone,
        role=data.role,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    access_token = create_access_token({"sub": str(user.id)})
    return AuthResponse(access_token=access_token, user_id=str(user.id))


async def authenticate_user(db: AsyncSession, data: LoginRequest) -> AuthResponse:
    """Validate credentials and return JWT token."""
    user = await db.scalar(select(User).where(User.email == data.email.lower()))
    if not user or not verify_password(data.password, user.password_hash):
        raise UnauthorizedError("Invalid email or password")

    if not user.is_active:
        raise UnauthorizedError("This account is inactive")

    access_token = create_access_token({"sub": str(user.id)})
    return AuthResponse(access_token=access_token, user_id=str(user.id))


async def get_user_by_id(db: AsyncSession, user_id: UUID) -> User | None:
    """Fetch a user by id."""
    return await db.get(User, user_id)


async def update_user_profile(db: AsyncSession, user: User, data: UserProfileUpdate) -> User:
    """Update current user profile data."""
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)
    return user
