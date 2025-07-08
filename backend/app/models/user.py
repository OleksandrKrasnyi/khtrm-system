"""User models for KHTRM System."""

from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class UserRoleEnum(str, Enum):
    """User role enumeration for KHTRM system."""

    # Super admin - has access to everything
    SUPER_ADMIN = "super_admin"

    # Transport management roles
    DISPATCHER = "dispatcher"  # нарядчик - creates transport assignments
    TIMEKEEPER = "timekeeper"  # табельщик - records incidents and work hours
    PARKING_MANAGER = "parking_manager"  # принимает транспорт на стоянку
    FUEL_MANAGER = "fuel_manager"  # управляет топливом

    # Additional roles for future expansion
    MECHANIC = "mechanic"  # механик - for maintenance
    DRIVER = "driver"  # водитель - for driver interface
    INSPECTOR = "inspector"  # инспектор - for quality control
    ANALYST = "analyst"  # аналитик - for reports and analytics


class UserRole(Base, TimestampMixin):
    """User role model with permissions."""

    __tablename__ = "user_roles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[UserRoleEnum] = mapped_column(
        String(50), unique=True, nullable=False, comment="Role name"
    )
    display_name_uk: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="Display name in Ukrainian"
    )
    display_name_en: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="Display name in English"
    )
    description: Mapped[str | None] = mapped_column(Text, comment="Role description")
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False, comment="Whether role is active"
    )

    # Permission flags for quick access checks
    can_manage_users: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="Can manage users and roles"
    )
    can_manage_vehicles: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="Can manage vehicle fleet"
    )
    can_create_assignments: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="Can create transport assignments"
    )
    can_record_incidents: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="Can record incidents and work hours"
    )
    can_manage_parking: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="Can manage parking and vehicle return"
    )
    can_manage_fuel: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="Can manage fuel operations"
    )
    can_view_reports: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="Can view reports and analytics"
    )
    can_manage_system: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="Can manage system settings"
    )

    # Relationship to users
    users: Mapped[list["User"]] = relationship(
        "User", back_populates="role", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<UserRole(name={self.name}, display_name_uk={self.display_name_uk})>"


class User(Base, TimestampMixin):
    """User model for KHTRM system."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Basic user information
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True, comment="Unique username"
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        comment="User email address",
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="Hashed password"
    )

    # Personal information
    first_name: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="First name"
    )
    last_name: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="Last name"
    )
    middle_name: Mapped[str | None] = mapped_column(
        String(100), comment="Middle name (patronymic)"
    )
    phone: Mapped[str | None] = mapped_column(String(20), comment="Phone number")

    # Role and permissions
    role_id: Mapped[int] = mapped_column(
        ForeignKey("user_roles.id"), nullable=False, comment="User role ID"
    )

    # Account status
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False, comment="Whether user account is active"
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, comment="Whether user email is verified"
    )

    # Login tracking
    last_login: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), comment="Last login timestamp"
    )
    login_count: Mapped[int] = mapped_column(
        default=0, nullable=False, comment="Total login count"
    )

    # Additional metadata
    employee_id: Mapped[str | None] = mapped_column(
        String(50), unique=True, comment="Employee ID number"
    )
    department: Mapped[str | None] = mapped_column(
        String(100), comment="Department name"
    )
    notes: Mapped[str | None] = mapped_column(
        Text, comment="Additional notes about user"
    )

    # Relationships
    role: Mapped["UserRole"] = relationship("UserRole", back_populates="users")

    @property
    def full_name(self) -> str:
        """Get full name of user."""
        parts = [self.last_name, self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        return " ".join(parts)

    @property
    def is_super_admin(self) -> bool:
        """Check if user is super admin."""
        return self.role.name == UserRoleEnum.SUPER_ADMIN

    @property
    def is_dispatcher(self) -> bool:
        """Check if user is dispatcher."""
        return self.role.name == UserRoleEnum.DISPATCHER

    @property
    def is_timekeeper(self) -> bool:
        """Check if user is timekeeper."""
        return self.role.name == UserRoleEnum.TIMEKEEPER

    @property
    def is_parking_manager(self) -> bool:
        """Check if user is parking manager."""
        return self.role.name == UserRoleEnum.PARKING_MANAGER

    @property
    def is_fuel_manager(self) -> bool:
        """Check if user is fuel manager."""
        return self.role.name == UserRoleEnum.FUEL_MANAGER

    def has_permission(self, permission: str) -> bool:
        """Check if user has specific permission."""
        if self.is_super_admin:
            return True

        return getattr(self.role, permission, False)

    def __repr__(self) -> str:
        return f"<User(username={self.username}, role={self.role.name})>"
