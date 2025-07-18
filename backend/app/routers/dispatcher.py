"""Enhanced dispatcher router for assignment management with real MySQL data."""

from datetime import date
from typing import Any

from fastapi import APIRouter, HTTPException, Query, Body
from sqlalchemy import text

from ..database import engine
from ..services.assignment_service import assignment_service

router = APIRouter()


@router.get("/check-table-structure")
async def check_table_structure(
    table_name: str = Query("zanaradka", description="Table name to check"),
) -> dict[str, Any]:
    """Check the structure of the zanaradka table to get correct field names."""
    try:
        with engine.connect() as conn:
            # Get table structure
            describe_query = text(f"DESCRIBE {table_name}")
            result = conn.execute(describe_query)
            fields = result.fetchall()

            # Get sample data to see what's in the table
            sample_query = text(f"SELECT * FROM {table_name} LIMIT 3")
            sample_result = conn.execute(sample_query)
            sample_data = sample_result.fetchall()

            # Get column names
            column_names = list(sample_result.keys()) if sample_data else []

            return {
                "table_name": table_name,
                "field_structure": [
                    {
                        "field": field[0],
                        "type": field[1],
                        "null": field[2],
                        "key": field[3],
                        "default": field[4],
                        "extra": field[5],
                    }
                    for field in fields
                ],
                "column_names": column_names,
                "sample_data": [
                    {column_names[i]: value for i, value in enumerate(row)}
                    for row in sample_data
                ],
                "total_fields": len(fields),
            }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error checking table structure: {str(e)}"
        ) from e


@router.get("/test-raw-data")
async def test_raw_data() -> dict[str, Any]:
    """Test endpoint to check raw data in zanaradka table."""
    try:
        with engine.connect() as conn:
            # Count total records
            count_query = text("SELECT COUNT(*) as total FROM zanaradka")
            count_result = conn.execute(count_query)
            total_count = count_result.scalar()

            # Get first 3 records with key fields only
            simple_query = text("""
                SELECT
                    `key`,
                    marshrut,
                    data_day,
                    fiovoditel,
                    smena
                FROM zanaradka
                ORDER BY `key` DESC
                LIMIT 5
            """)

            result = conn.execute(simple_query)
            rows = result.fetchall()

            # Get date range
            date_range_query = text("""
                SELECT
                    MIN(data_day) as min_date,
                    MAX(data_day) as max_date,
                    COUNT(DISTINCT data_day) as unique_dates
                FROM zanaradka
                WHERE data_day IS NOT NULL
            """)

            date_result = conn.execute(date_range_query)
            date_info = date_result.fetchone()

            raw_data = []
            for row in rows:
                raw_data.append(
                    {
                        "key": row[0],
                        "marshrut": row[1],
                        "data_day": str(row[2]) if row[2] else None,
                        "fiovoditel": row[3],
                        "smena": row[4],
                    }
                )

            return {
                "total_records": total_count,
                "sample_records": raw_data,
                "date_range": {
                    "min_date": str(date_info.min_date) if date_info and date_info.min_date else None,
                    "max_date": str(date_info.max_date) if date_info and date_info.max_date else None,
                    "unique_dates": date_info.unique_dates if date_info else 0,
                },
            }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error testing raw data: {str(e)}"
        ) from e


