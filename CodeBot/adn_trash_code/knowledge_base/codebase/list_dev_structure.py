import os
import ast
import json

def list_files_and_metadata(start_path):
    """
    Recursively lists all files and directories starting from the specified path.
    Extracts metadata from Python files (functions, classes, and imports).
    """
    structure = {}

    for root, dirs, files in os.walk(start_path):
        dir_name = os.path.basename(root)
        structure[dir_name] = {"files": {}, "subdirectories": dirs}

        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                structure[dir_name]["files"][file] = extract_metadata(file_path)

    return structure


def extract_metadata(file_path):
    """
    Extracts metadata from a Python file: functions, classes, and imports.
    """
    metadata = {"functions": [], "classes": [], "imports": []}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=file_path)
            for node in ast.iter_child_nodes(tree):
                if isinstance(node, ast.FunctionDef):
                    metadata["functions"].append(node.name)
                elif isinstance(node, ast.ClassDef):
                    metadata["classes"].append(node.name)
                elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        metadata["imports"].append(alias.name)
    except Exception as e:
        metadata["error"] = str(e)

    return metadata


def save_structure_to_json(structure, output_file):
    """
    Saves the directory and metadata structure to a JSON file.
    """
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(structure, f, indent=4)
    print(f"Basecode structure saved to {output_file}")


def get_versioned_filename(base_path, base_name, extension):
    """
    Generates a versioned filename by appending a version number to the base name.
    """
    version = 1
    while True:
        file_name = f"{base_name}_v{version:02d}{extension}"
        full_path = os.path.join(base_path, file_name)
        if not os.path.exists(full_path):
            return full_path
        version += 1


if __name__ == "__main__":
    start_directory = "C:\\dev\\CodeBot"  # Adjust as needed
    base_path = "C:\\dev"
    base_name = "basecode_metadata"
    extension = ".json"

    # Generate a versioned filename for the output file
    output_file = get_versioned_filename(base_path, base_name, extension)

    if os.path.exists(start_directory):
        print(f"Scanning and extracting metadata from {start_directory}...\n")
        basecode_structure = list_files_and_metadata(start_directory)
        save_structure_to_json(basecode_structure, output_file)
    else:
        print(f"The directory {start_directory} does not exist. Please check the path.")