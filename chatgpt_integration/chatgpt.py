#!/usr/bin/env python3
"""
ChatGPT Integration - AI Conversation Ingestion and Archival System
================================================================

This script processes markdown conversation logs from various AI engines
(ChatGPT, Copilot, Gemini, VSCopilot) and converts them to multiple formats
for ingestion and archival purposes.

Usage: python chatgpt.py
"""

import os
import sys
import json
import shutil
from datetime import datetime
from pathlib import Path

# Get the script's directory to ensure proper path resolution
SCRIPT_DIR = Path(__file__).parent.absolute()
CHATGPT_INTEGRATION_DIR = SCRIPT_DIR
AIOS_ROOT = SCRIPT_DIR.parent

# Ensure we're working with absolute paths
MD_FOLDER = CHATGPT_INTEGRATION_DIR / "md"
INGESTION_FOLDER = CHATGPT_INTEGRATION_DIR / "ingestion"
ARK_FOLDER = MD_FOLDER / "ark"

print("🔧 ChatGPT Integration System")
print(f"📁 Working directory: {CHATGPT_INTEGRATION_DIR}")
print(f"📄 MD folder: {MD_FOLDER}")
print(f"📦 Ingestion folder: {INGESTION_FOLDER}")
print(f"🗄️ Archive folder: {ARK_FOLDER}")
print("-" * 50)


def move_to_archive(output_folder):
    """Move existing files to archive before creating new ones"""
    output_path = Path(output_folder)
    archive_folder = output_path / "archive"
    archive_folder.mkdir(exist_ok=True)

    for file_path in output_path.iterdir():
        if file_path.name != "archive" and file_path.is_file():
            archive_path = archive_folder / file_path.name

            if archive_path.exists():
                file_type = file_path.suffix[1:]  # Remove the dot
                type_folder = archive_folder / file_type
                type_folder.mkdir(exist_ok=True)

                type_file_path = type_folder / file_path.name
                if type_file_path.exists():
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    new_file_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
                    shutil.move(str(file_path), str(type_folder / new_file_name))
                else:
                    shutil.move(str(file_path), str(type_file_path))
            else:
                shutil.move(str(file_path), str(archive_path))


