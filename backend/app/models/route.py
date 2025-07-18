"""
Route model for dispatcher functionality
Based on sprmarshrut table structure from database analysis
"""

from typing import Any

from sqlalchemy import Boolean, Column, Integer, String, Text

from .base import Base


class Route(Base):
    """
    Model for routes (маршруты) - reference table for dispatcher functionality
    Based on sprmarshrut table with 296 records
    """

    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)

    # Route identification
    number = Column(
        Integer, nullable=False, unique=True, index=True, comment="Номер маршрута"
    )
    name = Column(String(255), nullable=True, comment="Название маршрута")

    # Route endpoints
    start_point = Column(String(255), nullable=True, comment="Начальная остановка")
    end_point = Column(String(255), nullable=True, comment="Конечная остановка")

    # Route characteristics
    route_type = Column(
        String(50), nullable=True, comment="Тип маршрута (трамвай, троллейбус, автобус)"
    )
    distance = Column(Integer, nullable=True, comment="Протяженность маршрута в метрах")
    travel_time = Column(Integer, nullable=True, comment="Время в пути в минутах")

    # Schedule information
    first_departure = Column(String(10), nullable=True, comment="Время первого рейса")
    last_departure = Column(String(10), nullable=True, comment="Время последнего рейса")
    interval_peak = Column(
        Integer, nullable=True, comment="Интервал в час пик (минуты)"
    )
    interval_normal = Column(
        Integer, nullable=True, comment="Интервал в обычное время (минуты)"
    )

    # Technical information
    depot = Column(String(100), nullable=True, comment="Депо")
    fuel_address = Column(String(255), nullable=True, comment="Адрес заправки")
    garage_address = Column(String(255), nullable=True, comment="Адрес гаража")

    # Status
    is_active = Column(Boolean, default=True, comment="Активный маршрут")
    is_deleted = Column(Boolean, default=False, comment="Флаг удаления")

    # Additional information
    description = Column(Text, nullable=True, comment="Описание маршрута")
    notes = Column(Text, nullable=True, comment="Примечания")

    # Relationships
    # assignments = relationship("Assignment", back_populates="route")

    def __repr__(self) -> str:
        return f"<Route(id={self.id}, number={self.number}, name={self.name})>"

    @property
    def display_name(self) -> str:
        """Human readable route name"""
        if self.name:
            return f"№{self.number} - {self.name}"
        return f"Маршрут №{self.number}"

    @property
    def route_info(self) -> str:
        """Full route information"""
        if self.start_point and self.end_point:
            return f"{self.start_point} - {self.end_point}"
        return self.display_name

    def to_dict(self) -> dict[str, Any]:
        """Convert route to dictionary for API responses"""
        return {
            "id": self.id,
            "number": self.number,
            "name": self.name,
            "start_point": self.start_point,
            "end_point": self.end_point,
            "route_type": self.route_type,
            "distance": self.distance,
            "travel_time": self.travel_time,
            "first_departure": self.first_departure,
            "last_departure": self.last_departure,
            "interval_peak": self.interval_peak,
            "interval_normal": self.interval_normal,
            "depot": self.depot,
            "fuel_address": self.fuel_address,
            "garage_address": self.garage_address,
            "is_active": self.is_active,
            "description": self.description,
            "notes": self.notes,
            "display_name": self.display_name,
            "route_info": self.route_info,
        }