@router.get("/test-encoding")
async def test_encoding(
    assignment_date: str = Query(
        "2025-07-06", description="Assignment date (YYYY-MM-DD)"
    ),
) -> dict[str, Any]:
    """Test endpoint to try different encoding approaches for Ukrainian text."""
    try:
        with engine.connect() as conn:
            query = text("""
                SELECT
                    fiovoditel,
                    fioconduktor
                FROM zanaradka
                WHERE data_day = :target_date
                    AND fiovoditel IS NOT NULL
                    AND fiovoditel != ''
                LIMIT 3
            """)

            result = conn.execute(query, {"target_date": assignment_date})
            rows = result.fetchall()

            encoding_tests = []
            for row in rows:
                driver_name = row.fiovoditel
                conductor_name = row.fioconduktor or ""

                test_result = {
                    "original": driver_name,
                    "conductor_original": conductor_name,
                    "encoding_attempts": {},
                }

                # Try different encoding conversions
                try:
                    # If data is stored as latin-1 but should be cp1251
                    if isinstance(driver_name, str):
                        # Try to encode as latin-1 and decode as cp1251
                        test_result["encoding_attempts"]["latin1_to_cp1251"] = (
                            driver_name.encode("latin-1").decode(
                                "cp1251", errors="ignore"
                            )
                        )
                        # Try to encode as latin-1 and decode as utf-8
                        test_result["encoding_attempts"]["latin1_to_utf8"] = (
                            driver_name.encode("latin-1").decode(
                                "utf-8", errors="ignore"
                            )
                        )
                        # Try to encode as cp1252 and decode as cp1251
                        test_result["encoding_attempts"]["cp1252_to_cp1251"] = (
                            driver_name.encode("cp1252", errors="ignore").decode(
                                "cp1251", errors="ignore"
                            )
                        )
                except Exception as e:
                    test_result["encoding_attempts"]["error"] = str(e)

                encoding_tests.append(test_result)

            return {
                "date": assignment_date,
                "encoding_tests": encoding_tests,
                "message": "Try different encoding conversions to find the correct one",
            }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error in encoding test: {str(e)}"
        ) from e


@router.get("/test-simple-query")
async def test_simple_query(
    assignment_date: str = Query(
        "2025-07-06", description="Assignment date (YYYY-MM-DD)"
    ),
    limit: int = Query(3, description="Number of records to return"),
) -> dict[str, Any]:
    """Test endpoint with minimal fields to debug the WHERE clause."""
    try:
        with engine.connect() as conn:
            # First, test without WHERE to see if query works
            test_query = text("""
                SELECT
                    `key` as id,
                    marshrut as route_number,
                    data_day as assignment_date,
                    fiovoditel as driver_name,
                    smena as shift
                FROM zanaradka
                ORDER BY `key` DESC
                LIMIT :limit
            """)

            result = conn.execute(test_query, {"limit": limit})
            rows_without_where = result.fetchall()

            # Now test with WHERE clause
            date_query = text("""
                SELECT
                    `key` as id,
                    marshrut as route_number,
                    data_day as assignment_date,
                    fiovoditel as driver_name,
                    smena as shift
                FROM zanaradka
                WHERE data_day = :target_date
                ORDER BY `key` DESC
                LIMIT :limit
            """)

            result_with_where = conn.execute(
                date_query, {"target_date": assignment_date, "limit": limit}
            )
            rows_with_where = result_with_where.fetchall()

            # Count records for that date
            count_query = text("""
                SELECT COUNT(*) as count
                FROM zanaradka
                WHERE data_day = :target_date
            """)

            count_result = conn.execute(count_query, {"target_date": assignment_date})
            count_for_date = count_result.scalar()

            return {
                "test_date": assignment_date,
                "records_without_where": [
                    {
                        "id": row.id,
                        "route_number": str(row.route_number)
                        if row.route_number
                        else "",
                        "assignment_date": str(row.assignment_date)
                        if row.assignment_date
                        else None,
                        "driver_name": row.driver_name or "",
                        "shift": str(row.shift) if row.shift else "",
                    }
                    for row in rows_without_where
                ],
                "records_with_where": [
                    {
                        "id": row.id,
                        "route_number": str(row.route_number)
                        if row.route_number
                        else "",
                        "assignment_date": str(row.assignment_date)
                        if row.assignment_date
                        else None,
                        "driver_name": row.driver_name or "",
                        "shift": str(row.shift) if row.shift else "",
                    }
                    for row in rows_with_where
                ],
                "count_for_date": count_for_date,
            }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error in test simple query: {str(e)}"
        ) from e


