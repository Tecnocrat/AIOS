import os
import json
import time
import zipfile
import logging
from deepdiff import DeepDiff  # Install with `pip install deepdiff`
from datetime import datetime
from library.autologger import AutoLogger

# Initialize the centralized autologging system
autologger = AutoLogger()
logger = autologger.get_logger("utils")  # Get a logger for the 'utils' namespace

# Initialize the logging, autolog, and debugger
autolog = None  # Placeholder until AutoLogDebugger is correctly imported or replaced.
# Replace AutoLogDebugger with a basic logger until the correct module is resolved.
autolog = logging.getLogger("autolog")
autolog.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
autolog.addHandler(handler)

# ------------------
# Filesystem Functions
# ------------------
def list_files_and_directories(start_path):
    """
    Recursively lists all files and directories starting from the specified path.
    Returns the file structure as a nested dictionary.
    """
    nested_file_structure = {}

    for root, dirs, files in os.walk(start_path):
        relative_path = os.path.relpath(root, start_path)
        if (relative_path == "."):
            relative_path = os.path.basename(root)

        current_dir = nested_file_structure
        for part in relative_path.split(os.sep):
            current_dir = current_dir.setdefault(part, {})

        current_dir["files"] = files

    return nested_file_structure


def save_to_json(data, output_path):
    """
    Saves the given data to a JSON file at the specified output path.
    If the file already exists, creates a copy with a unique name only if the content differs.
    """
    try:
        if os.path.exists(output_path):
            # Load existing data for comparison
            with open(output_path, "r", encoding="utf-8") as existing_file:
                existing_data = json.load(existing_file)
            
            # Compare the new data with the existing data
            if data == existing_data:
                logger.info(f"No changes detected in {output_path}. Skipping save.")
                return

            # Create a unique name for the new file if content differs
            base, ext = os.path.splitext(output_path)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"{base}_{timestamp}{ext}"

        # Save the new data to the JSON file
        with open(output_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4)
        logger.info(f"Data saved to {output_path}.")
    except Exception as e:
        logger.error(f"Error saving to JSON file: {e}")
        raise

