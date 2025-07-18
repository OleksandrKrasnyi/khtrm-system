#!/usr/bin/env python3
"""
Windows Server Data Extraction Tool
Extracts data from Windows server without SSH using direct connections
"""

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

import pymysql

# Server configuration
REMOTE_HOST = "91.222.248.216"
REMOTE_PORT = 61317
REMOTE_USER = "user101"
REMOTE_PASSWORD = os.getenv("REMOTE_PASSWORD", "your_remote_password_here")

# MySQL configuration
MYSQL_HOST = "91.222.248.216"
MYSQL_PORT = 61317  # Using the same port that's open
MYSQL_USER = "khtrm_remote"
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "your_mysql_password_here")
MYSQL_DATABASE = "saltdepoavt_"


class WindowsDataExtractor:
    def __init__(self):
        self.output_dir = Path("extracted_data")
        self.output_dir.mkdir(exist_ok=True)

    def test_mysql_connection(self) -> bool:
        """Test direct MySQL connection"""
        try:
            print(f"🔍 Testing MySQL connection to {MYSQL_HOST}:{MYSQL_PORT}...")

            connection = pymysql.connect(
                host=MYSQL_HOST,
                port=MYSQL_PORT,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DATABASE,
                charset="utf8mb4",
                connect_timeout=30,
            )

            with connection.cursor() as cursor:
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()
                print(f"✅ MySQL connection successful! Version: {version[0]}")

            connection.close()
            return True

        except Exception as e:
            print(f"❌ MySQL connection failed: {e}")
            return False

    def extract_mysql_data(self) -> dict[str, Any]:
        """Extract data from MySQL database"""
        mysql_data = {
            "connection_status": "failed",
            "database_info": {},
            "tables": [],
            "dispatcher_tables": {},
            "sample_data": {},
        }

        try:
            connection = pymysql.connect(
                host=MYSQL_HOST,
                port=MYSQL_PORT,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DATABASE,
                charset="utf8mb4",
                connect_timeout=30,
            )

            mysql_data["connection_status"] = "success"

            with connection.cursor() as cursor:
                # Get database version and info
                cursor.execute("SELECT VERSION(), DATABASE(), USER()")
                version_info = cursor.fetchone()
                mysql_data["database_info"] = {
                    "version": version_info[0],
                    "database": version_info[1],
                    "user": version_info[2],
                }

                # Get all tables
                cursor.execute("SHOW TABLES")
                tables = [row[0] for row in cursor.fetchall()]
                mysql_data["tables"] = tables

                print(f"📊 Found {len(tables)} tables in database")

                # Get dispatcher-specific tables
                dispatcher_keywords = [
                    "zanar",
                    "marshr",
                    "personal",
                    "sprpe",
                    "grafik",
                    "smena",
                    "route",
                ]
                dispatcher_tables = {}

                for table in tables:
                    if any(keyword in table.lower() for keyword in dispatcher_keywords):
                        try:
                            # Get table structure
                            cursor.execute(f"DESCRIBE `{table}`")
                            columns = cursor.fetchall()

                            # Get row count
                            cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
                            row_count = cursor.fetchone()[0]

                            # Get sample data (first 3 rows)
                            cursor.execute(f"SELECT * FROM `{table}` LIMIT 3")
                            sample_rows = cursor.fetchall()

                            dispatcher_tables[table] = {
                                "columns": [
                                    {
                                        "name": col[0],
                                        "type": col[1],
                                        "null": col[2],
                                        "key": col[3],
                                        "default": col[4],
                                    }
                                    for col in columns
                                ],
                                "row_count": row_count,
                                "sample_data": sample_rows,
                            }

                            print(
                                f"  📋 {table}: {row_count} rows, {len(columns)} columns"
                            )

                        except Exception as e:
                            print(f"⚠️  Error processing table {table}: {e}")

                mysql_data["dispatcher_tables"] = dispatcher_tables

                # Get specific data for main tables
                main_tables = ["zanaradka", "sprmarshrut", "sprpersonal", "sprpe"]
                sample_data = {}

                for table in main_tables:
                    if table in tables:
                        try:
                            cursor.execute(f"SELECT * FROM `{table}` LIMIT 5")
                            rows = cursor.fetchall()

                            cursor.execute(f"DESCRIBE `{table}`")
                            columns = [col[0] for col in cursor.fetchall()]

                            sample_data[table] = {
                                "columns": columns,
                                "sample_rows": rows,
                            }

                        except Exception as e:
                            print(f"⚠️  Error getting sample data for {table}: {e}")

                mysql_data["sample_data"] = sample_data

            connection.close()

        except Exception as e:
            print(f"❌ Error extracting MySQL data: {e}")
            mysql_data["error"] = str(e)

        return mysql_data

    def test_smb_connection(self) -> dict[str, Any]:
        """Test SMB/CIFS connection to access files"""
        smb_data = {
            "connection_status": "failed",
            "accessible_shares": [],
            "error": None,
        }

        try:
            # Try to list shares using net view
            result = subprocess.run(
                ["net", "view", f"\\\\{REMOTE_HOST}"],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                smb_data["connection_status"] = "success"
                smb_data["shares_output"] = result.stdout
                print("✅ SMB connection successful")
            else:
                smb_data["error"] = result.stderr
                print(f"❌ SMB connection failed: {result.stderr}")

        except Exception as e:
            smb_data["error"] = str(e)
            print(f"❌ SMB test error: {e}")

        return smb_data

    def test_winrm_connection(self) -> dict[str, Any]:
        """Test WinRM connection"""
        winrm_data = {"connection_status": "failed", "test_results": [], "error": None}

        try:
            # Test WinRM availability
            result = subprocess.run(
                [
                    "winrs",
                    "-r",
                    f"{REMOTE_HOST}:{REMOTE_PORT}",
                    "-u",
                    REMOTE_USER,
                    "-p",
                    REMOTE_PASSWORD,
                    "echo",
                    "test",
                ],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                winrm_data["connection_status"] = "success"
                winrm_data["test_output"] = result.stdout
                print("✅ WinRM connection successful")
            else:
                winrm_data["error"] = result.stderr
                print(f"❌ WinRM connection failed: {result.stderr}")

        except Exception as e:
            winrm_data["error"] = str(e)
            print(f"❌ WinRM test error: {e}")

        return winrm_data

    def generate_dispatcher_analysis(
        self, mysql_data: dict[str, Any]
    ) -> dict[str, Any]:
        """Generate analysis specific to dispatcher functionality"""
        analysis = {
            "assignment_structure": {},
            "route_structure": {},
            "employee_structure": {},
            "vehicle_structure": {},
            "recommendations": [],
        }

        if mysql_data["connection_status"] == "success":
            dispatcher_tables = mysql_data.get("dispatcher_tables", {})

            # Analyze assignment table (zanaradka)
            if "zanaradka" in dispatcher_tables:
                table_info = dispatcher_tables["zanaradka"]
                analysis["assignment_structure"] = {
                    "table_name": "zanaradka",
                    "total_records": table_info["row_count"],
                    "key_fields": [
                        col["name"] for col in table_info["columns"] if col["key"]
                    ],
                    "all_fields": [col["name"] for col in table_info["columns"]],
                    "sample_data": table_info["sample_data"][:2],  # First 2 rows
                }

                analysis["recommendations"].append(
                    "Основная таблица нарядов найдена - zanaradka с "
                    + f"{table_info['row_count']} записями"
                )

            # Analyze route table (sprmarshrut)
            if "sprmarshrut" in dispatcher_tables:
                table_info = dispatcher_tables["sprmarshrut"]
                analysis["route_structure"] = {
                    "table_name": "sprmarshrut",
                    "total_records": table_info["row_count"],
                    "key_fields": [
                        col["name"] for col in table_info["columns"] if col["key"]
                    ],
                    "all_fields": [col["name"] for col in table_info["columns"]],
                }

                analysis["recommendations"].append(
                    "Справочник маршрутов найден - sprmarshrut с "
                    + f"{table_info['row_count']} записями"
                )

            # Analyze employee table (sprpersonal)
            if "sprpersonal" in dispatcher_tables:
                table_info = dispatcher_tables["sprpersonal"]
                analysis["employee_structure"] = {
                    "table_name": "sprpersonal",
                    "total_records": table_info["row_count"],
                    "key_fields": [
                        col["name"] for col in table_info["columns"] if col["key"]
                    ],
                    "all_fields": [col["name"] for col in table_info["columns"]],
                }

                analysis["recommendations"].append(
                    "Справочник персонала найден - sprpersonal с "
                    + f"{table_info['row_count']} записями"
                )

            # Analyze vehicle table (sprpe)
            if "sprpe" in dispatcher_tables:
                table_info = dispatcher_tables["sprpe"]
                analysis["vehicle_structure"] = {
                    "table_name": "sprpe",
                    "total_records": table_info["row_count"],
                    "key_fields": [
                        col["name"] for col in table_info["columns"] if col["key"]
                    ],
                    "all_fields": [col["name"] for col in table_info["columns"]],
                }

                analysis["recommendations"].append(
                    "Справочник транспорта найден - sprpe с "
                    + f"{table_info['row_count']} записями"
                )

        return analysis

    def save_extraction_results(self, data: dict[str, Any]):
        """Save all extracted data to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save as JSON
        json_file = self.output_dir / f"windows_extraction_{timestamp}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)

        # Save as readable report
        report_file = self.output_dir / f"windows_extraction_report_{timestamp}.md"
        self.generate_markdown_report(data, report_file)

        print("💾 Results saved to:")
        print(f"  📄 JSON: {json_file}")
        print(f"  📄 Report: {report_file}")

    def generate_markdown_report(self, data: dict[str, Any], output_file: Path):
        """Generate human-readable markdown report"""
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("# Windows Server Data Extraction Report\n\n")
            f.write(
                f"**Extraction Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            )
            f.write(f"**Server:** {REMOTE_HOST}\n\n")

            # MySQL Results
            if "mysql_data" in data:
                mysql_data = data["mysql_data"]
                f.write("## 🗄️ MySQL Database Analysis\n\n")

                if mysql_data["connection_status"] == "success":
                    f.write("✅ **Connection Status:** Success\n")
                    f.write(
                        f"**Database:** {mysql_data['database_info']['database']}\n"
                    )
                    f.write(f"**Version:** {mysql_data['database_info']['version']}\n")
                    f.write(f"**Total Tables:** {len(mysql_data['tables'])}\n\n")

                    # Dispatcher Tables
                    if mysql_data["dispatcher_tables"]:
                        f.write("### 🎯 Dispatcher-Related Tables\n\n")
                        for table_name, table_info in mysql_data[
                            "dispatcher_tables"
                        ].items():
                            f.write(f"#### {table_name}\n")
                            f.write(f"- **Records:** {table_info['row_count']}\n")
                            f.write(f"- **Columns:** {len(table_info['columns'])}\n")
                            f.write("- **Key Fields:** ")
                            key_fields = [
                                col["name"]
                                for col in table_info["columns"]
                                if col["key"]
                            ]
                            f.write(", ".join(key_fields) if key_fields else "None")
                            f.write("\n\n")
                else:
                    f.write("❌ **Connection Status:** Failed\n")
                    f.write(
                        f"**Error:** {mysql_data.get('error', 'Unknown error')}\n\n"
                    )

            # Dispatcher Analysis
            if "dispatcher_analysis" in data:
                analysis = data["dispatcher_analysis"]
                f.write("## 📊 Dispatcher Functionality Analysis\n\n")

                if analysis["assignment_structure"]:
                    f.write("### 📋 Assignment Structure (Наряды)\n")
                    assign_struct = analysis["assignment_structure"]
                    f.write(f"- **Table:** {assign_struct['table_name']}\n")
                    f.write(f"- **Total Records:** {assign_struct['total_records']}\n")
                    f.write(
                        f"- **Key Fields:** {', '.join(assign_struct['key_fields'])}\n"
                    )
                    f.write(
                        f"- **All Fields:** {', '.join(assign_struct['all_fields'])}\n\n"
                    )

                if analysis["recommendations"]:
                    f.write("### 💡 Recommendations\n")
                    for rec in analysis["recommendations"]:
                        f.write(f"- {rec}\n")
                    f.write("\n")

            # Connection Tests
            if "connection_tests" in data:
                f.write("## 🔗 Connection Tests\n\n")
                tests = data["connection_tests"]

                for test_name, test_result in tests.items():
                    status = (
                        "✅" if test_result["connection_status"] == "success" else "❌"
                    )
                    f.write(f"### {status} {test_name}\n")
                    f.write(f"**Status:** {test_result['connection_status']}\n")
                    if test_result.get("error"):
                        f.write(f"**Error:** {test_result['error']}\n")
                    f.write("\n")

    def run_extraction(self):
        """Main extraction process"""
        print("🚀 Starting Windows Server Data Extraction...")
        print(f"📡 Target server: {REMOTE_HOST}")

        extraction_data = {
            "extraction_info": {
                "date": datetime.now().isoformat(),
                "server": REMOTE_HOST,
                "extraction_type": "windows_direct",
            }
        }

        # Test connections
        print("\n🔗 Testing connections...")
        connection_tests = {}

        # Test MySQL
        print("\n1️⃣ Testing MySQL connection...")
        mysql_available = self.test_mysql_connection()

        if mysql_available:
            print("\n📊 Extracting MySQL data...")
            mysql_data = self.extract_mysql_data()
            extraction_data["mysql_data"] = mysql_data

            # Generate dispatcher analysis
            print("\n🎯 Analyzing dispatcher functionality...")
            dispatcher_analysis = self.generate_dispatcher_analysis(mysql_data)
            extraction_data["dispatcher_analysis"] = dispatcher_analysis

        # Test SMB
        print("\n2️⃣ Testing SMB connection...")
        smb_result = self.test_smb_connection()
        connection_tests["SMB"] = smb_result

        # Test WinRM
        print("\n3️⃣ Testing WinRM connection...")
        winrm_result = self.test_winrm_connection()
        connection_tests["WinRM"] = winrm_result

        extraction_data["connection_tests"] = connection_tests

        # Save results
        print("\n💾 Saving extraction results...")
        self.save_extraction_results(extraction_data)

        print("\n✅ Windows extraction completed successfully!")
        print(f"📂 Results saved in: {self.output_dir}")


if __name__ == "__main__":
    extractor = WindowsDataExtractor()
    extractor.run_extraction()
