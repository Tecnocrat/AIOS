import os
import zipfile

def extract_python_files_to_zip(folder_path, output_zip):
    """
    Extracts all Python files from the given folder and writes their contents to a compressed ZIP file.

    Args:
        folder_path (str): The folder to search for Python files.
        output_zip (str): The path to the output ZIP file.
    """
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            file_content = f.read()
                            # Write the file content to the ZIP archive
                            relative_path = os.path.relpath(file_path, folder_path)
                            zipf.writestr(relative_path, file_content)
                            print(f"Added {relative_path} to {output_zip}")
                    except UnicodeDecodeError as e:
                        print(f"Error reading {file_path}: {e}")

# Specify the folder to scan and the output ZIP file
extract_python_files_to_zip("C:\\Dev", "extracted_python_files.zip")