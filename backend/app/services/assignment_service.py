"""Assignment service for fetching real data from MySQL zanaradka table."""

from datetime import date
from typing import Any

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from ..database import engine


def fix_ukrainian_encoding(text: str) -> str:
    """Try to fix Ukrainian text encoding issues."""
    if not text or not isinstance(text, str):
        return text

    # If text contains garbled characters, try to fix encoding
    if any(
        char in text
        for char in [
            "Ð",
            "Ñ",
            "Ò",
            "Ó",
            "Ô",
            "Õ",
            "Ã",
            "°",
            "º",
            "½",
            "¾",
            "¿",
            "»",
            "¼",
        ]
    ):
        try:
            # The data appears to be UTF-8 bytes interpreted as latin-1
            # First encode as latin-1 to get the original bytes, then decode as UTF-8
            byte_data = text.encode("latin-1")
            fixed_text = byte_data.decode("utf-8")
            # Check if the result looks reasonable (contains Cyrillic characters)
            if any("\u0400" <= char <= "\u04ff" for char in fixed_text):
                return fixed_text
        except (UnicodeDecodeError, UnicodeEncodeError):
            try:
                # Alternative: try cp1251 encoding
                fixed_text = text.encode("latin-1").decode("cp1251")
                if any("\u0400" <= char <= "\u04ff" for char in fixed_text):
                    return fixed_text
            except (UnicodeDecodeError, UnicodeEncodeError):
                pass

        # Another approach: try windows-1252 to utf-8
        try:
            fixed_text = text.encode("windows-1252").decode("utf-8")
            if any("\u0400" <= char <= "\u04ff" for char in fixed_text):
                return fixed_text
        except (UnicodeDecodeError, UnicodeEncodeError):
            pass

    return text


