"""
Enhanced Assignment model for dispatcher functionality
Based on zanaradka table structure from MS Access database analysis
Includes all fields visible in the provided MS Access images
"""

from typing import Any

from sqlalchemy import Boolean, Column, Date, Integer, String, Text, Time

from .base import Base


class Assignment(Base):
    """
    Enhanced model for assignments (наряды) - main table for dispatcher functionality
    Based on zanaradka table with all fields from MS Access interface
    """

    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)

    # Date and time information
    assignment_date = Column(Date, nullable=False, index=True, comment="Дата зарядки")
    month = Column(Integer, nullable=True, comment="Месяц (Мт)")

    # Brigade and shift information
    brigade = Column(String(10), nullable=True, comment="Бригада (Бр)")
    shift = Column(String(10), nullable=True, index=True, comment="Смена")

    # Application and address
    application_number = Column(String(50), nullable=True, comment="Заявка")
    address = Column(String(255), nullable=True, comment="Адрес")

    # Route and type information
    route_number = Column(Integer, nullable=False, index=True, comment="Номер маршрута")
    route_type = Column(String(50), nullable=True, comment="Тип")
    internal_number = Column(String(50), nullable=True, comment="№ в")

    # Fuel information
    fuel_route = Column(String(100), nullable=True, comment="Маршрут топливо")
    fuel_address = Column(String(255), nullable=True, comment="Адрес заправки")

    # Driver waybill information
    driver_waybill = Column(String(50), nullable=True, comment="ПБ вод")

    # Working hours (5 different hour periods)
    hour1 = Column(Time, nullable=True, comment="Час1")
    hour2 = Column(Time, nullable=True, comment="Час2")
    hour3 = Column(Time, nullable=True, comment="Час3")
    hour4 = Column(Time, nullable=True, comment="Час4")
    hour5 = Column(Time, nullable=True, comment="Час5")

    # Waybill and departure information
    waybill_number = Column(String(50), nullable=True, comment="П.Б.")
    departure_vzd = Column(Time, nullable=True, comment="Взд (время выезда)")
    departure_zgd = Column(Time, nullable=True, comment="Згд (время заезда)")

    # End time and shifts
    end_kb = Column(Time, nullable=True, comment="К.Б.")
    break_1 = Column(Time, nullable=True, comment="Пер.1")
    break_2 = Column(Time, nullable=True, comment="Пер.2")

    # Profitability and efficiency
    profit_start = Column(Time, nullable=True, comment="П.выг")
    profit_end = Column(Time, nullable=True, comment="К.выг")

    # Vehicle information
    vehicle_number = Column(String(50), nullable=True, index=True, comment="Н.авт")
    vehicle_model = Column(String(100), nullable=True, comment="М.авт")
    vehicle_bedt = Column(String(50), nullable=True, comment="М.Бедт")

    # Additional information
    coal_info = Column(String(50), nullable=True, comment="Вугл")
    vehicle_type_pc = Column(String(50), nullable=True, comment="Тип PC")
    state_number_pc = Column(String(50), nullable=True, comment="Держ.№ PC")

    # Driver and conductor information
    driver_tab_number = Column(
        Integer, nullable=True, index=True, comment="Табельный номер водителя"
    )
    driver_name = Column(String(255), nullable=True, comment="ФИО водителя")
    conductor_tab_number = Column(
        Integer, nullable=True, comment="Табельный номер кондуктора"
    )
    conductor_name = Column(String(255), nullable=True, comment="ФИО кондуктора")

    # Standard schedule information
    departure_time = Column(Time, nullable=True, comment="Время выхода")
    arrival_time = Column(Time, nullable=True, comment="Время захода")

    # Route endpoints
    route_endpoint = Column(String(255), nullable=True, comment="Конечная остановка")

    # Status and control
    is_deleted = Column(Boolean, default=False, comment="Флаг удаления")
    status = Column(String(50), default="active", comment="Статус наряда")

    # Additional notes
    notes = Column(Text, nullable=True, comment="Примечания")

    # Relationships (will be defined when creating related models)
    # route = relationship("Route", back_populates="assignments")
    # driver = relationship("Employee", foreign_keys=[driver_tab_number], back_populates="driver_assignments")
    # conductor = relationship("Employee", foreign_keys=[conductor_tab_number], back_populates="conductor_assignments")
    # vehicle = relationship("Vehicle", back_populates="assignments")

    def __repr__(self) -> str:
        return f"<Assignment(id={self.id}, route={self.route_number}, date={self.assignment_date}, driver={self.driver_name})>"

    @property
    def display_name(self) -> str:
        """Human readable assignment name"""
        return (
            f"Маршрут {self.route_number}, {self.assignment_date.strftime('%d.%m.%Y')}"
        )

    @property
    def shift_display(self) -> str:
        """Human readable shift"""
        shift_names = {"1": "1-я смена", "2": "2-я смена", "3": "3-я смена"}
        return shift_names.get(self.shift or "", self.shift or "")  # type: ignore[arg-type]

    @property
    def working_hours_summary(self) -> str | None:
        """Summary of all working hours"""
        hours = []
        for i in range(1, 6):
            hour = getattr(self, f"hour{i}")
            if hour:
                hours.append(f"Час{i}: {hour.strftime('%H:%M')}")
        return "; ".join(hours) if hours else None

    @property
    def breaks_summary(self) -> str | None:
        """Summary of break periods"""
        breaks = []
        if self.break_1:
            breaks.append(f"Перерыв 1: {self.break_1.strftime('%H:%M')}")
        if self.break_2:
            breaks.append(f"Перерыв 2: {self.break_2.strftime('%H:%M')}")
        return "; ".join(breaks) if breaks else None

    @property
    def full_vehicle_info(self) -> str | None:
        """Complete vehicle information"""
        parts = []
        if self.vehicle_number:
            parts.append(f"№{self.vehicle_number}")
        if self.vehicle_model:
            parts.append(str(self.vehicle_model))
        if self.state_number_pc:
            parts.append(f"г/н {self.state_number_pc}")
        return " - ".join(parts) if parts else None

    def to_dict(self) -> dict[str, Any]:
        """Convert assignment to dictionary for API responses"""
        return {
            "id": self.id,
            "assignment_date": self.assignment_date.isoformat()
            if self.assignment_date
            else None,
            "month": self.month,
            "brigade": self.brigade,
            "shift": self.shift,
            "shift_display": self.shift_display,
            "application_number": self.application_number,
            "address": self.address,
            "route_number": self.route_number,
            "route_type": self.route_type,
            "internal_number": self.internal_number,
            "fuel_route": self.fuel_route,
            "fuel_address": self.fuel_address,
            "driver_waybill": self.driver_waybill,
            "hour1": self.hour1.strftime("%H:%M") if self.hour1 else None,
            "hour2": self.hour2.strftime("%H:%M") if self.hour2 else None,
            "hour3": self.hour3.strftime("%H:%M") if self.hour3 else None,
            "hour4": self.hour4.strftime("%H:%M") if self.hour4 else None,
            "hour5": self.hour5.strftime("%H:%M") if self.hour5 else None,
            "waybill_number": self.waybill_number,
            "departure_vzd": self.departure_vzd.strftime("%H:%M")
            if self.departure_vzd
            else None,
            "departure_zgd": self.departure_zgd.strftime("%H:%M")
            if self.departure_zgd
            else None,
            "end_kb": self.end_kb.strftime("%H:%M") if self.end_kb else None,
            "break_1": self.break_1.strftime("%H:%M") if self.break_1 else None,
            "break_2": self.break_2.strftime("%H:%M") if self.break_2 else None,
            "profit_start": self.profit_start.strftime("%H:%M")
            if self.profit_start
            else None,
            "profit_end": self.profit_end.strftime("%H:%M")
            if self.profit_end
            else None,
            "vehicle_number": self.vehicle_number,
            "vehicle_model": self.vehicle_model,
            "vehicle_bedt": self.vehicle_bedt,
            "coal_info": self.coal_info,
            "vehicle_type_pc": self.vehicle_type_pc,
            "state_number_pc": self.state_number_pc,
            "driver_tab_number": self.driver_tab_number,
            "driver_name": self.driver_name,
            "conductor_tab_number": self.conductor_tab_number,
            "conductor_name": self.conductor_name,
            "departure_time": self.departure_time.strftime("%H:%M")
            if self.departure_time
            else None,
            "arrival_time": self.arrival_time.strftime("%H:%M")
            if self.arrival_time
            else None,
            "route_endpoint": self.route_endpoint,
            "status": self.status,
            "notes": self.notes,
            "display_name": self.display_name,
            "working_hours_summary": self.working_hours_summary,
            "breaks_summary": self.breaks_summary,
            "full_vehicle_info": self.full_vehicle_info,
        }

    def to_simple_dict(self) -> dict[str, Any]:
        """Convert assignment to simplified dictionary for simple table view"""
        return {
            "id": self.id,
            "route_number": self.route_number,
            "shift": self.shift,
            "shift_display": self.shift_display,
            "driver_name": self.driver_name,
            "conductor_name": self.conductor_name,
            "vehicle_number": self.vehicle_number,
            "assignment_date": self.assignment_date.isoformat()
            if self.assignment_date
            else None,
            "departure_time": self.departure_time.strftime("%H:%M")
            if self.departure_time
            else None,
            "arrival_time": self.arrival_time.strftime("%H:%M")
            if self.arrival_time
            else None,
            "status": self.status,
            "display_name": self.display_name,
        }

    def to_extended_dict(self) -> dict[str, Any]:
        """Convert assignment to extended dictionary for detailed table view"""
        return {
            "id": self.id,
            "route_number": self.route_number,
            "brigade": self.brigade,
            "shift": self.shift,
            "shift_display": self.shift_display,
            "driver_tab_number": self.driver_tab_number,
            "driver_name": self.driver_name,
            "conductor_tab_number": self.conductor_tab_number,
            "conductor_name": self.conductor_name,
            "vehicle_number": self.vehicle_number,
            "state_number_pc": self.state_number_pc,
            "assignment_date": self.assignment_date.isoformat()
            if self.assignment_date
            else None,
            "departure_time": self.departure_time.strftime("%H:%M")
            if self.departure_time
            else None,
            "arrival_time": self.arrival_time.strftime("%H:%M")
            if self.arrival_time
            else None,
            "waybill_number": self.waybill_number,
            "fuel_address": self.fuel_address,
            "route_endpoint": self.route_endpoint,
            "working_hours_summary": self.working_hours_summary,
            "breaks_summary": self.breaks_summary,
            "status": self.status,
            "notes": self.notes,
            "display_name": self.display_name,
        }