@router.get("/direct-assignments")
async def get_direct_assignments(
    assignment_date: str = Query(
        "2025-07-06", description="Assignment date (YYYY-MM-DD)"
    ),
    limit: int = Query(10, description="Number of records to return"),
) -> dict[str, Any]:
    """Direct assignment endpoint that bypasses the service layer."""
    try:
        from ..services.assignment_service import fix_ukrainian_encoding

        with engine.connect() as conn:
            query = text("""
                SELECT
                    z.`key` as id,
                    z.marshrut as route_number,
                    z.vipusk as brigade,
                    z.smena as shift,
                    z.tabvoditel as driver_tab_number,
                    z.fiovoditel as driver_name,
                    z.tabconduktor as conductor_tab_number,
                    z.fioconduktor as conductor_name,
                    z.`pe№` as vehicle_number,
                    z.`putlist№` as waybill_number,
                    z.data_day as assignment_date,
                    z.tvih as departure_time,
                    z.tzah as arrival_time,
                    z.tvihmarsrut as departure_vzd,
                    z.tend as arrival_zgd,
                    z.tPodgotovkaVod as preparation_time,
                    z.tSda4aVod as end_time,
                    z.tVihdepoVod as driver_departure_time,
                    z.tZahdepoVod as driver_arrival_time,
                    CASE
                        WHEN z.tvih IS NOT NULL AND z.tzah IS NOT NULL THEN
                            TIME_FORMAT(SEC_TO_TIME(
                                TIME_TO_SEC(z.tzah) - TIME_TO_SEC(z.tvih) -
                                COALESCE(TIME_TO_SEC(z.tob1), 0) -
                                COALESCE(TIME_TO_SEC(z.tob2), 0) -
                                CASE
                                    WHEN z.tna4otst IS NOT NULL AND z.tkonotst IS NOT NULL THEN
                                        TIME_TO_SEC(z.tkonotst) - TIME_TO_SEC(z.tna4otst)
                                    ELSE 0
                                END
                            ), '%H:%i')
                        ELSE NULL
                    END as profit_start,
                    CASE
                        WHEN z.tvih IS NOT NULL AND z.tzah IS NOT NULL THEN
                            TIME_FORMAT(SEC_TO_TIME(
                                TIME_TO_SEC(z.tzah) - TIME_TO_SEC(z.tvih) -
                                COALESCE(TIME_TO_SEC(z.tob1), 0) -
                                COALESCE(TIME_TO_SEC(z.tob2), 0) -
                                CASE
                                    WHEN z.tna4otst IS NOT NULL AND z.tkonotst IS NOT NULL THEN
                                        TIME_TO_SEC(z.tkonotst) - TIME_TO_SEC(z.tna4otst)
                                    ELSE 0
                                END
                            ), '%H:%i')
                        ELSE NULL
                    END as profit_end,
                    z.ZaprAdr as fuel_address,
                    z.zaprv as fuel_number,
                    z.zaprFakt as fuel_actual,
                    z.tipvipusk as route_type,
                    z.kpvih as route_endpoint,
                    z.kpzah as route_endpoint_arrival,
                    z.tob1 as break_1,
                    z.tob2 as break_2,
                    z.mestootst as parking_place,
                    z.Soobhenie as notes,
                    z.den_nedeli as day_of_week,
                    MONTH(z.data_day) as month,
                    t.plan_chas as plan_hours,
                    t.time_pr_depo as hour_prep_depo,
                    t.time_pr_line as hour_prep_line,
                    t.time_pr_vod as hour_prep_driver,
                    t.time_fakt_line as hour_work_actual
                FROM zanaradka z
                LEFT JOIN tabel t ON (t.tab = z.tabvoditel AND t.data_day = z.data_day)
                WHERE z.data_day = :target_date
                ORDER BY z.marshrut, z.smena
                LIMIT :limit
            """)

            result = conn.execute(
                query, {"target_date": assignment_date, "limit": limit}
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
                        "brigade": str(row.brigade) if row.brigade else "",
                        "shift": str(row.shift) if row.shift else "",
                        "driver_tab_number": str(row.driver_tab_number)
                        if row.driver_tab_number
                        else "",
                        "driver_name": fix_ukrainian_encoding(row.driver_name or ""),
                        "conductor_tab_number": str(row.conductor_tab_number)
                        if row.conductor_tab_number
                        else "",
                        "conductor_name": fix_ukrainian_encoding(
                            row.conductor_name or ""
                        ),
                        "vehicle_number": str(row.vehicle_number)
                        if row.vehicle_number
                        else "",
                        "waybill_number": str(row.waybill_number)
                        if row.waybill_number
                        else "",
                        "assignment_date": str(row.assignment_date)
                        if row.assignment_date
                        else None,
                        "departure_time": str(row.departure_time)
                        if row.departure_time
                        else None,
                        "arrival_time": str(row.arrival_time)
                        if row.arrival_time
                        else None,
                        "departure_vzd": str(row.departure_vzd)
                        if row.departure_vzd
                        else None,
                        "arrival_zgd": str(row.arrival_zgd)
                        if row.arrival_zgd
                        else None,
                        "preparation_time": str(row.preparation_time)
                        if row.preparation_time
                        else None,
                        "end_time": str(row.end_time) if row.end_time else None,
                        "driver_departure_time": str(row.driver_departure_time)
                        if row.driver_departure_time
                        else None,
                        "driver_arrival_time": str(row.driver_arrival_time)
                        if row.driver_arrival_time
                        else None,
                        "fuel_address": row.fuel_address or "",
                        "fuel_number": str(row.fuel_number)
                        if row.fuel_number and row.fuel_number != 0
                        else "0",
                        "fuel_actual": str(row.fuel_actual) if row.fuel_actual else "",
                        "route_type": row.route_type or "",
                        "route_endpoint": row.route_endpoint or "",
                        "route_endpoint_arrival": row.route_endpoint_arrival or "",
                        "break_1": str(row.break_1) if row.break_1 else "",
                        "break_2": str(row.break_2) if row.break_2 else "",
                        "parking_place": row.parking_place or "",
                        "notes": fix_ukrainian_encoding(row.notes or ""),
                        "day_of_week": row.day_of_week or "",
                        "month": str(row.month) if row.month else "",
                        "plan_hours": str(row.plan_hours) if row.plan_hours else "",
                        "hour_prep_depo": str(row.hour_prep_depo)
                        if row.hour_prep_depo
                        else "",
                        "hour_prep_line": str(row.hour_prep_line)
                        if row.hour_prep_line
                        else "",
                        "hour_prep_driver": str(row.hour_prep_driver)
                        if row.hour_prep_driver
                        else "",
                        "hour_work_actual": str(row.hour_work_actual)
                        if row.hour_work_actual
                        else "",
                        "profit_start": str(row.profit_start)
                        if row.profit_start
                        else "",
                        "profit_end": str(row.profit_end) if row.profit_end else "",
                        "status": "active",
                    }
                )

            return {
                "assignments": assignments,
                "total_count": len(assignments),
                "date": assignment_date,
                "query_used": "Direct database query bypassing service layer",
            }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error in direct assignments: {str(e)}"
        ) from e