def convert_md_to_formats(md_file_path, output_folder):
    """Convert markdown file to multiple formats (txt, csv, json, xml)"""
    md_path = Path(md_file_path)
    output_path = Path(output_folder)

    # Create output folder if it doesn't exist
    output_path.mkdir(exist_ok=True)

    # Move existing files to archive if output folder has files
    if any(output_path.iterdir()):
        move_to_archive(output_path)

    with open(md_path, "r", encoding="utf-8") as md_file:
        content = md_file.read()

    base_name = md_path.stem  # filename without extension

    # Convert to .txt
    txt_path = output_path / f"{base_name}.txt"
    with open(txt_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(content)

    # Convert to .csv
    csv_path = output_path / f"{base_name}.csv"
    csv_content = "Title,Description\n" + content.replace("\n", "\n")
    with open(csv_path, "w", encoding="utf-8") as csv_file:
        csv_file.write(csv_content)

    # Convert to .json
    json_path = output_path / f"{base_name}.json"
    json_content = {"content": content}
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(json_content, json_file, indent=4)

    # Convert to .xml
    xml_path = output_path / f"{base_name}.xml"
    xml_content = f'<?xml version="1.0" encoding="UTF-8"?>\n<document>\n<content>{content}</content>\n</document>'
    with open(xml_path, "w", encoding="utf-8") as xml_file:
        xml_file.write(xml_content)

    print(f"✅ Converted {md_path.name} to multiple formats")


def process_md_files(input_folder, output_folder):
    """Process all markdown files in input folder and convert to multiple formats"""
    input_path = Path(input_folder)
    output_path = Path(output_folder)

    if not input_path.exists():
        print(f"❌ Input folder {input_path} does not exist")
        return

    md_files = list(input_path.glob("*.md"))
    if not md_files:
        print(f"❌ No markdown files found in {input_path}")
        return

    # Create output folder if it doesn't exist
    output_path.mkdir(exist_ok=True)

    # Move existing files to archive once at the start
    if any(output_path.iterdir()):
        print("� Moving existing ingestion files to archive...")
        move_to_archive(output_path)

    print(f"�📄 Processing {len(md_files)} markdown files...")
    for md_file in md_files:
        convert_md_to_formats_no_archive(md_file, output_path)

    print(f"✅ All files processed to {output_path}")


def convert_md_to_formats_no_archive(md_file_path, output_folder):
    """Convert markdown file to multiple formats without archiving (used in batch processing)"""
    md_path = Path(md_file_path)
    output_path = Path(output_folder)

    with open(md_path, "r", encoding="utf-8") as md_file:
        content = md_file.read()

    base_name = md_path.stem  # filename without extension

    # Convert to .txt
    txt_path = output_path / f"{base_name}.txt"
    with open(txt_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(content)

    # Convert to .csv
    csv_path = output_path / f"{base_name}.csv"
    csv_content = "Title,Description\n" + content.replace("\n", "\n")
    with open(csv_path, "w", encoding="utf-8") as csv_file:
        csv_file.write(csv_content)

    # Convert to .json
    json_path = output_path / f"{base_name}.json"
    json_content = {"content": content}
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(json_content, json_file, indent=4)

    # Convert to .xml
    xml_path = output_path / f"{base_name}.xml"
    xml_content = f'<?xml version="1.0" encoding="UTF-8"?>\n<document>\n<content>{content}</content>\n</document>'
    with open(xml_path, "w", encoding="utf-8") as xml_file:
        xml_file.write(xml_content)

    print(f"✅ Converted {md_path.name} to multiple formats")


def create_vscopilot_iteration():
    """Archive current vscopilot conversation and clear for new iteration (legacy function)"""
    vscopilot_path = "md/vscopilot.md"
    vscopilot_ark_path = "md/vscopilot_ark.md"

    # Ensure vscopilot.md exists
    if not os.path.exists(vscopilot_path):
        print("vscopilot.md does not exist.")
        return

    # Read contents of vscopilot.md
    with open(vscopilot_path, "r", encoding="utf-8") as vscopilot_file:
        vscopilot_content = vscopilot_file.read()

    # Append contents to vscopilot_ark.md
    with open(vscopilot_ark_path, "a", encoding="utf-8") as vscopilot_ark_file:
        vscopilot_ark_file.write(
            f"\n--- Iteration {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n"
        )
        vscopilot_ark_file.write(vscopilot_content)

    # Clear vscopilot.md for next iteration
    with open(vscopilot_path, "w", encoding="utf-8") as vscopilot_file:
        vscopilot_file.write("")


def create_engine_iteration(engine_name):
    """Archive current engine conversation and clear for new iteration"""
    engine_path = MD_FOLDER / f"{engine_name}.md"
    ARK_FOLDER.mkdir(exist_ok=True)
    engine_ark_path = ARK_FOLDER / f"{engine_name}_ark.md"

    # Ensure engine.md exists
    if not engine_path.exists():
        print(f"❌ {engine_name}.md does not exist at {engine_path}")
        return

    # Read contents of engine.md
    with open(engine_path, "r", encoding="utf-8") as engine_file:
        engine_content = engine_file.read()

    if not engine_content.strip():
        print(f"⚠️ {engine_name}.md is empty, nothing to archive")
        return

    # Append contents to engine_ark.md
    with open(engine_ark_path, "a", encoding="utf-8") as engine_ark_file:
        engine_ark_file.write(
            f"\n--- Iteration {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n"
        )
        engine_ark_file.write(engine_content)

    # Clear engine.md for next iteration
    with open(engine_path, "w", encoding="utf-8") as engine_file:
        engine_file.write("")

    print(f"✅ {engine_name}.md archived and cleared for new iteration")


def engines_submenu():
    """Submenu for engine-specific operations"""
    print("\n🔧 Engine Operations:")
    print("Choose an engine to archive and clear:")
    print("1. chatgpt")
    print("2. copilot")
    print("3. gemini")
    print("4. vscopilot")
    print("5. Back to main menu")

    engine_choice = input("Enter your choice (1-5): ").strip()

    engine_map = {"1": "chatgpt", "2": "copilot", "3": "gemini", "4": "vscopilot"}

    if engine_choice in engine_map:
        engine_name = engine_map[engine_choice]
        print(f"🗄️ Processing {engine_name} engine...")
        create_engine_iteration(engine_name)
    elif engine_choice == "5":
        return
    else:
        print("❌ Invalid choice. Please enter 1-5.")


def main():
    """Main function with improved error handling and path validation"""
    print("🤖 AIOS ChatGPT Integration System")
    print(f"🐍 Python: {sys.version}")
    print(f"📂 Working from: {CHATGPT_INTEGRATION_DIR}")
    print()

    # Ensure required directories exist
    MD_FOLDER.mkdir(exist_ok=True)
    INGESTION_FOLDER.mkdir(exist_ok=True)
    ARK_FOLDER.mkdir(exist_ok=True)

    try:
        print("Choose an option:")
        print("1. Create ingestion (convert all .md files to multiple formats)")
        print("2. Engines submenu (archive and clear specific engine)")
        print("3. Show current files status")
        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            print(f"📋 Processing markdown files from {MD_FOLDER} to {INGESTION_FOLDER}")
            process_md_files(MD_FOLDER, INGESTION_FOLDER)
        elif choice == "2":
            engines_submenu()
        elif choice == "3":
            show_files_status()
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")
    except KeyboardInterrupt:
        print("\n⚠️ Operation cancelled by user")
    except (OSError, IOError, FileNotFoundError) as e:
        print(f"❌ File system error: {e}")
    except ValueError as e:
        print(f"❌ Invalid input: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


def show_files_status():
    """Show current status of markdown files"""
    print("\n📊 Current Files Status:")
    print("-" * 40)

    for engine in ["chatgpt", "copilot", "gemini", "vscopilot"]:
        engine_path = MD_FOLDER / f"{engine}.md"
        ark_path = ARK_FOLDER / f"{engine}_ark.md"

        if engine_path.exists():
            size = engine_path.stat().st_size
            status = f"📄 {size} bytes" if size > 0 else "📄 Empty"
        else:
            status = "❌ Missing"

        ark_status = "🗄️ Has archive" if ark_path.exists() else "🗄️ No archive"
        print(f"  {engine:10} → {status:15} | {ark_status}")

    print("\n📦 Ingestion files:")
    if INGESTION_FOLDER.exists():
        ingestion_files = list(INGESTION_FOLDER.glob("*"))
        if ingestion_files:
            for file in ingestion_files:
                if file.is_file():
                    print(f"  📄 {file.name}")
        else:
            print("  📄 No ingestion files")
    print()


if __name__ == "__main__":
    main()