class AssignmentService:
    """Service for managing assignment data from MySQL zanaradka table."""

    def __init__(self) -> None:
        self.engine = engine

    def get_simple_assignments(
        self, assignment_date: date | None = None, limit: int = 10
    ) -> dict[str, Any]:
        """Get simple assignment data with basic fields."""
        try:
            target_date = assignment_date or date.today()

            with self.engine.connect() as conn:
                query = text("""
                    SELECT
                        `key` as id,
                        marshrut as route_number,
                        smena as shift,
                        fiovoditel as driver_name,
                        `pe№` as vehicle_number,
                        data_day as assignment_date,
                        tvih as departure_time,
                        tzah as arrival_time,
                        'active' as status
                    FROM zanaradka
                    WHERE data_day = :target_date
                    ORDER BY marshrut, smena
                    LIMIT :limit
                """)

                result = conn.execute(
                    query, {"target_date": target_date, "limit": limit}
                )
                rows = result.fetchall()

                assignments = []
                for row in rows:
                    assignments.append(
                        {
                            "id": row.id,
                            "route_number": str(row.route_number)
                            if row.route_number
                            else "",
                            "shift": str(row.shift) if row.shift else "",
                            "driver_name": fix_ukrainian_encoding(
                                row.driver_name or ""
                            ),
                            "vehicle_number": str(row.vehicle_number)
                            if row.vehicle_number
                            else "",
                            "assignment_date": row.assignment_date.isoformat()
                            if row.assignment_date
                            else None,
                            "departure_time": str(row.departure_time)
                            if row.departure_time
                            else None,
                            "arrival_time": str(row.arrival_time)
                            if row.arrival_time
                            else None,
                            "status": "active",
                        }
                    )

                return {
                    "assignments": assignments,
                    "total_count": len(assignments),
                    "date": target_date.isoformat(),
                }

        except SQLAlchemyError as e:
            print(f"Database error in get_simple_assignments: {e}")
            return {
                "assignments": [],
                "total_count": 0,
                "date": target_date.isoformat(),
            }
        except Exception as e:
            print(f"Error in get_simple_assignments: {e}")
            return {
                "assignments": [],
                "total_count": 0,
                "date": target_date.isoformat(),
            }

    def get_extended_assignments(
        self, assignment_date: date | None = None, limit: int = 50
    ) -> dict[str, Any]:
        """Get extended assignment data with more fields."""
        try:
            target_date = assignment_date or date.today()

            with self.engine.connect() as conn:
                query = text("""
                    SELECT
                        `key` as id,
                        data_day as assignment_date,
                        marshrut as route_number,
                        vipusk as brigade,
                        smena as shift,
                        tabvoditel as driver_tab_number,
                        fiovoditel as driver_name,
                        `pe№` as vehicle_number,
                        tvih as departure_time,
                        tzah as arrival_time,
                        `putlist№` as waybill_number,
                        ZaprAdr as fuel_address,
                        kpvih as route_endpoint,
                        den_nedeli as day_of_week,
                        tipvipusk as route_type,
                        mestootst as parking_place,
                        'active' as status
                    FROM zanaradka
                    WHERE data_day = :target_date
                    ORDER BY marshrut, smena
                    LIMIT :limit
                """)

                result = conn.execute(
                    query, {"target_date": target_date, "limit": limit}
                )
                rows = result.fetchall()

                assignments = []
                for row in rows:
                    assignments.append(
                        {
                            "id": row.id,
                            "assignment_date": row.assignment_date.isoformat()
                            if row.assignment_date
                            else None,
                            "route_number": str(row.route_number)
                            if row.route_number
                            else "",
                            "brigade": str(row.brigade) if row.brigade else "",
                            "shift": str(row.shift) if row.shift else "",
                            "driver_tab_number": str(row.driver_tab_number)
                            if row.driver_tab_number
                            else "",
                            "driver_name": fix_ukrainian_encoding(
                                row.driver_name or ""
                            ),
                            "vehicle_number": str(row.vehicle_number)
                            if row.vehicle_number
                            else "",
                            "departure_time": str(row.departure_time)
                            if row.departure_time
                            else None,
                            "arrival_time": str(row.arrival_time)
                            if row.arrival_time
                            else None,
                            "waybill_number": row.waybill_number or "",
                            "fuel_address": row.fuel_address or "",
                            "route_endpoint": row.route_endpoint or "",
                            "day_of_week": row.day_of_week or "",
                            "route_type": row.route_type or "",
                            "parking_place": row.parking_place or "",
                            "status": "active",
                        }
                    )

                # Calculate statistics
                total_assignments = len(assignments)
                active_assignments = len(
                    [a for a in assignments if a["status"] == "active"]
                )
                total_routes = len({a["route_number"] for a in assignments})

                return {
                    "assignments": assignments,
                    "total_count": total_assignments,
                    "date": target_date.isoformat(),
                    "statistics": {
                        "total_assignments": total_assignments,
                        "active_assignments": active_assignments,
                        "total_routes": total_routes,
                        "completed_assignments": total_assignments - active_assignments,
                    },
                }

        except SQLAlchemyError as e:
            print(f"Database error in get_extended_assignments: {e}")
            return {
                "assignments": [],
                "total_count": 0,
                "date": target_date.isoformat(),
            }
        except Exception as e:
            print(f"Error in get_extended_assignments: {e}")
            return {
                "assignments": [],
                "total_count": 0,
                "date": target_date.isoformat(),
            }

    def get_full_assignments(
        self, assignment_date: date | None = None, limit: int = 100
    ) -> dict[str, Any]:
        """Get full assignment data with all MS Access fields."""
        try:
            target_date = assignment_date or date.today()

            with self.engine.connect() as conn:
                query = text("""
                    SELECT
                        `key` as id,
                        data_day as assignment_date,
                        MONTH(data_day) as month,
                        vipusk as brigade,
                        smena as shift,
                        tipvipusk as route_type,
                        marshrut as route_number,
                        `pe№` as vehicle_number,
                        tabvoditel as driver_tab_number,
                        fiovoditel as driver_name,
                        tabconduktor as conductor_tab_number,
                        fioconduktor as conductor_name,
                        tvih as departure_time,
                        tzah as arrival_time,
                        `putlist№` as waybill_number,
                        ZaprAdr as fuel_address,
                        kpvih as route_endpoint,
                        tob1 as break_1,
                        tob2 as break_2,
                        tPodgotovkaVod as hour1,
                        tPodgotovkaKon as hour2,
                        tSda4aVod as hour3,
                        tSda4aKon as hour4,
                        tVihdepoVod as hour5,
                        tVihdepoKon as departure_vzd,
                        tZahdepoVod as departure_zgd,
                        tZahdepoKon as end_kb,
                        Soobhenie as notes,
                        mestootst as parking_place,
                        den_nedeli as day_of_week,
                        vipusk as internal_number,
                        CASE
                            WHEN tvih IS NOT NULL AND tzah IS NOT NULL THEN
                                TIME_FORMAT(SEC_TO_TIME(
                                    TIME_TO_SEC(tzah) - TIME_TO_SEC(tvih) -
                                    COALESCE(TIME_TO_SEC(tob1), 0) -
                                    COALESCE(TIME_TO_SEC(tob2), 0) -
                                    CASE
                                        WHEN tna4otst IS NOT NULL AND tkonotst IS NOT NULL THEN
                                            TIME_TO_SEC(tkonotst) - TIME_TO_SEC(tna4otst)
                                        ELSE 0
                                    END
                                ), '%H:%i')
                            ELSE NULL
                        END as profit_start,
                        CASE
                            WHEN tvih IS NOT NULL AND tzah IS NOT NULL THEN
                                ROUND(
                                    (TIME_TO_SEC(tzah) - TIME_TO_SEC(tvih) -
                                     COALESCE(TIME_TO_SEC(tob1), 0) -
                                     COALESCE(TIME_TO_SEC(tob2), 0) -
                                     CASE
                                         WHEN tna4otst IS NOT NULL AND tkonotst IS NOT NULL THEN
                                             TIME_TO_SEC(tkonotst) - TIME_TO_SEC(tna4otst)
                                         ELSE 0
                                     END
                                    ) / 3600, 1
                                )
                            ELSE NULL
                        END as profit_end,
                        'active' as status
                    FROM zanaradka
                    WHERE data_day = :target_date
                    ORDER BY marshrut, smena
                    LIMIT :limit
                """)

                result = conn.execute(
                    query, {"target_date": target_date, "limit": limit}
                )
                rows = result.fetchall()

                assignments = []
                for row in rows:
                    assignments.append(
                        {
                            "id": row.id,
                            "assignment_date": row.assignment_date.isoformat()
                            if row.assignment_date
                            else None,
                            "date_charging": row.assignment_date.isoformat()
                            if row.assignment_date
                            else None,
                            "month": str(row.month) if row.month else "",
                            "brigade": str(row.brigade) if row.brigade else "",
                            "shift": str(row.shift) if row.shift else "",
                            "route_type": row.route_type or "",
                            "route_number": str(row.route_number)
                            if row.route_number
                            else "",
                            "internal_number": str(row.internal_number)
                            if row.internal_number
                            else "",
                            "vehicle_number": str(row.vehicle_number)
                            if row.vehicle_number
                            else "",
                            # Для соответствия оригинальной таблице
                            "vehicle_number_for_ro": str(
                                row.vehicle_number
                            )  # Номер ПС для колонки Ро
                            if row.vehicle_number
                            else "",
                            "driver_tab_for_internal": str(
                                row.driver_tab_number
                            )  # Таб номер для колонки № в
                            if row.driver_tab_number
                            else "",
                            "driver_tab_number": str(row.driver_tab_number)
                            if row.driver_tab_number
                            else "",
                            "driver_name": fix_ukrainian_encoding(
                                row.driver_name or ""
                            ),
                            "conductor_tab_number": str(row.conductor_tab_number)
                            if row.conductor_tab_number
                            else "",
                            "conductor_name": fix_ukrainian_encoding(
                                row.conductor_name or ""
                            ),
                            "departure_time": str(row.departure_time)
                            if row.departure_time
                            else "",
                            "arrival_time": str(row.arrival_time)
                            if row.arrival_time
                            else "",
                            "waybill_number": row.waybill_number or "",
                            "fuel_address": row.fuel_address
                            if row.fuel_address and row.fuel_address != "-"
                            else "Barrel",
                            "route_endpoint": row.route_endpoint or "",
                            "parking_place": row.parking_place or "Hospital Emergency",
                            "day_of_week": str(row.day_of_week)
                            if row.day_of_week
                            else "",
                            "hour1": str(row.hour1)
                            if row.hour1 and row.hour1 != "00:00"
                            else "",
                            "hour2": str(row.hour2)
                            if row.hour2 and row.hour2 != "00:00"
                            else "",
                            "hour3": str(row.hour3)
                            if row.hour3 and row.hour3 != "00:00"
                            else "",
                            "hour4": str(row.hour4)
                            if row.hour4 and row.hour4 != "00:00"
                            else "",
                            "hour5": str(row.hour5)
                            if row.hour5 and row.hour5 != "00:00"
                            else "",
                            "break_1": str(row.break_1)
                            if row.break_1 and row.break_1 != "00:00"
                            else "",
                            "break_2": str(row.break_2)
                            if row.break_2 and row.break_2 != "00:00"
                            else "",
                            "profit_start": str(row.profit_start)
                            if row.profit_start and row.profit_start != "00:00"
                            else "",
                            "profit_end": str(row.profit_end)
                            if row.profit_end and row.profit_end != 0
                            else "",
                            "departure_vzd": str(row.departure_vzd)
                            if row.departure_vzd and row.departure_vzd != "00:00"
                            else "",
                            "departure_zgd": str(row.departure_zgd)
                            if row.departure_zgd and row.departure_zgd != "00:00"
                            else "",
                            "end_kb": str(row.end_kb)
                            if row.end_kb and row.end_kb != "00:00"
                            else "",
                            "notes": fix_ukrainian_encoding(row.notes or ""),
                            "status": "active",
                            # Поля для полного соответствия MS Access
                            "address": row.parking_place or "",
                            "driver_waybill": row.waybill_number or "",
                            "vehicle_model": "",  # Нет в базе, заглушка
                            "vehicle_bedt": "",  # Нет в базе, заглушка
                            "coal_info": "",  # Нет в базе, заглушка
                            "application": str(row.route_number)
                            if row.route_number
                            else "",
                        }
                    )

                # Calculate statistics
                total_assignments = len(assignments)
                active_assignments = len(
                    [a for a in assignments if a["status"] == "active"]
                )
                total_routes = len({a["route_number"] for a in assignments})

                return {
                    "assignments": assignments,
                    "total_count": total_assignments,
                    "date": target_date.isoformat(),
                    "statistics": {
                        "total_assignments": total_assignments,
                        "active_assignments": active_assignments,
                        "total_routes": total_routes,
                        "completed_assignments": total_assignments - active_assignments,
                    },
                }

        except SQLAlchemyError as e:
            print(f"Database error in get_full_assignments: {e}")
            return {
                "assignments": [],
                "total_count": 0,
                "date": target_date.isoformat(),
            }
        except Exception as e:
            print(f"Error in get_full_assignments: {e}")
            return {
                "assignments": [],
                "total_count": 0,
                "date": target_date.isoformat(),
            }

    def get_available_dates(self, days_back: int = 30) -> list[str]:
        """Get available dates with assignment data."""
        try:
            with self.engine.connect() as conn:
                query = text("""
                    SELECT DISTINCT data_day as assignment_date
                    FROM zanaradka
                    WHERE data_day >= DATE_SUB(NOW(), INTERVAL :days_back DAY)
                    ORDER BY assignment_date DESC
                """)

                result = conn.execute(query, {"days_back": days_back})
                rows = result.fetchall()

                dates = [row.assignment_date.isoformat() for row in rows]
                return dates

        except SQLAlchemyError as e:
            print(f"Database error in get_available_dates: {e}")
            return []
        except Exception as e:
            print(f"Error in get_available_dates: {e}")
            return []

    def get_statistics(self, assignment_date: date | None = None) -> dict[str, Any]:
        """Get assignment statistics for a specific date."""
        try:
            target_date = assignment_date or date.today()

            with self.engine.connect() as conn:
                query = text("""
                    SELECT
                        COUNT(*) as total_assignments,
                        COUNT(DISTINCT marshrut) as total_routes,
                        COUNT(DISTINCT tabvoditel) as total_drivers,
                        COUNT(DISTINCT `pe№`) as total_vehicles,
                        COUNT(DISTINCT vipusk) as total_brigades
                    FROM zanaradka
                    WHERE data_day = :target_date
                """)

                result = conn.execute(query, {"target_date": target_date})
                row = result.fetchone()

                return {
                    "date": target_date.isoformat(),
                    "total_assignments": row.total_assignments if row else 0,
                    "active_assignments": row.total_assignments if row else 0,  # Assume all are active
                    "completed_assignments": 0,
                    "total_routes": row.total_routes if row else 0,
                    "total_drivers": row.total_drivers if row else 0,
                    "total_vehicles": row.total_vehicles if row else 0,
                    "total_brigades": row.total_brigades if row else 0,
                }

        except SQLAlchemyError as e:
            print(f"Database error in get_statistics: {e}")
            return {"date": target_date.isoformat(), "total_assignments": 0}
        except Exception as e:
            print(f"Error in get_statistics: {e}")
            return {"date": target_date.isoformat(), "total_assignments": 0}


# Global service instance
assignment_service = AssignmentService()