@router.get("/simple-assignments")
async def get_simple_assignments(
    assignment_date: str | None = Query(
        None, description="Assignment date (YYYY-MM-DD)"
    ),
    limit: int = Query(10, description="Number of records to return"),
) -> dict[str, Any]:
    """Get simple list of assignments for dispatcher view."""
    try:
        # Parse date if provided
        target_date = None
        if assignment_date:
            target_date = date.fromisoformat(assignment_date)

        # Get data from service
        result = assignment_service.get_simple_assignments(target_date, limit)

        return result

    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"Invalid date format: {str(e)}"
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching assignments: {str(e)}"
        ) from e


@router.get("/extended-assignments")
async def get_extended_assignments(
    assignment_date: str | None = Query(
        None, description="Assignment date (YYYY-MM-DD)"
    ),
    limit: int = Query(50, description="Number of records to return"),
) -> dict[str, Any]:
    """Get extended list of assignments with more fields for dispatcher view."""
    try:
        # Parse date if provided
        target_date = None
        if assignment_date:
            target_date = date.fromisoformat(assignment_date)

        # Get data from service
        result = assignment_service.get_extended_assignments(target_date, limit)

        return result

    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"Invalid date format: {str(e)}"
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching assignments: {str(e)}"
        ) from e


@router.get("/full-assignments")
async def get_full_assignments(
    assignment_date: str | None = Query(
        None, description="Assignment date (YYYY-MM-DD)"
    ),
    limit: int = Query(100, description="Number of records to return"),
) -> dict[str, Any]:
    """Get full assignment data with all MS Access fields for dispatcher view."""
    try:
        # Parse date if provided
        target_date = None
        if assignment_date:
            target_date = date.fromisoformat(assignment_date)

        # Get data from service
        result = assignment_service.get_full_assignments(target_date, limit)

        return result

    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"Invalid date format: {str(e)}"
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching assignments: {str(e)}"
        ) from e