# ------------------
# JSON Comparison Functions
# ------------------
def load_json(file_path):
    """
    Loads a JSON file and returns its content.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)
    except Exception as e:
        logging.error(f"Error loading JSON file {file_path}: {e}")
        raise


def compare_json_files(file1, file2):
    """
    Compares two JSON files and returns their differences.
    If no differences are found, returns None.
    """
    data1 = load_json(file1)
    data2 = load_json(file2)

    if data1 is None or data2 is None:
        print("Error: One or both JSON files could not be loaded.")
        return None

    differences = DeepDiff(data1, data2, ignore_order=True)
    return differences if differences else None


def find_json_files(directory):
    """
    Finds all JSON files in the specified directory.
    """
    json_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(root, file))
    return json_files


def delete_identical_json_files(directory):
    """
    Searches for all JSON files in the directory, reports differences, and deletes identical copies.
    """
    json_files = find_json_files(directory)
    checked_files = set()

    for i, file1 in enumerate(json_files):
        if file1 in checked_files:
            continue

        for file2 in json_files[i + 1:]:
            if file2 in checked_files:
                continue

            differences = compare_json_files(file1, file2)
            if differences is None:
                print(f"Identical files found: {file1} and {file2}")
                print(f"Deleting {file2}...")
                os.remove(file2)
                checked_files.add(file2)
            else:
                print(f"Differences found between {file1} and {file2}:")
                # Convert differences to a JSON-serializable format
                print(json.dumps(differences, indent=4))

        checked_files.add(file1)

def backup_system():
    """
    Creates a backup of critical system files and logs, excluding the backups folder itself.
    """
    try:
        backup_dir = os.path.join("C:\\dev", "backups")
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"backup_{timestamp}.zip")

        logger.info(f"Creating system backup at {backup_file}...")
        with zipfile.ZipFile(backup_file, "w") as backup_zip:
            for folder_name, subfolders, filenames in os.walk("C:\\dev"):
                # Exclude the backups folder
                if folder_name.startswith(backup_dir):
                    continue

                for filename in filenames:
                    file_path = os.path.join(folder_name, filename)
                    try:
                        # Add the file to the zip archive
                        backup_zip.write(file_path, os.path.relpath(file_path, "C:\\dev"))
                    except Exception as e:
                        logger.warning(f"Failed to back up file: {file_path}. Error: {e}")

        logger.info(f"System backup created at {backup_file}.")
    except Exception as e:
        logger.error(f"Error during system backup: {e}")

def analyze_file_system(root_directory="C:\\dev", output_file=None):
    """
    Analyzes the file system starting from the given root directory and generates a JSON file.
    :param root_directory: The root directory to analyze.
    :param output_file: The path to save the JSON output. Defaults to 'C:\\dev\\storage\\directory_structure.json'.
    :return: The path to the generated JSON file.
    """
    try:
        logger.info(f"Starting file system analysis for root directory: {root_directory}")

        # Default output file location
        if (output_file is None):
            storage_dir = os.path.join(root_directory, "storage")
            os.makedirs(storage_dir, exist_ok=True)
            output_file = os.path.join(storage_dir, "directory_structure.json")

        # Recursive function to analyze the directory structure
        def analyze_directory(directory):
            structure = {"type": "directory", "path": directory, "contents": []}
            try:
                for entry in os.scandir(directory):
                    if entry.is_dir(follow_symlinks=False):
                        structure["contents"].append(analyze_directory(entry.path))
                    elif entry.is_file(follow_symlinks=False):
                        structure["contents"].append({
                            "type": "file",
                            "path": entry.path,
                            "size": os.path.getsize(entry.path)
                        })
            except PermissionError as e:
                logger.warning(f"Permission denied: {directory}. Error: {e}")
                structure["contents"].append({"type": "error", "message": "Permission denied"})
            return structure

        # Analyze the root directory
        directory_structure = analyze_directory(root_directory)

        # Add metadata
        output_data = {
            "root_directory": root_directory,
            "timestamp": datetime.now().isoformat(),
            "structure": directory_structure
        }

        # Save to JSON file
        with open(output_file, "w") as json_file:
            json.dump(output_data, json_file, indent=4)
        logger.info(f"File system analysis complete. Output saved to: {output_file}")

        return output_file
    except Exception as e:
        logger.error(f"Error during file system analysis: {e}")
        return None

def generate_file_structure(root_directory="C:\\dev", storage_directory="C:\\dev\\OS\\storage\\filesys"):
    """
    Generates a JSON file describing the file structure of the given root directory.
    Saves the latest snapshot to 'filesys.main.json', full snapshots with timestamps to 'time_sys',
    and changes (diffs) between snapshots to 'simple_sys'.
    :param root_directory: The root directory to analyze.
    :param storage_directory: The base directory for storing file system snapshots.
    :return: The path to the saved JSON file, or None if no changes were detected.
    """
    try:
        logger.info(f"Generating file structure for root directory: {root_directory}")

        # Ensure the storage directories exist
        os.makedirs(storage_directory, exist_ok=True)
        time_sys_dir = os.path.join(storage_directory, "time_sys")
        simple_sys_dir = os.path.join(storage_directory, "simple_sys")
        os.makedirs(time_sys_dir, exist_ok=True)
        os.makedirs(simple_sys_dir, exist_ok=True)

        # Recursive function to analyze the directory structure
        def analyze_directory(directory):
            structure = {"type": "directory", "path": directory, "contents": []}
            try:
                for entry in os.scandir(directory):
                    if entry.is_dir(follow_symlinks=False):
                        structure["contents"].append(analyze_directory(entry.path))
                    elif entry.is_file(follow_symlinks=False):
                        structure["contents"].append({
                            "type": "file",
                            "path": entry.path,
                            "size": os.path.getsize(entry.path)
                        })
            except PermissionError as e:
                logger.warning(f"Permission denied: {directory}. Error: {e}")
                structure["contents"].append({"type": "error", "message": "Permission denied"})
            return structure

        # Analyze the root directory
        directory_structure = analyze_directory(root_directory)

        # Add metadata
        output_data = {
            "root_directory": root_directory,
            "timestamp": datetime.now().isoformat(),
            "structure": directory_structure
        }

        # Path to the main JSON file
        main_file_path = os.path.join(storage_directory, "filesys.main.json")

        # Load the last snapshot if it exists
        last_snapshot = None
        if os.path.exists(main_file_path):
            with open(main_file_path, "r") as main_file:
                last_snapshot = json.load(main_file)

        # Compare with the last snapshot
        if last_snapshot:
            # Remove the timestamp field for comparison
            last_snapshot.pop("timestamp", None)
            current_snapshot = output_data.copy()
            current_snapshot.pop("timestamp", None)

            # Check for differences
            if last_snapshot == current_snapshot:
                logger.info("No changes detected in the file structure. Skipping save.")
                return None

            # Generate a diff and save it to `simple_sys`
            diff = DeepDiff(last_snapshot, current_snapshot, ignore_order=True).to_dict()
            if diff:
                diff_file_path = os.path.join(simple_sys_dir, f"changes.{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
                with open(diff_file_path, "w") as diff_file:
                    json.dump(diff, diff_file, indent=4)
                logger.info(f"Changes detected. Diff saved to: {diff_file_path}")

        # Save the new snapshot to `filesys.main.json`
        with open(main_file_path, "w") as main_file:
            json.dump(output_data, main_file, indent=4)
        logger.info(f"Latest snapshot saved to: {main_file_path}")

        # Save a full snapshot with a timestamp to `time_sys`
        timestamped_file_path = os.path.join(time_sys_dir, f"filesys.{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(timestamped_file_path, "w") as timestamped_file:
            json.dump(output_data, timestamped_file, indent=4)
        logger.info(f"Full snapshot saved to: {timestamped_file_path}")

        return main_file_path
    except Exception as e:
        logger.error(f"Error generating file structure: {e}")
        return None