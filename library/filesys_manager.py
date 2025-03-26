import os
import json
from datetime import datetime
from deepdiff import DeepDiff
from library.autologger import AutoLogger

# Initialize logger
autologger = AutoLogger()
logger = autologger.get_logger("filesys_manager")

def generate_file_structure(root_directory="C:\\dev", storage_directory="C:\\dev\\OS\\storage\\filesys"):
    """
    Generates a JSON file describing the file structure of the given root directory.
    Saves the latest snapshot to 'filesys.main.json', full snapshots with timestamps to 'time_sys',
    and changes (diffs) between snapshots to 'simple_sys'.
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
            diff = DeepDiff(last_snapshot, current_snapshot, ignore_order=True).to_dict()
            if not diff:
                logger.info("No changes detected in the file structure. Skipping save.")
                return None

            # Save the diff to `simple_sys`
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