@router.get("/available-dates")
async def get_available_dates(
    days_back: int = Query(
        30, description="Number of days back to look for available dates"
    ),
) -> dict[str, Any]:
    """Get available dates with assignment data."""
    try:
        dates = assignment_service.get_available_dates(days_back)

        return {"available_dates": dates, "total_count": len(dates)}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching available dates: {str(e)}"
        ) from e


@router.get("/statistics")
async def get_dispatcher_statistics(
    assignment_date: str | None = Query(
        None, description="Assignment date (YYYY-MM-DD)"
    ),
) -> dict[str, Any]:
    """Get comprehensive statistics for dispatcher dashboard."""
    try:
        # Parse date if provided
        target_date = None
        if assignment_date:
            target_date = date.fromisoformat(assignment_date)

        # Get statistics from service
        stats = assignment_service.get_statistics(target_date)

        return stats

    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"Invalid date format: {str(e)}"
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching statistics: {str(e)}"
        ) from e


@router.get("/test-connection")
async def test_database_connection() -> dict[str, Any]:
    """Test database connection to verify everything works."""
    try:
        # Try to get available dates as a connection test
        dates = assignment_service.get_available_dates(7)

        return {
            "status": "success",
            "message": "Database connection successful",
            "available_dates_count": len(dates),
            "sample_dates": dates[:3] if dates else [],
        }

    except Exception as e:
        return {"status": "error", "message": f"Database connection failed: {str(e)}"}


@router.get("/admin/databases")
async def get_available_databases() -> dict[str, Any]:
    """Get list of available databases for admin selection."""
    try:
        with engine.connect() as conn:
            # Get all databases
            query = text("SHOW DATABASES")
            result = conn.execute(query)
            all_databases = [row[0] for row in result.fetchall()]

            # Filter out system databases
            system_dbs = ["information_schema", "mysql", "performance_schema", "sys"]
            user_databases = [db for db in all_databases if db not in system_dbs]

            return {
                "databases": user_databases,
                "default_database": "saltdepoavt_",
                "total_count": len(user_databases),
            }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching databases: {str(e)}"
        ) from e


@router.get("/admin/tables")
async def get_database_tables(
    database_name: str = Query(..., description="Database name"),
) -> dict[str, Any]:
    """Get list of tables in the specified database."""
    try:
        with engine.connect() as conn:
            # Use the specified database
            conn.execute(text(f"USE `{database_name}`"))

            # Get all tables
            query = text("SHOW TABLES")
            result = conn.execute(query)
            tables = [row[0] for row in result.fetchall()]

            # Get table info with row counts and column counts
            table_info = []
            for table in tables:
                try:
                    count_query = text(f"SELECT COUNT(*) FROM `{table}`")
                    count_result = conn.execute(count_query)
                    row_count = count_result.scalar()

                    # Get column count
                    columns_query = text(f"SHOW COLUMNS FROM `{table}`")
                    columns_result = conn.execute(columns_query)
                    column_count = len(columns_result.fetchall())

                    table_info.append(
                        {
                            "name": table,
                            "row_count": row_count,
                            "column_count": column_count,
                        }
                    )
                except Exception:
                    table_info.append(
                        {"name": table, "row_count": 0, "column_count": 0}
                    )

            return {
                "database": database_name,
                "tables": table_info,
                "total_count": len(tables),
            }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching tables: {str(e)}"
        ) from e


