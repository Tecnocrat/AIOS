import os
import json

def get_folder_structure(root_dir, exclude_git=False):
    folder_structure = {}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Exclude .git folder if the option is selected
        if exclude_git and ".git" in dirpath:
            continue

        # Get relative path from the root directory
        relative_path = os.path.relpath(dirpath, root_dir)
        if relative_path == ".":
            relative_path = ""
        
        # Add folder and its files to the structure
        folder_structure[relative_path] = {
            "folders": dirnames,
            "files": filenames
        }
    return folder_structure

def save_to_json(data, output_folder, output_file):
    os.makedirs(output_folder, exist_ok=True)
    with open(os.path.join(output_folder, output_file), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def cli_ui():
    print("=== Folder Structure JSON Generator ===")
    print("Choose a folder to analyze:")
    print("1. Architect")
    print("2. chatgpt")
    print("3. AIOS")
    print("4. Exit")
    
    choice = input("Enter your choice (1/2/3/4): ").strip()
    return choice

if __name__ == "__main__":
    # Base paths for folders
    base_paths = {
        "1": r"C:\dev\Architect",
        "2": r"C:\dev\chatgpt",
        "3": r"C:\dev\AIOS"
    }

    while True:
        choice = cli_ui()
        if choice in base_paths:
            root_directory = base_paths[choice]
            folder_name = os.path.basename(root_directory)
            output_folder = os.path.join(r"C:\dev\AIOS\docs", folder_name)
            output_file = "folder_structure.json"

            print(f"Analyzing folder: {root_directory}")
            exclude_git = input("Exclude .git folder? (y/n): ").strip().lower() == "y"
            structure = get_folder_structure(root_directory, exclude_git=exclude_git)
            save_to_json(structure, output_folder, output_file)
            print(f"Folder structure saved to {os.path.join(output_folder, output_file)}")
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")