#!/usr/bin/env python3
"""
Quick MS Access Data Extraction
Simplified version for rapid information gathering
"""

import json
import os
from datetime import datetime
from pathlib import Path

import paramiko

# Server configuration
REMOTE_HOST = "91.222.248.216"
REMOTE_PORT = 61317
REMOTE_USER = "user101"
REMOTE_PASSWORD = os.getenv("REMOTE_PASSWORD", "your_remote_password_here")


def connect_ssh():
    """Create SSH connection"""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname=REMOTE_HOST,
        port=REMOTE_PORT,
        username=REMOTE_USER,
        password=REMOTE_PASSWORD,
        timeout=60,
        banner_timeout=60,
        auth_timeout=60,
        look_for_keys=False,
        allow_agent=False,
    )
    return client


def execute_command(ssh_client, command):
    """Execute command and return output"""
    try:
        stdin, stdout, stderr = ssh_client.exec_command(command)
        return stdout.read().decode(errors="ignore").strip()
    except Exception as e:
        return f"Error: {e}"


def main():
    """Quick extraction of key information"""
    print("🚀 Quick Access Data Extraction")
    print(f"📡 Connecting to {REMOTE_HOST}:{REMOTE_PORT}...")

    try:
        ssh = connect_ssh()
        print("✅ Connected successfully")

        results = {
            "extraction_date": datetime.now().isoformat(),
            "server_info": {},
            "access_files": [],
            "mysql_info": {},
            "file_structure": {},
        }

        # 1. Basic server info
        print("\n📋 Getting server information...")
        results["server_info"] = {
            "hostname": execute_command(ssh, "hostname"),
            "os_info": execute_command(ssh, "uname -a"),
            "disk_usage": execute_command(ssh, "df -h"),
            "current_dir": execute_command(ssh, "pwd"),
            "user": execute_command(ssh, "whoami"),
        }

        # 2. Find Access files
        print("\n🔍 Searching for MS Access files...")
        access_search = execute_command(
            ssh,
            'find /c /d /opt . -name "*.mdb" -o -name "*.accdb" 2>/dev/null | head -10',
        )

        if access_search and access_search != "Error":
            results["access_files"] = access_search.split("\n")
            print(f"📁 Found {len(results['access_files'])} Access files")
            for file in results["access_files"]:
                if file:
                    print(f"  - {file}")

        # 3. Check MySQL connection
        print("\n🗄️ Checking MySQL database...")
        mysql_test = execute_command(
            ssh,
            "mysql -h localhost -u khtrm_remote -p'KhTRM_2025!' -e 'SHOW DATABASES;' 2>/dev/null",
        )

        if "saltdepoavt_" in mysql_test:
            print("✅ MySQL connection successful")

            # Get table list
            tables = execute_command(
                ssh,
                "mysql -h localhost -u khtrm_remote -p'KhTRM_2025!' saltdepoavt_ -e 'SHOW TABLES;' 2>/dev/null",
            )

            table_list = [
                line.strip() for line in tables.split("\n")[1:] if line.strip()
            ]
            results["mysql_info"] = {
                "connection": "success",
                "database": "saltdepoavt_",
                "tables_count": len(table_list),
                "tables": table_list[:20],  # First 20 tables
            }

            print(f"📊 Found {len(table_list)} tables in database")

            # Get dispatcher related tables info
            dispatcher_tables = [
                t
                for t in table_list
                if any(
                    keyword in t.lower()
                    for keyword in ["zanar", "marshr", "personal", "sprpe", "grafik"]
                )
            ]

            if dispatcher_tables:
                print(f"🎯 Found {len(dispatcher_tables)} dispatcher-related tables:")
                for table in dispatcher_tables:
                    print(f"  - {table}")

        # 4. Look for common directories
        print("\n📂 Checking directory structure...")
        dirs_to_check = [
            "/c/Program Files",
            "/c/Users",
            "/d/",
            "/opt/transport",
            "/var/log",
        ]

        for dir_path in dirs_to_check:
            dir_content = execute_command(
                ssh, f'ls -la "{dir_path}" 2>/dev/null | head -5'
            )
            if dir_content and "No such file" not in dir_content:
                results["file_structure"][dir_path] = dir_content.split("\n")

        # 5. Search for configuration files
        print("\n⚙️ Looking for configuration files...")
        config_files = execute_command(
            ssh,
            'find /c /d /opt . -name "*.ini" -o -name "*.cfg" -o -name "*.conf" 2>/dev/null | head -10',
        )

        if config_files:
            results["config_files"] = config_files.split("\n")

        # 6. Save results
        output_dir = Path("extracted_data")
        output_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_file = output_dir / f"quick_extraction_{timestamp}.json"

        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        # Generate summary report
        report_file = output_dir / f"extraction_summary_{timestamp}.md"
        with open(report_file, "w", encoding="utf-8") as f:
            f.write("# Quick Extraction Summary\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Server:** {REMOTE_HOST}:{REMOTE_PORT}\n\n")

            f.write("## 🗃️ MS Access Files\n")
            if results["access_files"]:
                for file in results["access_files"]:
                    if file:
                        f.write(f"- {file}\n")
            else:
                f.write("- No Access files found\n")

            f.write("\n## 🗄️ MySQL Database\n")
            if results["mysql_info"].get("connection") == "success":
                f.write(f"- **Database:** {results['mysql_info']['database']}\n")
                f.write(f"- **Tables:** {results['mysql_info']['tables_count']}\n")
                f.write("- **Key tables for dispatcher:**\n")
                dispatcher_tables = [
                    t
                    for t in results["mysql_info"]["tables"]
                    if any(
                        keyword in t.lower()
                        for keyword in ["zanar", "marshr", "personal", "sprpe"]
                    )
                ]
                for table in dispatcher_tables:
                    f.write(f"  - {table}\n")
            else:
                f.write("- Connection failed\n")

            f.write("\n## 📂 Directory Structure\n")
            for dir_path, content in results["file_structure"].items():
                f.write(f"### {dir_path}\n")
                for line in content[:3]:
                    f.write(f"- {line}\n")
                f.write("\n")

        print("\n💾 Results saved:")
        print(f"  📄 JSON: {json_file}")
        print(f"  📄 Report: {report_file}")
        print("\n✅ Quick extraction completed!")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        if "ssh" in locals():
            ssh.close()
            print("🔒 Connection closed")


if __name__ == "__main__":
    main()