@router.get("/admin/table-fields")
async def get_table_fields(
    database_name: str = Query(..., description="Database name"),
    table_name: str = Query(..., description="Table name"),
) -> dict[str, Any]:
    """Get field information for the specified table."""
    try:
        with engine.connect() as conn:
            # Use the specified database
            conn.execute(text(f"USE `{database_name}`"))

            # Get table structure
            describe_query = text(f"DESCRIBE `{table_name}`")
            result = conn.execute(describe_query)
            fields = result.fetchall()

            # Get sample data to understand field content
            sample_query = text(f"SELECT * FROM `{table_name}` LIMIT 3")
            sample_result = conn.execute(sample_query)
            sample_data = sample_result.fetchall()
            column_names = list(sample_result.keys()) if sample_data else []

            field_info = []
            for field in fields:
                field_name = field[0]
                field_type = field[1]
                is_nullable = field[2] == "YES"
                is_key = field[3] != ""
                default_value = field[4]

                # Get sample values for this field
                sample_values = []
                for row in sample_data:
                    if field_name in column_names:
                        field_index = column_names.index(field_name)
                        value = row[field_index]
                        if value is not None:
                            sample_values.append(str(value)[:50])  # Limit to 50 chars

                field_info.append(
                    {
                        "name": field_name,
                        "type": field_type,
                        "nullable": is_nullable,
                        "is_key": is_key,
                        "default_value": default_value,
                        "sample_values": sample_values[:3],  # Max 3 sample values
                    }
                )

            return {
                "database": database_name,
                "table": table_name,
                "fields": field_info,
                "total_fields": len(field_info),
            }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching table fields: {str(e)}"
        ) from e


@router.get("/admin/table-data")
async def get_table_data(
    database_name: str = Query(..., description="Database name"),
    table_name: str = Query(..., description="Table name"),
    columns: str = Query(None, description="Comma-separated list of columns to fetch"),
    limit: int = Query(100, description="Maximum number of records to return"),
) -> dict[str, Any]:
    """Get data from the specified table with optional column filtering."""
    try:
        with engine.connect() as conn:
            # Use the specified database
            conn.execute(text(f"USE `{database_name}`"))

            # Parse columns if provided
            if columns:
                # Clean and validate column names
                column_list = [col.strip() for col in columns.split(",")]
                # Escape column names
                escaped_columns = [f"`{col}`" for col in column_list if col]
                columns_str = ", ".join(escaped_columns)
            else:
                columns_str = "*"

            # Build and execute query
            query = text(f"SELECT {columns_str} FROM `{table_name}` LIMIT {limit}")
            result = conn.execute(query)
            rows = result.fetchall()

            # Get column names
            column_names = list(result.keys())

            # Format data
            data = []
            for row in rows:
                row_dict: dict[str, Any] = {}
                for i, value in enumerate(row):
                    column_name = column_names[i]
                    # Convert values to JSON-serializable format
                    if value is None:
                        row_dict[column_name] = None
                    elif isinstance(value, date):
                        row_dict[column_name] = value.isoformat()
                    else:
                        row_dict[column_name] = str(value)
                data.append(row_dict)

            return {
                "database": database_name,
                "table": table_name,
                "columns": column_names,
                "data": data,
                "total_rows": len(data),
                "limit": limit,
            }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching table data: {str(e)}"
        ) from e


