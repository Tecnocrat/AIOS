import os
import sys
import threading
import base64
import zipfile
import shutil
import time
import psutil

# Add CodeBot folder to Python search path
CODEBOT_DIR = os.path.dirname(os.path.abspath(__file__))
ADB_DIR = os.path.join(os.path.dirname(CODEBOT_DIR), "adn_trash_code")
os.makedirs(ADB_DIR, exist_ok=True)

MODULES_DIR = os.path.join(CODEBOT_DIR, "modules")
if MODULES_DIR not in sys.path:
    sys.path.append(MODULES_DIR)

# Import modules
from modules.file_manager import setup_project_structure, scan_test_folder, inject_text
from modules.compression import compress_libraries, decompress_library
from modules.knowledge_base import create_knowledge_archive, save_knowledge
from modules.ui_interface import launch_ui
from modules.dictionaries import save_wordlists
from modules.learning import load_language_libraries, analyze_library, copy_core_for_testing
from modules.ai_engine import explain_python_code
from modules.text_injector import inject_text as custom_inject_text

# ------------------
# CORE FUNCTIONS
# ------------------
def monitor_resources():
    """
    Monitors system resources (CPU, memory, and disk usage) and logs the data periodically.
    """
    print("Starting resource monitoring...")
    try:
        while True:
            # Get CPU usage
            cpu_usage = psutil.cpu_percent(interval=1)
            # Get memory usage
            memory = psutil.virtual_memory()
            memory_usage = memory.percent
            # Get disk usage
            disk = psutil.disk_usage('/')
            disk_usage = disk.percent

            # Log the resource usage
            print(f"CPU Usage: {cpu_usage}% | Memory Usage: {memory_usage}% | Disk Usage: {disk_usage}%")

            # Sleep for a short interval before the next check
            time.sleep(5)
    except Exception as e:
        print(f"Error monitoring resources: {e}")


def clear_folder(folder_path):
    """
    Deletes all contents of the specified folder and recreates it.
    """
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)
    print(f"Cleared and recreated folder: {folder_path}")


def extract_python_files_to_zip(folder_path, output_zip):
    """
    Extracts all Python files from the given folder and writes their contents to a compressed ZIP file.
    """
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            file_content = f.read()
                            relative_path = os.path.relpath(file_path, folder_path)
                            zipf.writestr(relative_path, file_content)
                            print(f"Added {relative_path} to {output_zip}")
                    except UnicodeDecodeError as e:
                        print(f"Error reading {file_path}: {e}")


def extract_zip_to_folder(zip_path, output_folder):
    """
    Extracts the contents of a ZIP file to the specified folder.
    """
    with zipfile.ZipFile(zip_path, "r") as zipf:
        zipf.extractall(output_folder)
        print(f"Extracted ZIP contents to: {output_folder}")


def compress_and_encode_script(script_path=None, zip_name="codebot_core.zip", output_file_base="codebot_core_base64_vol"):
    """
    Compresses the script into a ZIP file, encodes it in Base64, and splits it into chunks.
    """
    if script_path is None:
        script_path = os.path.abspath(__file__)
    zip_path = os.path.join(ADB_DIR, zip_name)
    with zipfile.ZipFile(zip_path, "w") as zipf:
        zipf.write(script_path, arcname="codebot_core.py")
    print(f"Script compressed into: {zip_name}")
    with open(zip_path, "rb") as zip_file:
        encoded = base64.b64encode(zip_file.read()).decode("utf-8")
    return split_and_save_base64(encoded, output_file_base)


def split_and_save_base64(encoded_text, volume_base="codebot_core_base64_vol", chunk_size=9999):
    """
    Splits a Base64-encoded string into chunks and saves them as separate files.
    """
    volumes = [encoded_text[i:i+chunk_size] for i in range(0, len(encoded_text), chunk_size)]
    volume_files = []
    for index, chunk in enumerate(volumes, start=1):
        filename = f"{volume_base}{index}.txt"
        output_path = os.path.join(ADB_DIR, filename)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(chunk)
        volume_files.append(filename)
        print(f"Saved Volume {index} to {filename}")
    return volume_files


def modularize_functions():
    """
    Placeholder function for modularizing functions.
    Add the logic for modularizing functions here.
    """
    print("Modularizing functions... (this is a placeholder)")


# ------------------
# MAIN EXECUTION
# ------------------
if __name__ == "__main__":
    try:
        print("\nStep 1: Setting up project structure...")
        setup_project_structure()

        print("\nStep 2: Modularizing functions...")
        modularize_functions()

        print("\nStep 3: Launching resource monitor...")
        resource_monitor_thread = threading.Thread(target=monitor_resources, daemon=True)
        resource_monitor_thread.start()

        print("\nStep 4: Launching UI Interface...")
        launch_ui()

        print("\nStep 5: Creating knowledge archive...")
        create_knowledge_archive("../adn_trash_code")

        print("\nStep 6: Compressing libraries...")
        compress_libraries()

        print("\nStep 7: Encoding main script to Base64 and splitting into volumes...")
        volumes_created = compress_and_encode_script()
        print("Volumes created:", volumes_created)

        print("\nStep 8: Testing decompression of runtime library...")
        decompress_library(file_to_extract="runtime_library.txt")

        print("\nStep 9: Scanning test folder...")
        test_tools = scan_test_folder("C:\\dev\\test")
        print(f"Available tools in the test folder: {test_tools}")

        print("\nStep 10: Generating symbol library...")
        save_wordlists("C:\\dev\\adn_trash_code\\dictionaries")

        print("\nStep 11: Teaching CodeBot Python...")
        python_libs = load_language_libraries(language="python")
        for lib in python_libs:
            analyze_library(os.path.join("C:\\dev\\adn_trash_code\\python_libs", lib), debug=False)

        print("\nStep 12: Creating parallel testing environment...")
        copy_core_for_testing()

        print("\nStep 13: Backing up the entire C:\\Dev codebase...")
        codebase_folder = os.path.join(ADB_DIR, "knowledge_base", "codebase")
        clear_folder(codebase_folder)

        zip_path = os.path.join(ADB_DIR, "knowledge_base", "codebase_backup.zip")
        extract_python_files_to_zip("C:\\Dev", zip_path)
        extract_zip_to_folder(zip_path, codebase_folder)

        print("\nStep 14: Explaining a Python code snippet...")
        code_snippet = """
        def greet(name):
            return f'Hello, {name}!'
        """
        explanation = explain_python_code(code_snippet)
        print(f"AI Explanation:\n{explanation}")

        print("\nStep 15: Injecting text into a file...")
        file_path = "C:\\dev\\example.txt"
        text = "This is a test injection."
        result = inject_text(file_path, text, position="append")
        print(result)

        print("\nStep 16: Saving knowledge...")
        knowledge_file = "C:\\dev\\knowledge.txt"
        knowledge = "Knowledge is power."
        save_knowledge(knowledge_file, knowledge)

        print("\nStep 17: Custom text injection...")
        custom_file = "C:\\dev\\custom.txt"
        custom_text = "Custom injection example."
        custom_result = custom_inject_text(custom_file, custom_text, position="overwrite")
        print(custom_result)

        print("\nAll tasks completed successfully.")
    except Exception as e:
        print(f"An error occurred during execution: {e}")