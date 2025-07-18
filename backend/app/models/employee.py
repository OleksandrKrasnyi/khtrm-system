"""
Employee model for dispatcher functionality
Based on sprpersonal table structure from database analysis
"""

from typing import Any

from sqlalchemy import Boolean, Column, Date, Integer, String, Text

from .base import Base


class Employee(Base):
    """
    Model for employees (сотрудники) - reference table for dispatcher functionality
    Based on sprpersonal table with 966 records
    """

    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)

    # Employee identification
    tab_number = Column(
        Integer, nullable=False, unique=True, index=True, comment="Табельный номер"
    )
    full_name = Column(String(255), nullable=False, comment="ФИО сотрудника")

    # Personal information
    first_name = Column(String(100), nullable=True, comment="Имя")
    last_name = Column(String(100), nullable=True, comment="Фамилия")
    middle_name = Column(String(100), nullable=True, comment="Отчество")

    # Position information
    position = Column(String(100), nullable=True, comment="Должность")
    category = Column(
        String(50), nullable=True, comment="Категория (водитель, кондуктор, etc.)"
    )
    qualification = Column(String(50), nullable=True, comment="Квалификация")

    # Work information
    hire_date = Column(Date, nullable=True, comment="Дата приема на работу")
    department = Column(String(100), nullable=True, comment="Отдел/депо")
    shift = Column(String(10), nullable=True, comment="Смена")

    # License information (for drivers)
    license_number = Column(
        String(50), nullable=True, comment="Номер водительского удостоверения"
    )
    license_category = Column(String(20), nullable=True, comment="Категория ВУ")
    license_expiry = Column(Date, nullable=True, comment="Дата окончания ВУ")

    # Contact information
    phone = Column(String(50), nullable=True, comment="Телефон")
    email = Column(String(100), nullable=True, comment="Email")
    address = Column(String(255), nullable=True, comment="Адрес")

    # Status
    is_active = Column(Boolean, default=True, comment="Активный сотрудник")
    is_deleted = Column(Boolean, default=False, comment="Флаг удаления")

    # Additional information
    notes = Column(Text, nullable=True, comment="Примечания")

    # Relationships
    # driver_assignments = relationship("Assignment", foreign_keys="Assignment.driver_tab_number", back_populates="driver")
    # conductor_assignments = relationship("Assignment", foreign_keys="Assignment.conductor_tab_number", back_populates="conductor")

    def __repr__(self) -> str:
        return f"<Employee(id={self.id}, tab_number={self.tab_number}, name={self.full_name})>"

    @property
    def display_name(self) -> str:
        """Human readable employee name"""
        if self.tab_number:
            return f"№{self.tab_number} - {self.full_name}"
        return self.full_name or ""  # type: ignore[return-value]

    @property
    def short_name(self) -> str:
        """Short employee name for display"""
        if self.last_name and self.first_name:
            if self.middle_name:
                return f"{self.last_name} {self.first_name[0]}.{self.middle_name[0]}."
            return f"{self.last_name} {self.first_name[0]}."
        return self.full_name or ""  # type: ignore[return-value]

    @property
    def is_driver(self) -> bool:
        """Check if employee is a driver"""
        return bool(self.category and "водитель" in self.category.lower())

    @property
    def is_conductor(self) -> bool:
        """Check if employee is a conductor"""
        return bool(self.category and "кондуктор" in self.category.lower())

    def to_dict(self) -> dict[str, Any]:
        """Convert employee to dictionary for API responses"""
        return {
            "id": self.id,
            "tab_number": self.tab_number,
            "full_name": self.full_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "middle_name": self.middle_name,
            "position": self.position,
            "category": self.category,
            "qualification": self.qualification,
            "hire_date": self.hire_date.isoformat() if self.hire_date else None,
            "department": self.department,
            "shift": self.shift,
            "license_number": self.license_number,
            "license_category": self.license_category,
            "license_expiry": self.license_expiry.isoformat()
            if self.license_expiry
            else None,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "is_active": self.is_active,
            "notes": self.notes,
            "display_name": self.display_name,
            "short_name": self.short_name,
            "is_driver": self.is_driver,
            "is_conductor": self.is_conductor,
        }