@router.post("/admin/custom-table-data")
async def get_custom_table_data(
    database_name: str = Query(..., description="Database name"),
    table_name: str = Query(..., description="Table name"),
    request: dict = Body(..., description="Custom table configuration with fields"),
    limit: int = Query(100, description="Maximum number of records to return"),
) -> dict[str, Any]:
    """Get data from table with custom fields processed."""
    try:
        with engine.connect() as conn:
            # Use the specified database
            conn.execute(text(f"USE `{database_name}`"))

            # Parse the request
            columns = request.get("columns", [])
            custom_fields = request.get("custom_fields", [])
            
            # Build the SELECT clause
            select_parts = []
            join_clauses = []
            
            # Add regular columns
            for col in columns:
                if not col.get("is_custom", False):
                    select_parts.append(f"`{col['field']}` AS `{col['field']}`")
            
            # Process custom fields
            for field in custom_fields:
                field_sql = generate_custom_field_sql(field, conn, database_name)
                if field_sql:
                    select_parts.append(field_sql)
                    
                    # Add JOIN clauses if needed
                    if field.get("type") == "join":
                        join_sql = generate_join_clause(field, database_name)
                        if join_sql:
                            join_clauses.append(join_sql)
                    elif field.get("type") == "lookup":
                        lookup_sql = generate_lookup_join(field, database_name)
                        if lookup_sql:
                            join_clauses.append(lookup_sql)
            
            # Build the full query
            if not select_parts:
                select_parts = ["*"]
                
            query_parts = [
                f"SELECT {', '.join(select_parts)}",
                f"FROM `{table_name}`"
            ]
            
            # Add JOIN clauses
            for join_clause in join_clauses:
                query_parts.append(join_clause)
            
            # Add GROUP BY for aggregate fields
            group_by_fields = []
            for field in custom_fields:
                if field.get("type") == "aggregate" and field.get("config", {}).get("groupByField"):
                    group_by_fields.append(f"`{field['config']['groupByField']}`")
            
            if group_by_fields:
                query_parts.append(f"GROUP BY {', '.join(group_by_fields)}")
            
            query_parts.append(f"LIMIT {limit}")
            
            final_query = " ".join(query_parts)
            
            # Execute the query
            result = conn.execute(text(final_query))
            rows = result.fetchall()
            
            # Get column names
            column_names = list(result.keys())
            
            # Format data
            data = []
            for row in rows:
                row_dict: dict[str, Any] = {}
                for i, value in enumerate(row):
                    column_name = column_names[i]
                    # Convert values to JSON-serializable format
                    if value is None:
                        row_dict[column_name] = None
                    elif isinstance(value, date):
                        row_dict[column_name] = value.isoformat()
                    else:
                        row_dict[column_name] = str(value)
                data.append(row_dict)
            
            return {
                "database": database_name,
                "table": table_name,
                "columns": column_names,
                "data": data,
                "total_records": len(data),
                "query": final_query  # For debugging
            }
            
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching custom table data: {str(e)}"
        ) from e


def generate_custom_field_sql(field: dict, conn, database_name: str) -> str:
    """Generate SQL for custom field based on its type and configuration."""
    field_type = field.get("type")
    config = field.get("config", {})
    field_name = field.get("name", "custom_field")
    
    if field_type == "calculated":
        return generate_calculated_field_sql(config, field_name)
    elif field_type == "join":
        return generate_join_field_sql(config, field_name)
    elif field_type == "aggregate":
        return generate_aggregate_field_sql(config, field_name)
    elif field_type == "lookup":
        return generate_lookup_field_sql(config, field_name)
    
    return ""


