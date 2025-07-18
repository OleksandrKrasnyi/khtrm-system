"""
Vehicle model for dispatcher functionality
Based on sprpe table structure from database analysis
"""

from typing import Any

from sqlalchemy import Boolean, Column, Date, Integer, String, Text

from .base import Base


class Vehicle(Base):
    """
    Model for vehicles (транспорт) - reference table for dispatcher functionality
    Based on sprpe table with 218 records
    """

    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)

    # Vehicle identification
    internal_number = Column(
        String(50),
        nullable=False,
        unique=True,
        index=True,
        comment="Внутренний номер ПС",
    )
    state_number = Column(
        String(50), nullable=True, index=True, comment="Государственный номер"
    )

    # Vehicle information
    vehicle_type = Column(
        String(50), nullable=True, comment="Тип ПС (автобус, троллейбус, трамвай)"
    )
    model = Column(String(100), nullable=True, comment="Модель")
    manufacturer = Column(String(100), nullable=True, comment="Производитель")
    year = Column(Integer, nullable=True, comment="Год выпуска")

    # Technical specifications
    capacity = Column(Integer, nullable=True, comment="Вместимость (пассажиров)")
    fuel_type = Column(String(50), nullable=True, comment="Тип топлива")
    engine_type = Column(String(100), nullable=True, comment="Тип двигателя")

    # Operational information
    route_number = Column(Integer, nullable=True, comment="Закрепленный маршрут")
    depot = Column(String(100), nullable=True, comment="Депо")
    garage_number = Column(String(50), nullable=True, comment="Номер гаража")

    # Status and maintenance
    status = Column(
        String(50), default="active", comment="Статус (active, repair, decommissioned)"
    )
    is_active = Column(Boolean, default=True, comment="Активный ПС")
    is_deleted = Column(Boolean, default=False, comment="Флаг удаления")

    # Dates
    acquisition_date = Column(Date, nullable=True, comment="Дата поступления")
    last_maintenance = Column(Date, nullable=True, comment="Дата последнего ТО")
    next_maintenance = Column(Date, nullable=True, comment="Дата следующего ТО")

    # Additional information
    notes = Column(Text, nullable=True, comment="Примечания")
    description = Column(Text, nullable=True, comment="Описание")

    # Relationships
    # assignments = relationship("Assignment", back_populates="vehicle")

    def __repr__(self) -> str:
        return f"<Vehicle(id={self.id}, internal_number={self.internal_number}, model={self.model})>"

    @property
    def display_name(self) -> str:
        """Human readable vehicle name"""
        if self.model:
            return f"№{self.internal_number} - {self.model}"
        return f"ПС №{self.internal_number}"

    @property
    def full_name(self) -> str:
        """Full vehicle information"""
        parts = [f"№{self.internal_number}"]
        if self.model:
            parts.append(str(self.model))
        if self.state_number:
            parts.append(f"г/н {self.state_number}")
        return " - ".join(parts)

    @property
    def status_display(self) -> str:
        """Human readable status"""
        status_names = {
            "active": "В работе",
            "repair": "В ремонте",
            "maintenance": "На ТО",
            "decommissioned": "Списан",
            "reserve": "Резерв",
        }
        return status_names.get(self.status or "", self.status or "")  # type: ignore[arg-type]

    def to_dict(self) -> dict[str, Any]:
        """Convert vehicle to dictionary for API responses"""
        return {
            "id": self.id,
            "internal_number": self.internal_number,
            "state_number": self.state_number,
            "vehicle_type": self.vehicle_type,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "year": self.year,
            "capacity": self.capacity,
            "fuel_type": self.fuel_type,
            "engine_type": self.engine_type,
            "route_number": self.route_number,
            "depot": self.depot,
            "garage_number": self.garage_number,
            "status": self.status,
            "status_display": self.status_display,
            "is_active": self.is_active,
            "acquisition_date": self.acquisition_date.isoformat()
            if self.acquisition_date
            else None,
            "last_maintenance": self.last_maintenance.isoformat()
            if self.last_maintenance
            else None,
            "next_maintenance": self.next_maintenance.isoformat()
            if self.next_maintenance
            else None,
            "notes": self.notes,
            "description": self.description,
            "display_name": self.display_name,
            "full_name": self.full_name,
        }
