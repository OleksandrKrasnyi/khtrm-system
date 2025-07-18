#!/usr/bin/env python3
"""
MS Access Data Extraction Tool
Extracts SQL queries, VBA code, form structures from MS Access databases on remote server
"""

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

import paramiko

# Server configuration
REMOTE_HOST = "91.222.248.216"
REMOTE_PORT = 61317
REMOTE_USER = "user101"
REMOTE_PASSWORD = os.getenv("REMOTE_PASSWORD", "your_remote_password_here")


class AccessDataExtractor:
    def __init__(self):
        self.ssh_client = None
        self.sftp_client = None
        self.output_dir = Path("extracted_access_data")
        self.output_dir.mkdir(exist_ok=True)

    def connect_to_server(self) -> bool:
        """Connect to remote server via SSH"""
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            print(f"Connecting to {REMOTE_HOST}:{REMOTE_PORT}...")
            self.ssh_client.connect(
                hostname=REMOTE_HOST,
                port=REMOTE_PORT,
                username=REMOTE_USER,
                password=REMOTE_PASSWORD,
                timeout=30,
            )

            self.sftp_client = self.ssh_client.open_sftp()
            print("✅ Successfully connected to remote server")
            return True

        except Exception as e:
            print(f"❌ Failed to connect to server: {e}")
            return False

    def find_access_files(self, search_paths: list[str] = None) -> list[str]:
        """Find MS Access database files on remote server"""
        if search_paths is None:
            search_paths = ["/c/", "/d/", "/home/", "/opt/", "/var/", "."]

        access_files = []
        extensions = [".mdb", ".accdb", ".mde", ".accde"]

        for search_path in search_paths:
            try:
                print(f"🔍 Searching for Access files in {search_path}...")

                # Search for Access files
                find_command = f"find {search_path} -type f \\( "
                find_command += " -o ".join(
                    [f'-name "*.{ext[1:]}"' for ext in extensions]
                )
                find_command += " \\) 2>/dev/null | head -20"

                stdin, stdout, stderr = self.ssh_client.exec_command(find_command)
                files = stdout.read().decode().strip().split("\n")

                for file_path in files:
                    if file_path and any(
                        file_path.lower().endswith(ext) for ext in extensions
                    ):
                        access_files.append(file_path)
                        print(f"  📁 Found: {file_path}")

            except Exception as e:
                print(f"⚠️  Error searching {search_path}: {e}")
                continue

        return access_files

    def download_access_file(self, remote_path: str) -> str | None:
        """Download Access file from remote server"""
        try:
            filename = Path(remote_path).name
            local_path = self.output_dir / "databases" / filename
            local_path.parent.mkdir(exist_ok=True)

            print(f"⬇️  Downloading {remote_path}...")
            self.sftp_client.get(remote_path, str(local_path))

            # Check file size
            file_size = os.path.getsize(local_path)
            print(f"✅ Downloaded {filename} ({file_size} bytes)")

            return str(local_path)

        except Exception as e:
            print(f"❌ Failed to download {remote_path}: {e}")
            return None

    def extract_access_metadata(self, access_file_path: str) -> dict[str, Any]:
        """Extract metadata from Access database using mdb-tools or similar"""
        metadata = {
            "file_path": access_file_path,
            "file_size": os.path.getsize(access_file_path),
            "extraction_date": datetime.now().isoformat(),
            "tables": [],
            "queries": [],
            "forms": [],
            "reports": [],
            "modules": [],
        }

        try:
            # Try to extract table structure using mdb-tools (if available)
            result = subprocess.run(
                ["mdb-tables", "-1", access_file_path],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                tables = [t.strip() for t in result.stdout.split("\n") if t.strip()]
                metadata["tables"] = tables
                print(f"📊 Found {len(tables)} tables")

                # Extract table schemas
                for table in tables[:10]:  # Limit to first 10 tables
                    try:
                        schema_result = subprocess.run(
                            ["mdb-schema", access_file_path, "-T", table],
                            capture_output=True,
                            text=True,
                            timeout=10,
                        )
                        if schema_result.returncode == 0:
                            schema_file = self.output_dir / "schemas" / f"{table}.sql"
                            schema_file.parent.mkdir(exist_ok=True)
                            schema_file.write_text(schema_result.stdout)
                    except Exception as e:
                        print(f"⚠️  Failed to extract schema for {table}: {e}")

        except FileNotFoundError:
            print(
                "⚠️  mdb-tools not found. Install with: sudo apt-get install mdb-tools"
            )
        except Exception as e:
            print(f"⚠️  Error extracting metadata: {e}")

        return metadata

    def search_for_queries_and_code(self, remote_paths: list[str]) -> dict[str, Any]:
        """Search for SQL queries and VBA code in text files on remote server"""
        code_data = {
            "sql_queries": [],
            "vba_code": [],
            "config_files": [],
            "log_files": [],
        }

        # Common file extensions that might contain SQL or VBA
        search_extensions = [
            ".sql",
            ".vba",
            ".bas",
            ".cls",
            ".frm",
            ".txt",
            ".log",
            ".cfg",
            ".ini",
        ]

        for remote_path in remote_paths:
            try:
                print(f"🔍 Searching for code files in {remote_path}...")

                for ext in search_extensions:
                    find_command = f'find {remote_path} -name "*{ext}" -type f 2>/dev/null | head -10'
                    stdin, stdout, stderr = self.ssh_client.exec_command(find_command)
                    files = stdout.read().decode().strip().split("\n")

                    for file_path in files:
                        if file_path and file_path.endswith(ext):
                            try:
                                # Read file content
                                cat_command = (
                                    f'cat "{file_path}" 2>/dev/null | head -100'
                                )
                                stdin, stdout, stderr = self.ssh_client.exec_command(
                                    cat_command
                                )
                                content = stdout.read().decode(errors="ignore")

                                if content.strip():
                                    file_info = {
                                        "file_path": file_path,
                                        "extension": ext,
                                        "content_preview": content[
                                            :1000
                                        ],  # First 1000 chars
                                        "size_estimate": len(content),
                                    }

                                    if ext in [".sql"]:
                                        code_data["sql_queries"].append(file_info)
                                    elif ext in [".vba", ".bas", ".cls", ".frm"]:
                                        code_data["vba_code"].append(file_info)
                                    elif ext in [".cfg", ".ini"]:
                                        code_data["config_files"].append(file_info)
                                    else:
                                        code_data["log_files"].append(file_info)

                            except Exception as e:
                                print(f"⚠️  Error reading {file_path}: {e}")

            except Exception as e:
                print(f"⚠️  Error searching {remote_path}: {e}")

        return code_data

    def generate_database_info(self) -> dict[str, Any]:
        """Generate information about available databases and tables"""
        db_info = {"mysql_databases": [], "table_structures": {}, "sample_queries": []}

        try:
            # Try to connect to MySQL and get database info
            mysql_command = "mysql -h localhost -u khtrm_remote -p'KhTRM_2025!' -e 'SHOW DATABASES;' 2>/dev/null"
            stdin, stdout, stderr = self.ssh_client.exec_command(mysql_command)
            output = stdout.read().decode()

            if "saltdepoavt_" in output:
                print("✅ Found MySQL database: saltdepoavt_")

                # Get table list
                tables_command = "mysql -h localhost -u khtrm_remote -p'KhTRM_2025!' saltdepoavt_ -e 'SHOW TABLES;' 2>/dev/null"
                stdin, stdout, stderr = self.ssh_client.exec_command(tables_command)
                tables_output = stdout.read().decode()

                # Extract table names
                tables = []
                for line in tables_output.split("\n")[1:]:  # Skip header
                    if line.strip():
                        tables.append(line.strip())

                db_info["mysql_databases"] = ["saltdepoavt_"]
                db_info["available_tables"] = tables[:20]  # First 20 tables

                print(f"📊 Found {len(tables)} tables in MySQL database")

        except Exception as e:
            print(f"⚠️  Error getting MySQL info: {e}")

        return db_info

    def save_extraction_results(self, data: dict[str, Any]):
        """Save all extracted data to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save as JSON
        json_file = self.output_dir / f"extraction_results_{timestamp}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # Save as readable report
        report_file = self.output_dir / f"extraction_report_{timestamp}.md"
        self.generate_markdown_report(data, report_file)

        print("💾 Results saved to:")
        print(f"  📄 JSON: {json_file}")
        print(f"  📄 Report: {report_file}")

    def generate_markdown_report(self, data: dict[str, Any], output_file: Path):
        """Generate human-readable markdown report"""
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("# MS Access Data Extraction Report\n\n")
            f.write(
                f"**Extraction Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            )

            # Access Files Found
            if "access_files" in data:
                f.write("## 🗃️ MS Access Files Found\n\n")
                for file_info in data["access_files"]:
                    f.write(
                        f"- **{file_info['file_path']}** ({file_info['file_size']} bytes)\n"
                    )
                    if "tables" in file_info:
                        f.write(f"  - Tables: {len(file_info['tables'])}\n")
                f.write("\n")

            # Database Info
            if "database_info" in data:
                f.write("## 🗄️ Database Information\n\n")
                db_info = data["database_info"]
                if db_info.get("mysql_databases"):
                    f.write("### MySQL Databases:\n")
                    for db in db_info["mysql_databases"]:
                        f.write(f"- {db}\n")

                if db_info.get("available_tables"):
                    f.write("### Available Tables:\n")
                    for table in db_info["available_tables"][:10]:
                        f.write(f"- {table}\n")
                f.write("\n")

            # Code Files
            if "code_data" in data:
                code_data = data["code_data"]
                f.write("## 💻 Code Files Found\n\n")

                if code_data.get("sql_queries"):
                    f.write("### SQL Queries:\n")
                    for sql_file in code_data["sql_queries"][:5]:
                        f.write(f"- **{sql_file['file_path']}**\n")
                        f.write(
                            f"  ```sql\n{sql_file['content_preview'][:200]}...\n  ```\n"
                        )

                if code_data.get("vba_code"):
                    f.write("### VBA Code:\n")
                    for vba_file in code_data["vba_code"][:5]:
                        f.write(f"- **{vba_file['file_path']}**\n")
                        f.write(
                            f"  ```vba\n{vba_file['content_preview'][:200]}...\n  ```\n"
                        )

    def run_extraction(self):
        """Main extraction process"""
        print("🚀 Starting MS Access Data Extraction...")

        if not self.connect_to_server():
            return

        try:
            extraction_data = {
                "extraction_info": {
                    "date": datetime.now().isoformat(),
                    "server": f"{REMOTE_HOST}:{REMOTE_PORT}",
                    "user": REMOTE_USER,
                }
            }

            # 1. Find Access files
            print("\n📁 Step 1: Finding MS Access files...")
            access_files = self.find_access_files(["/c/", "/d/", "/opt/", "."])

            # 2. Download and analyze Access files
            print("\n📥 Step 2: Downloading and analyzing Access files...")
            access_file_data = []
            for file_path in access_files[:3]:  # Limit to first 3 files
                local_path = self.download_access_file(file_path)
                if local_path:
                    metadata = self.extract_access_metadata(local_path)
                    access_file_data.append(metadata)

            extraction_data["access_files"] = access_file_data

            # 3. Search for code files
            print("\n🔍 Step 3: Searching for SQL and VBA code...")
            code_data = self.search_for_queries_and_code(["/c/", "/d/", "/opt/"])
            extraction_data["code_data"] = code_data

            # 4. Get database information
            print("\n🗄️  Step 4: Getting database information...")
            db_info = self.generate_database_info()
            extraction_data["database_info"] = db_info

            # 5. Save results
            print("\n💾 Step 5: Saving extraction results...")
            self.save_extraction_results(extraction_data)

            print("\n✅ Extraction completed successfully!")
            print(f"📂 Results saved in: {self.output_dir}")

        except Exception as e:
            print(f"❌ Error during extraction: {e}")

        finally:
            if self.sftp_client:
                self.sftp_client.close()
            if self.ssh_client:
                self.ssh_client.close()
            print("🔒 Connection closed")


if __name__ == "__main__":
    extractor = AccessDataExtractor()
    extractor.run_extraction()