def generate_calculated_field_sql(config: dict, field_name: str) -> str:
    """Generate SQL for calculated fields."""
    calc_type = config.get("calculationType", "")
    
    if calc_type == "time_difference":
        start_field = config.get("startTimeField", "")
        end_field = config.get("endTimeField", "")
        result_format = config.get("resultFormat", "minutes")
        
        if start_field and end_field:
            if result_format == "minutes":
                return f"(TIME_TO_SEC(`{end_field}`) - TIME_TO_SEC(`{start_field}`)) / 60 AS `{field_name}`"
            elif result_format == "hours_minutes":
                # Format as HH:MM without seconds, ensure leading zero for hours
                return f"TIME_FORMAT(SEC_TO_TIME(TIME_TO_SEC(`{end_field}`) - TIME_TO_SEC(`{start_field}`)), '%H:%i') AS `{field_name}`"
            elif result_format == "decimal_hours":
                return f"(TIME_TO_SEC(`{end_field}`) - TIME_TO_SEC(`{start_field}`)) / 3600 AS `{field_name}`"
    
    elif calc_type == "date_difference":
        start_field = config.get("startDateField", "")
        end_field = config.get("endDateField", "")
        
        if start_field and end_field:
            return f"DATEDIFF(`{end_field}`, `{start_field}`) AS `{field_name}`"
    
    elif calc_type == "arithmetic":
        formula = config.get("formula", "")
        if formula:
            # Replace field references {field} with `field`
            import re
            sql_formula = re.sub(r'\{(\w+)\}', r'`\1`', formula)
            return f"({sql_formula}) AS `{field_name}`"
    
    elif calc_type == "concatenation":
        concat_fields = config.get("concatFields", [])
        separator = config.get("separator", ", ")
        
        if concat_fields:
            field_parts = [f"IFNULL(`{field}`, '')" for field in concat_fields]
            return f"CONCAT({f', \'{separator}\', '.join(field_parts)}) AS `{field_name}`"
    
    elif calc_type == "conditional":
        condition_field = config.get("conditionField", "")
        operator = config.get("conditionOperator", "equals")
        condition_value = config.get("conditionValue", "")
        true_value = config.get("trueValue", "")
        false_value = config.get("falseValue", "")
        
        if condition_field and operator:
            sql_operator = get_sql_operator(operator)
            if operator in ["contains", "not_contains"]:
                condition_value = f"%{condition_value}%"
            
            return f"CASE WHEN `{condition_field}` {sql_operator} '{condition_value}' THEN '{true_value}' ELSE '{false_value}' END AS `{field_name}`"
    
    return ""


def generate_join_field_sql(config: dict, field_name: str) -> str:
    """Generate SQL for join fields."""
    join_table = config.get("joinTable", "")
    display_field = config.get("joinDisplayField", "")
    
    if join_table and display_field:
        return f"`{join_table}`.`{display_field}` AS `{field_name}`"
    
    return ""


def generate_aggregate_field_sql(config: dict, field_name: str) -> str:
    """Generate SQL for aggregate fields."""
    function = config.get("aggregateFunction", "COUNT")
    agg_field = config.get("aggregateField", "")
    
    if function == "COUNT":
        return f"COUNT(*) AS `{field_name}`"
    elif function and agg_field:
        return f"{function}(`{agg_field}`) AS `{field_name}`"
    
    return ""


def generate_lookup_field_sql(config: dict, field_name: str) -> str:
    """Generate SQL for lookup fields."""
    lookup_table = config.get("lookupTable", "")
    display_field = config.get("lookupDisplayField", "")
    
    if lookup_table and display_field:
        return f"lookup_table.`{display_field}` AS `{field_name}`"
    
    return ""


def generate_join_clause(config: dict, database_name: str) -> str:
    """Generate JOIN clause for join fields."""
    join_table = config.get("joinTable", "")
    source_field = config.get("joinSourceField", "")
    target_field = config.get("joinTargetField", "")
    join_type = config.get("joinType", "LEFT")
    
    if join_table and source_field and target_field:
        return f"{join_type} JOIN `{join_table}` ON `{source_field}` = `{join_table}`.`{target_field}`"
    
    return ""


def generate_lookup_join(config: dict, database_name: str) -> str:
    """Generate JOIN clause for lookup fields."""
    lookup_table = config.get("lookupTable", "")
    key_field = config.get("lookupKeyField", "")
    search_field = config.get("lookupSearchField", "")
    
    if lookup_table and key_field and search_field:
        return f"LEFT JOIN `{lookup_table}` AS lookup_table ON `{key_field}` = lookup_table.`{search_field}`"
    
    return ""


def get_sql_operator(operator: str) -> str:
    """Convert operator to SQL operator."""
    operators = {
        "equals": "=",
        "not_equals": "!=",
        "greater": ">",
        "less": "<",
        "contains": "LIKE",
        "not_contains": "NOT LIKE"
    }
    return operators.get(operator, "=")
