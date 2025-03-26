import zipfile
import os

# Prompt the user for the extraction folder path
output_folder = input("Enter the folder path where you want to extract the files: ").strip()

# Ensure the folder exists or create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Extract the ZIP file to the specified folder
with zipfile.ZipFile("extracted_python_files.zip", "r") as zipf:
    zipf.extractall(output_folder)  # Extracts to the user-specified folder
    print(f"Files extracted to: {output_folder}")