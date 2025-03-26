from library.utils import (
    list_files_and_directories,
    save_to_json,
    find_json_files,
    delete_identical_json_files,
)
import os
from datetime import datetime
from library.ai_core import AICore
import psutil

class AIOSCore:
    def __init__(self):
        """
        Initializes the AIOS core system.
        """
        self.ai_core = AICore()

    def self_reflex(self):
        """
        Triggers the self-reflection process in the AI core.
        :return: Metadata generated during self-reflection.
        """
        return self.ai_core.self_reflex()

    def start_interface(self, command):
        """
        Handles commands sent from the main application.
        :param command: The command to execute.
        :return: The result of the command execution.
        """
        if command == "self_reflex":
            return self.self_reflex()
        elif command == "status":
            return {"status": "AIOS Core is running", "timestamp": datetime.now().isoformat()}
        else:
            return {"error": f"Unknown command: {command}"}

def create_file(file_name):
    """
    Creates an empty file in the 'C:\\dev' directory.
    """
    try:
        file_path = os.path.join("C:\\dev", file_name)
        with open(file_path, "w") as f:
            pass
        print(f"File '{file_name}' created successfully at {file_path}.")
    except Exception as e:
        print(f"An error occurred while creating the file: {e}")


def scan_file_system():
    """
    Scans the file system and saves the structure to a JSON file.
    """
    default_directory = "C:\\dev"
    storage_directory = os.path.join(default_directory, "storage", "directory")
    os.makedirs(storage_directory, exist_ok=True)

    print(f"Default directory to scan: {default_directory}")
    start_directory = input(f"Enter the directory path to scan (or press Enter to use '{default_directory}'): ").strip()
    if not start_directory:
        start_directory = default_directory

    if os.path.exists(start_directory):
        print(f"\nScanning the directory structure of {start_directory}...\n")
        directory_structure = list_files_and_directories(start_directory)

        # Generate a unique filename based on the current timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(storage_directory, f"{timestamp}.json")

        # Save the output to the JSON file
        save_to_json(directory_structure, output_file)
        print(f"Directory structure saved to {output_file}.")
    else:
        print(f"The directory {start_directory} does not exist. Please check the path.")


def clean_json_files():
    """
    Cleans duplicate JSON files in the storage directory.
    """
    storage_directory = os.path.join("c:\\dev\\storage", "directory")
    print(f"Searching for JSON files in {storage_directory}...")
    delete_identical_json_files(storage_directory)
    print("Finished processing JSON files.")