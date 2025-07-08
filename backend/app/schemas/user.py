"""User schemas for KHTRM System."""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, validator

from ..models.user import UserRoleEnum


class UserRoleBase(BaseModel):
    """Base schema for user roles."""

    name: UserRoleEnum = Field(..., description="Role name")
    display_name_uk: str = Field(
        ..., min_length=2, max_length=100, description="Display name in Ukrainian"
    )
    display_name_en: str = Field(
        ..., min_length=2, max_length=100, description="Display name in English"
    )
    description: str | None = Field(None, description="Role description")
    is_active: bool = Field(True, description="Whether role is active")

    # Permission flags
    can_manage_users: bool = Field(False, description="Can manage users and roles")
    can_manage_vehicles: bool = Field(False, description="Can manage vehicle fleet")
    can_create_assignments: bool = Field(
        False, description="Can create transport assignments"
    )
    can_record_incidents: bool = Field(
        False, description="Can record incidents and work hours"
    )
    can_manage_parking: bool = Field(
        False, description="Can manage parking and vehicle return"
    )
    can_manage_fuel: bool = Field(False, description="Can manage fuel operations")
    can_view_reports: bool = Field(False, description="Can view reports and analytics")
    can_manage_system: bool = Field(False, description="Can manage system settings")


class UserRoleCreate(UserRoleBase):
    """Schema for creating user roles."""

    pass


class UserRoleUpdate(BaseModel):
    """Schema for updating user roles."""

    display_name_uk: str | None = Field(None, min_length=2, max_length=100)
    display_name_en: str | None = Field(None, min_length=2, max_length=100)
    description: str | None = None
    is_active: bool | None = None

    can_manage_users: bool | None = None
    can_manage_vehicles: bool | None = None
    can_create_assignments: bool | None = None
    can_record_incidents: bool | None = None
    can_manage_parking: bool | None = None
    can_manage_fuel: bool | None = None
    can_view_reports: bool | None = None
    can_manage_system: bool | None = None


class UserRoleResponse(UserRoleBase):
    """Schema for user role responses."""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    """Base schema for users."""

    username: str = Field(
        ..., min_length=3, max_length=50, description="Unique username"
    )
    email: EmailStr = Field(..., description="User email address")
    first_name: str = Field(..., min_length=2, max_length=100, description="First name")
    last_name: str = Field(..., min_length=2, max_length=100, description="Last name")
    middle_name: str | None = Field(
        None, min_length=2, max_length=100, description="Middle name (patronymic)"
    )
    phone: str | None = Field(
        None, regex=r"^\+?[\d\s\-\(\)]{7,20}$", description="Phone number"
    )
    employee_id: str | None = Field(
        None, min_length=1, max_length=50, description="Employee ID number"
    )
    department: str | None = Field(
        None, min_length=2, max_length=100, description="Department name"
    )
    notes: str | None = Field(None, description="Additional notes about user")

    @validator("username")
    def validate_username(cls, v):
        """Validate username format."""
        if not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError(
                "Ім'я користувача може містити тільки літери, цифри, дефіс та підкреслення"
            )
        return v.lower()

    @validator("phone")
    def validate_phone(cls, v):
        """Validate phone number format."""
        if v is not None:
            # Remove all non-digit characters except +
            cleaned = "".join(c for c in v if c.isdigit() or c == "+")
            if len(cleaned) < 7:
                raise ValueError("Номер телефону занадто короткий")
            if len(cleaned) > 20:
                raise ValueError("Номер телефону занадто довгий")
        return v

    @validator("first_name", "last_name", "middle_name")
    def validate_names(cls, v):
        """Validate name fields."""
        if v is not None:
            if not v.replace(" ", "").replace("-", "").replace("'", "").isalpha():
                raise ValueError(
                    "Ім'я може містити тільки літери, пробіли, дефіс та апостроф"
                )
        return v


class UserCreate(UserBase):
    """Schema for creating users."""

    password: str = Field(
        ..., min_length=8, max_length=100, description="User password"
    )
    role_id: int = Field(..., gt=0, description="User role ID")
    is_active: bool = Field(True, description="Whether user account is active")
    is_verified: bool = Field(False, description="Whether user email is verified")

    @validator("password")
    def validate_password(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError("Пароль має містити принаймні 8 символів")

        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_digit = any(c.isdigit() for c in v)

        if not (has_upper and has_lower and has_digit):
            raise ValueError(
                "Пароль має містити принаймні одну велику літеру, одну малу літеру та одну цифру"
            )

        return v


class UserUpdate(BaseModel):
    """Schema for updating users."""

    email: EmailStr | None = None
    first_name: str | None = Field(None, min_length=2, max_length=100)
    last_name: str | None = Field(None, min_length=2, max_length=100)
    middle_name: str | None = Field(None, min_length=2, max_length=100)
    phone: str | None = Field(None, regex=r"^\+?[\d\s\-\(\)]{7,20}$")
    employee_id: str | None = Field(None, min_length=1, max_length=50)
    department: str | None = Field(None, min_length=2, max_length=100)
    notes: str | None = None
    role_id: int | None = Field(None, gt=0)
    is_active: bool | None = None
    is_verified: bool | None = None

    @validator("phone")
    def validate_phone(cls, v):
        """Validate phone number format."""
        if v is not None:
            cleaned = "".join(c for c in v if c.isdigit() or c == "+")
            if len(cleaned) < 7:
                raise ValueError("Номер телефону занадто короткий")
            if len(cleaned) > 20:
                raise ValueError("Номер телефону занадто довгий")
        return v

    @validator("first_name", "last_name", "middle_name")
    def validate_names(cls, v):
        """Validate name fields."""
        if v is not None:
            if not v.replace(" ", "").replace("-", "").replace("'", "").isalpha():
                raise ValueError(
                    "Ім'я може містити тільки літери, пробіли, дефіс та апостроф"
                )
        return v


class UserResponse(UserBase):
    """Schema for user responses."""

    id: int
    role_id: int
    is_active: bool
    is_verified: bool
    last_login: datetime | None
    login_count: int
    created_at: datetime
    updated_at: datetime

    # Related data
    role: UserRoleResponse

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    """Schema for login requests."""

    username: str = Field(
        ..., min_length=3, max_length=50, description="Username or email"
    )
    password: str = Field(..., min_length=1, max_length=100, description="Password")

    @validator("username")
    def validate_username(cls, v):
        """Validate username format."""
        return v.lower().strip()


class TokenResponse(BaseModel):
    """Schema for token responses."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class LoginResponse(BaseModel):
    """Schema for login responses."""

    user: UserResponse
    token: TokenResponse
    message: str = "Успішно увійшли в систему"


class PasswordChangeRequest(BaseModel):
    """Schema for password change requests."""

    current_password: str = Field(
        ..., min_length=1, max_length=100, description="Current password"
    )
    new_password: str = Field(
        ..., min_length=8, max_length=100, description="New password"
    )
    confirm_password: str = Field(
        ..., min_length=8, max_length=100, description="Confirm new password"
    )

    @validator("confirm_password")
    def validate_password_match(cls, v, values):
        """Validate that passwords match."""
        if "new_password" in values and v != values["new_password"]:
            raise ValueError("Паролі не співпадають")
        return v

    @validator("new_password")
    def validate_new_password(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError("Пароль має містити принаймні 8 символів")

        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_digit = any(c.isdigit() for c in v)

        if not (has_upper and has_lower and has_digit):
            raise ValueError(
                "Пароль має містити принаймні одну велику літеру, одну малу літеру та одну цифру"
            )

        return v
