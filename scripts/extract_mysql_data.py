#!/usr/bin/env python3
"""
Enhanced MySQL Data Extraction Script for KHTRM System
Extracts all fields from the zanaradka table to match the enhanced Assignment model
Based on MS Access table structure analysis
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any

import mysql.connector
from mysql.connector import Error

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("mysql_extraction.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Database configuration
DB_CONFIG = {
    "host": "localhost",  # или IP удаленного сервера
    "port": 3306,
    "user": "khtrm_remote",
    "password": os.getenv("MYSQL_PASSWORD", "your_password_here"),
    "database": "saltdepoavt_",
    "charset": "utf8mb4",
}


class MySQLDataExtractor:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.output_dir = Path("extracted_mysql_data")
        self.output_dir.mkdir(exist_ok=True)

    def connect_to_database(self) -> bool:
        """Connect to MySQL database"""
        try:
            logger.info(
                f"Connecting to MySQL database at {DB_CONFIG['host']}:{DB_CONFIG['port']}"
            )
            self.connection = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.connection.cursor(dictionary=True)
            logger.info("✅ Successfully connected to MySQL database")
            return True
        except Error as e:
            logger.error(f"❌ Failed to connect to MySQL database: {e}")
            return False

    def test_connection(self) -> dict[str, Any]:
        """Test database connection and get basic info"""
        try:
            # Test connection
            self.cursor.execute("SELECT VERSION()")
            mysql_version = self.cursor.fetchone()

            # Get database info
            self.cursor.execute("SHOW DATABASES")
            databases = self.cursor.fetchall()

            # Get current database tables
            self.cursor.execute("SHOW TABLES")
            tables = self.cursor.fetchall()

            return {
                "status": "success",
                "mysql_version": mysql_version,
                "available_databases": [db["Database"] for db in databases],
                "current_database": DB_CONFIG["database"],
                "tables": [
                    table[f"Tables_in_{DB_CONFIG['database']}"] for table in tables
                ],
            }
        except Error as e:
            logger.error(f"❌ Database connection test failed: {e}")
            return {"status": "error", "error": str(e)}

    def analyze_zanaradka_table(self) -> dict[str, Any]:
        """Analyze the zanaradka table structure"""
        try:
            logger.info("🔍 Analyzing zanaradka table structure...")

            # Get table structure
            self.cursor.execute("DESCRIBE zanaradka")
            table_structure = self.cursor.fetchall()

            # Get table info
            self.cursor.execute("SHOW TABLE STATUS LIKE 'zanaradka'")
            table_info = self.cursor.fetchone()

            # Get row count
            self.cursor.execute("SELECT COUNT(*) as total_rows FROM zanaradka")
            row_count = self.cursor.fetchone()

            # Get sample data
            self.cursor.execute("SELECT * FROM zanaradka LIMIT 5")
            sample_data = self.cursor.fetchall()

            # Get date range
            self.cursor.execute("""
                SELECT
                    MIN(data_day) as min_date,
                    MAX(data_day) as max_date
                FROM zanaradka
                WHERE data_day IS NOT NULL
            """)
            date_range = self.cursor.fetchone()

            analysis = {
                "table_structure": table_structure,
                "table_info": table_info,
                "total_rows": row_count["total_rows"],
                "date_range": date_range,
                "sample_data": sample_data,
                "analysis_timestamp": datetime.now().isoformat(),
            }

            logger.info(f"✅ Table analysis complete: {row_count['total_rows']} rows")
            return analysis

        except Error as e:
            logger.error(f"❌ Failed to analyze zanaradka table: {e}")
            return {"error": str(e)}

    def extract_assignments_data(
        self,
        limit: int | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> dict[str, Any]:
        """Extract assignments data with all MS Access fields"""
        try:
            logger.info("🔄 Extracting assignments data...")

            # Build query with all fields matching enhanced Assignment model
            query = """
                SELECT
                    -- Basic identification
                    marshrut as route_number,
                    vipusk as route_release,
                    smena as shift,
                    data_day as assignment_date,
                    MONTH(data_day) as month,

                    -- Personnel information
                    tabvoditel as driver_tab_number,
                    fiovoditel as driver_name,
                    tabconduktor as conductor_tab_number,
                    fioconduktor as conductor_name,

                    -- Vehicle information
                    pe№ as vehicle_number,

                    -- Time information
                    tvih as departure_time,
                    tzah as arrival_time,

                    -- Documentation
                    putlist№ as waybill_number,

                    -- Additional fields that might exist in the table
                    -- These field names are guessed based on MS Access interface
                    -- You may need to adjust these based on actual table structure

                    -- Try to map MS Access fields to MySQL fields
                    -- This mapping might need adjustment based on actual table structure
                    brigade as brigade,
                    application as application_number,
                    address as address,
                    type as route_type,
                    internal_num as internal_number,
                    fuel_route as fuel_route,
                    fuel_address as fuel_address,
                    driver_waybill as driver_waybill,

                    -- Working hours (if they exist as separate fields)
                    hour1 as hour1,
                    hour2 as hour2,
                    hour3 as hour3,
                    hour4 as hour4,
                    hour5 as hour5,

                    -- Departure/arrival times
                    departure_vzd as departure_vzd,
                    departure_zgd as departure_zgd,
                    end_kb as end_kb,

                    -- Breaks
                    break_1 as break_1,
                    break_2 as break_2,

                    -- Profitability
                    profit_start as profit_start,
                    profit_end as profit_end,

                    -- Vehicle details
                    vehicle_model as vehicle_model,
                    vehicle_bedt as vehicle_bedt,
                    coal_info as coal_info,
                    vehicle_type_pc as vehicle_type_pc,
                    state_number_pc as state_number_pc,

                    -- Route endpoint
                    route_endpoint as route_endpoint,

                    -- Status and notes
                    status as status,
                    notes as notes

                FROM zanaradka
                WHERE 1=1
            """

            # Add date filters if provided
            params = []
            if start_date:
                query += " AND data_day >= %s"
                params.append(start_date)
            if end_date:
                query += " AND data_day <= %s"
                params.append(end_date)

            # Add ordering and limit
            query += " ORDER BY data_day DESC, marshrut, smena"
            if limit:
                query += " LIMIT %s"
                params.append(limit)

            logger.info(f"Executing query with params: {params}")
            self.cursor.execute(query, params)

            # Fetch all results
            assignments = []
            rows = self.cursor.fetchall()

            logger.info(f"Processing {len(rows)} assignment records...")

            for row in rows:
                # Convert MySQL result to our enhanced format
                assignment = {
                    "route_number": row.get("route_number"),
                    "route_release": row.get("route_release"),
                    "shift": str(row.get("shift")) if row.get("shift") else None,
                    "assignment_date": row.get("assignment_date").isoformat()
                    if row.get("assignment_date")
                    else None,
                    "month": row.get("month"),
                    "brigade": row.get("brigade"),
                    "application_number": row.get("application_number"),
                    "address": row.get("address"),
                    "route_type": row.get("route_type"),
                    "internal_number": row.get("internal_number"),
                    "fuel_route": row.get("fuel_route"),
                    "fuel_address": row.get("fuel_address"),
                    "driver_waybill": row.get("driver_waybill"),
                    "driver_tab_number": row.get("driver_tab_number"),
                    "driver_name": row.get("driver_name"),
                    "conductor_tab_number": row.get("conductor_tab_number"),
                    "conductor_name": row.get("conductor_name"),
                    "vehicle_number": row.get("vehicle_number"),
                    "vehicle_model": row.get("vehicle_model"),
                    "vehicle_bedt": row.get("vehicle_bedt"),
                    "coal_info": row.get("coal_info"),
                    "vehicle_type_pc": row.get("vehicle_type_pc"),
                    "state_number_pc": row.get("state_number_pc"),
                    "departure_time": str(row.get("departure_time"))
                    if row.get("departure_time")
                    else None,
                    "arrival_time": str(row.get("arrival_time"))
                    if row.get("arrival_time")
                    else None,
                    "hour1": str(row.get("hour1")) if row.get("hour1") else None,
                    "hour2": str(row.get("hour2")) if row.get("hour2") else None,
                    "hour3": str(row.get("hour3")) if row.get("hour3") else None,
                    "hour4": str(row.get("hour4")) if row.get("hour4") else None,
                    "hour5": str(row.get("hour5")) if row.get("hour5") else None,
                    "waybill_number": row.get("waybill_number"),
                    "departure_vzd": str(row.get("departure_vzd"))
                    if row.get("departure_vzd")
                    else None,
                    "departure_zgd": str(row.get("departure_zgd"))
                    if row.get("departure_zgd")
                    else None,
                    "end_kb": str(row.get("end_kb")) if row.get("end_kb") else None,
                    "break_1": str(row.get("break_1")) if row.get("break_1") else None,
                    "break_2": str(row.get("break_2")) if row.get("break_2") else None,
                    "profit_start": str(row.get("profit_start"))
                    if row.get("profit_start")
                    else None,
                    "profit_end": str(row.get("profit_end"))
                    if row.get("profit_end")
                    else None,
                    "route_endpoint": row.get("route_endpoint"),
                    "status": row.get("status", "active"),
                    "notes": row.get("notes"),
                }
                assignments.append(assignment)

            logger.info(f"✅ Successfully extracted {len(assignments)} assignments")

            return {
                "assignments": assignments,
                "total_count": len(assignments),
                "extraction_timestamp": datetime.now().isoformat(),
                "query_parameters": {
                    "limit": limit,
                    "start_date": start_date,
                    "end_date": end_date,
                },
            }

        except Error as e:
            logger.error(f"❌ Failed to extract assignments data: {e}")
            return {"error": str(e)}

    def extract_reference_data(self) -> dict[str, Any]:
        """Extract reference data from related tables"""
        try:
            logger.info("🔄 Extracting reference data...")

            reference_data = {}

            # Extract routes (sprmarshrut)
            try:
                self.cursor.execute("SELECT * FROM sprmarshrut LIMIT 100")
                routes = self.cursor.fetchall()
                reference_data["routes"] = routes
                logger.info(f"✅ Extracted {len(routes)} routes")
            except Error as e:
                logger.warning(f"⚠️ Failed to extract routes: {e}")

            # Extract personnel (sprpersonal)
            try:
                self.cursor.execute("SELECT * FROM sprpersonal LIMIT 1000")
                personnel = self.cursor.fetchall()
                reference_data["personnel"] = personnel
                logger.info(f"✅ Extracted {len(personnel)} personnel records")
            except Error as e:
                logger.warning(f"⚠️ Failed to extract personnel: {e}")

            # Extract vehicles (sprpe)
            try:
                self.cursor.execute("SELECT * FROM sprpe LIMIT 500")
                vehicles = self.cursor.fetchall()
                reference_data["vehicles"] = vehicles
                logger.info(f"✅ Extracted {len(vehicles)} vehicles")
            except Error as e:
                logger.warning(f"⚠️ Failed to extract vehicles: {e}")

            return reference_data

        except Error as e:
            logger.error(f"❌ Failed to extract reference data: {e}")
            return {"error": str(e)}

    def save_extraction_results(self, data: dict[str, Any], filename: str = None):
        """Save extraction results to JSON file"""
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"mysql_extraction_{timestamp}.json"

            output_file = self.output_dir / filename

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)

            logger.info(f"✅ Extraction results saved to: {output_file}")
            return str(output_file)

        except Exception as e:
            logger.error(f"❌ Failed to save extraction results: {e}")
            return None

    def generate_extraction_report(self, extraction_data: dict[str, Any]) -> str:
        """Generate extraction report"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = self.output_dir / f"extraction_report_{timestamp}.md"

            with open(report_file, "w", encoding="utf-8") as f:
                f.write("# MySQL Data Extraction Report\n\n")
                f.write(
                    f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                )

                if "assignments" in extraction_data:
                    assignments = extraction_data["assignments"]
                    f.write("## Assignments Data\n\n")
                    f.write(f"- **Total Records:** {len(assignments)}\n")

                    if assignments:
                        # Date range
                        dates = [
                            a["assignment_date"]
                            for a in assignments
                            if a["assignment_date"]
                        ]
                        if dates:
                            f.write(f"- **Date Range:** {min(dates)} to {max(dates)}\n")

                        # Routes
                        routes = {
                            a["route_number"] for a in assignments if a["route_number"]
                        }
                        f.write(f"- **Routes:** {len(routes)} unique routes\n")

                        # Drivers
                        drivers = {
                            a["driver_name"] for a in assignments if a["driver_name"]
                        }
                        f.write(f"- **Drivers:** {len(drivers)} unique drivers\n")

                        # Vehicles
                        vehicles = {
                            a["vehicle_number"]
                            for a in assignments
                            if a["vehicle_number"]
                        }
                        f.write(f"- **Vehicles:** {len(vehicles)} unique vehicles\n")

                if "routes" in extraction_data:
                    f.write("\n## Routes Data\n\n")
                    f.write(f"- **Total Records:** {len(extraction_data['routes'])}\n")

                if "personnel" in extraction_data:
                    f.write("\n## Personnel Data\n\n")
                    f.write(
                        f"- **Total Records:** {len(extraction_data['personnel'])}\n"
                    )

                if "vehicles" in extraction_data:
                    f.write("\n## Vehicles Data\n\n")
                    f.write(
                        f"- **Total Records:** {len(extraction_data['vehicles'])}\n"
                    )

                f.write("\n## Field Mapping\n\n")
                f.write(
                    "The following fields were extracted from the zanaradka table:\n\n"
                )

                if "assignments" in extraction_data and extraction_data["assignments"]:
                    sample_assignment = extraction_data["assignments"][0]
                    for field_name in sorted(sample_assignment.keys()):
                        f.write(f"- `{field_name}`\n")

            logger.info(f"✅ Extraction report generated: {report_file}")
            return str(report_file)

        except Exception as e:
            logger.error(f"❌ Failed to generate extraction report: {e}")
            return None

    def close_connection(self):
        """Close database connection"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            logger.info("Database connection closed")
        except Error as e:
            logger.error(f"Error closing database connection: {e}")

    def run_full_extraction(self, limit: int | None = 1000):
        """Run complete data extraction process"""
        try:
            logger.info("🚀 Starting full MySQL data extraction...")

            # Connect to database
            if not self.connect_to_database():
                return False

            # Test connection
            connection_test = self.test_connection()
            if connection_test["status"] != "success":
                logger.error("Connection test failed")
                return False

            # Analyze table structure
            table_analysis = self.analyze_zanaradka_table()

            # Extract assignments data
            assignments_data = self.extract_assignments_data(limit=limit)

            # Extract reference data
            reference_data = self.extract_reference_data()

            # Combine all data
            extraction_results = {
                "extraction_metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "database_config": {
                        "host": DB_CONFIG["host"],
                        "database": DB_CONFIG["database"],
                    },
                    "extraction_parameters": {"limit": limit},
                },
                "connection_test": connection_test,
                "table_analysis": table_analysis,
                "assignments": assignments_data.get("assignments", []),
                "reference_data": reference_data,
            }

            # Save results
            results_file = self.save_extraction_results(extraction_results)

            # Generate report
            report_file = self.generate_extraction_report(extraction_results)

            logger.info("🎉 Full extraction completed successfully!")
            logger.info(f"📄 Results saved to: {results_file}")
            logger.info(f"📊 Report generated: {report_file}")

            return True

        except Exception as e:
            logger.error(f"❌ Full extraction failed: {e}")
            return False
        finally:
            self.close_connection()


def main():
    """Main execution function"""
    extractor = MySQLDataExtractor()

    # Get command line arguments for flexibility
    import argparse

    parser = argparse.ArgumentParser(description="Extract data from MySQL database")
    parser.add_argument(
        "--limit", type=int, default=1000, help="Limit number of records to extract"
    )
    parser.add_argument(
        "--start-date", type=str, help="Start date for extraction (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--end-date", type=str, help="End date for extraction (YYYY-MM-DD)"
    )

    args = parser.parse_args()

    # Run extraction
    success = extractor.run_full_extraction(limit=args.limit)

    if success:
        print("✅ Data extraction completed successfully!")
        print("📁 Check the 'extracted_mysql_data' directory for results")
    else:
        print("❌ Data extraction failed!")
        print("📋 Check the 'mysql_extraction.log' file for details")


if __name__ == "__main__":
    main()
