#!/usr/bin/env python3
"""
Local Server Data Extraction Script
To be run directly on the Windows server
"""

import glob
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path


class LocalServerExtractor:
    def __init__(self):
        self.output_dir = Path("extraction_results")
        self.output_dir.mkdir(exist_ok=True)

    def find_access_files(self) -> list:
        """Find MS Access files on local system"""
        access_files = []
        search_patterns = ["*.mdb", "*.accdb", "*.mde", "*.accde"]

        # Common locations to search
        search_locations = [
            "C:\\",
            "D:\\",
            "C:\\Program Files\\",
            "C:\\Program Files (x86)\\",
            "C:\\Users\\",
            "C:\\Data\\",
            "C:\\Transport\\",
            "C:\\Depot\\",
            "C:\\Database\\",
            ".",
        ]

        print("🔍 Searching for MS Access files...")

        for location in search_locations:
            if os.path.exists(location):
                for pattern in search_patterns:
                    try:
                        files = glob.glob(
                            os.path.join(location, "**", pattern), recursive=True
                        )
                        for file in files:
                            if os.path.getsize(file) > 1000:  # Skip very small files
                                access_files.append(
                                    {
                                        "path": file,
                                        "size": os.path.getsize(file),
                                        "modified": datetime.fromtimestamp(
                                            os.path.getmtime(file)
                                        ).isoformat(),
                                    }
                                )
                                print(f"  📁 Found: {file}")
                    except Exception as e:
                        print(f"  ⚠️  Error searching {location}: {e}")

        return access_files

    def test_mysql_local(self) -> dict:
        """Test MySQL connection from local machine"""
        mysql_info = {
            "connection_status": "failed",
            "databases": [],
            "tables": [],
            "error": None,
        }

        # Try different MySQL command variations
        mysql_commands = [
            "mysql -u khtrm_remote -p'KhTRM_2025!' -e 'SHOW DATABASES;'",
            "mysql -h localhost -u khtrm_remote -p'KhTRM_2025!' -e 'SHOW DATABASES;'",
            "mysql -h 127.0.0.1 -u khtrm_remote -p'KhTRM_2025!' -e 'SHOW DATABASES;'",
        ]

        for cmd in mysql_commands:
            try:
                print(f"🔍 Testing: {cmd}")
                result = subprocess.run(
                    cmd, shell=True, capture_output=True, text=True, timeout=30
                )

                if result.returncode == 0:
                    mysql_info["connection_status"] = "success"
                    mysql_info["command_used"] = cmd
                    mysql_info["output"] = result.stdout

                    # Get specific database info
                    db_cmd = cmd.replace(
                        "SHOW DATABASES;", "USE saltdepoavt_; SHOW TABLES;"
                    )
                    db_result = subprocess.run(
                        db_cmd, shell=True, capture_output=True, text=True, timeout=30
                    )

                    if db_result.returncode == 0:
                        mysql_info["saltdepoavt_tables"] = db_result.stdout
                        print("✅ MySQL connection successful!")
                        return mysql_info

                else:
                    print(f"  ❌ Failed: {result.stderr}")

            except Exception as e:
                print(f"  ❌ Error: {e}")

        mysql_info["error"] = "All MySQL connection attempts failed"
        return mysql_info

    def extract_system_info(self) -> dict:
        """Extract system information"""
        system_info = {}

        try:
            # Basic system info
            system_info["hostname"] = subprocess.run(
                "hostname", capture_output=True, text=True
            ).stdout.strip()
            system_info["os_version"] = subprocess.run(
                "ver", shell=True, capture_output=True, text=True
            ).stdout.strip()
            system_info["current_user"] = subprocess.run(
                "whoami", capture_output=True, text=True
            ).stdout.strip()
            system_info["current_dir"] = os.getcwd()

            # Disk info
            disk_info = subprocess.run(
                "wmic logicaldisk get size,freespace,caption",
                capture_output=True,
                text=True,
            )
            system_info["disk_info"] = disk_info.stdout

            # Running processes (filter for database/access related)
            processes = subprocess.run("tasklist", capture_output=True, text=True)
            system_info["processes"] = processes.stdout

            # Network info
            network = subprocess.run("ipconfig /all", capture_output=True, text=True)
            system_info["network"] = network.stdout

            print("✅ System information extracted")

        except Exception as e:
            system_info["error"] = str(e)
            print(f"❌ Error extracting system info: {e}")

        return system_info

    def search_database_files(self) -> dict:
        """Search for database-related files"""
        db_files = {
            "sql_files": [],
            "backup_files": [],
            "config_files": [],
            "log_files": [],
        }

        # File patterns to search for
        patterns = {
            "sql_files": ["*.sql", "*.bak"],
            "backup_files": ["*.bak", "*.backup"],
            "config_files": ["*.ini", "*.cfg", "*.conf"],
            "log_files": ["*.log", "*.txt"],
        }

        search_locations = [
            "C:\\",
            "D:\\",
            "C:\\Program Files\\MySQL\\",
            "C:\\ProgramData\\MySQL\\",
            "C:\\Users\\",
            ".",
        ]

        print("🔍 Searching for database files...")

        for location in search_locations:
            if os.path.exists(location):
                for category, file_patterns in patterns.items():
                    for pattern in file_patterns:
                        try:
                            files = glob.glob(
                                os.path.join(location, "**", pattern), recursive=True
                            )
                            for file in files[:10]:  # Limit to first 10 matches
                                if os.path.getsize(file) > 100:  # Skip very small files
                                    db_files[category].append(
                                        {
                                            "path": file,
                                            "size": os.path.getsize(file),
                                            "modified": datetime.fromtimestamp(
                                                os.path.getmtime(file)
                                            ).isoformat(),
                                        }
                                    )
                        except Exception:
                            pass  # Skip errors

        return db_files

    def create_data_summary(self) -> dict:
        """Create summary of found data"""
        summary = {
            "extraction_date": datetime.now().isoformat(),
            "total_access_files": 0,
            "total_database_files": 0,
            "mysql_available": False,
            "recommendations": [],
        }

        # This will be populated by the main extraction process
        return summary

    def save_results(self, data: dict):
        """Save extraction results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save JSON
        json_file = self.output_dir / f"local_extraction_{timestamp}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)

        # Save readable report
        report_file = self.output_dir / f"local_extraction_report_{timestamp}.md"
        with open(report_file, "w", encoding="utf-8") as f:
            f.write("# Local Server Data Extraction Report\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Server:** {data['system_info'].get('hostname', 'Unknown')}\n\n")

            # System Info
            f.write("## 🖥️ System Information\n\n")
            if "system_info" in data:
                sys_info = data["system_info"]
                f.write(f"- **Hostname:** {sys_info.get('hostname', 'Unknown')}\n")
                f.write(f"- **OS Version:** {sys_info.get('os_version', 'Unknown')}\n")
                f.write(
                    f"- **Current User:** {sys_info.get('current_user', 'Unknown')}\n"
                )
                f.write(
                    f"- **Current Directory:** {sys_info.get('current_dir', 'Unknown')}\n\n"
                )

            # Access Files
            f.write("## 📁 MS Access Files Found\n\n")
            if "access_files" in data:
                for file_info in data["access_files"]:
                    f.write(f"- **{file_info['path']}**\n")
                    f.write(f"  - Size: {file_info['size']} bytes\n")
                    f.write(f"  - Modified: {file_info['modified']}\n\n")

            # MySQL Info
            f.write("## 🗄️ MySQL Connection Test\n\n")
            if "mysql_info" in data:
                mysql_info = data["mysql_info"]
                status = "✅" if mysql_info["connection_status"] == "success" else "❌"
                f.write(f"{status} **Status:** {mysql_info['connection_status']}\n")
                if mysql_info.get("command_used"):
                    f.write(f"- **Command Used:** {mysql_info['command_used']}\n")
                if mysql_info.get("saltdepoavt_tables"):
                    f.write("- **Tables in saltdepoavt_:**\n")
                    f.write(f"```\n{mysql_info['saltdepoavt_tables']}\n```\n")
                f.write("\n")

        print("💾 Results saved to:")
        print(f"  📄 JSON: {json_file}")
        print(f"  📄 Report: {report_file}")

        # Create a simple batch file for easy running
        batch_file = self.output_dir / "run_extraction.bat"
        with open(batch_file, "w") as f:
            f.write("@echo off\n")
            f.write("echo Starting Local Server Data Extraction...\n")
            f.write("python local_server_extraction.py\n")
            f.write("echo.\n")
            f.write(
                "echo Extraction completed. Check extraction_results folder for results.\n"
            )
            f.write("pause\n")

        print(f"  📄 Batch file: {batch_file}")

    def run_extraction(self):
        """Run the full extraction process"""
        print("🚀 Starting Local Server Data Extraction...")
        print("📍 Running on local machine")

        results = {
            "extraction_info": {
                "date": datetime.now().isoformat(),
                "script_version": "1.0",
                "location": "local_server",
            }
        }

        # Extract system information
        print("\n1️⃣ Extracting system information...")
        results["system_info"] = self.extract_system_info()

        # Find Access files
        print("\n2️⃣ Searching for MS Access files...")
        results["access_files"] = self.find_access_files()

        # Test MySQL
        print("\n3️⃣ Testing MySQL connection...")
        results["mysql_info"] = self.test_mysql_local()

        # Search for database files
        print("\n4️⃣ Searching for database files...")
        results["database_files"] = self.search_database_files()

        # Create summary
        print("\n5️⃣ Creating summary...")
        results["summary"] = self.create_data_summary()
        results["summary"]["total_access_files"] = len(results["access_files"])
        results["summary"]["mysql_available"] = (
            results["mysql_info"]["connection_status"] == "success"
        )

        # Save results
        print("\n💾 Saving results...")
        self.save_results(results)

        print("\n✅ Local extraction completed!")
        print(f"📂 Results saved in: {self.output_dir}")

        # Display summary
        print("\n📊 Summary:")
        print(f"  - Access files found: {len(results['access_files'])}")
        print(
            f"  - MySQL connection: {'✅' if results['mysql_info']['connection_status'] == 'success' else '❌'}"
        )
        print(f"  - System info: {'✅' if 'system_info' in results else '❌'}")


if __name__ == "__main__":
    print("=" * 60)
    print("MS Access Data Extraction Tool")
    print("For Windows Server (Local Execution)")
    print("=" * 60)

    extractor = LocalServerExtractor()
    extractor.run_extraction()

    print("\n" + "=" * 60)
    print("Instructions:")
    print("1. Copy the 'extraction_results' folder")
    print("2. Send the JSON and MD files to the development team")
    print("3. The data will be used to create the new web interface")
    print("=" * 60)
