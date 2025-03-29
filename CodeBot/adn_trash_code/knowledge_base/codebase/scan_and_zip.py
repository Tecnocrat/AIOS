import os
import zipfile


def list_files_and_directories(start_path, output_file=None):
    """
    Recursively lists all files and directories starting from the specified path.
    Displays the file structure in a tree-like format and optionally writes it to a file.
    """
    content = []
    for root, dirs, files in os.walk(start_path):
        # Calculate the depth to display the tree structure
        level = root.replace(start_path, "").count(os.sep)
        indent = " " * 4 * level
        line = f"{indent}{os.path.basename(root)}/"
        content.append(line)  # Collect the directory name
        print(line)

        # Print all files in the current directory
        sub_indent = " " * 4 * (level + 1)
        for file in files:
            line = f"{sub_indent}{file}"
            content.append(line)  # Collect file names
            print(line)

    # Optionally save the output to a file
    if output_file:
        with open(output_file, "w", encoding="utf-8") as file:
            file.write("\n".join(content))
        print(f"\nFile structure saved to {output_file}")


def create_zip_with_history(zip_directory, zip_name):
    """
    Creates a zip archive of the specified directory.
    Handles historical backups by renaming existing ZIP files with a numbered suffix.
    """
    # Check if the main zip file exists
    base_name, extension = os.path.splitext(zip_name)
    version = 1

    # Rename existing files if necessary
    while os.path.exists(os.path.join(zip_directory, zip_name)):
        zip_name = f"{base_name}_{version:02}{extension}"
        version += 1

    # Create the zip file
    zip_path = os.path.join(zip_directory, zip_name)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(zip_directory):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, zip_directory)
                zipf.write(file_path, arcname)
    print(f"\nFile system zipped to: {zip_path}")


if __name__ == "__main__":
    # Specify the directory to scan
    start_directory = "C:\\dev"  # Adjust as needed
    output_file = os.path.join(start_directory, "filesystem_structure.txt")
    zip_name = "file_sys.zip"

    # Ensure the directory exists
    if os.path.exists(start_directory):
        print(f"Scanning and zipping the directory structure of {start_directory}...\n")

        # List files and directories, saving the output to a file
        list_files_and_directories(start_directory, output_file)

        # Create a ZIP archive with versioning
        create_zip_with_history(start_directory, zip_name)
    else:
        print(f"The directory {start_directory} does not exist. Please check the path.")
