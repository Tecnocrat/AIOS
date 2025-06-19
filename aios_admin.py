import os
import json
import shutil
from datetime import datetime

MODULE_INDEX_PATH = r"C:\dev\AIOS\docs\module_index.json"
SUMMARY_DIR = r"C:\dev\AIOS\docs\summary"
SUMMARY_MD_PATH = os.path.join(SUMMARY_DIR, "module_summaries.md")
MANUAL_SUMMARY_PATH = os.path.join(SUMMARY_DIR, "module_summaries_input.txt")
TACHYONIC_DIR = r"C:\dev\AIOS\docs\tachyonic"

def get_folder_structure(root_dir, exclude_git=False):
    folder_structure = {}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if exclude_git and ".git" in dirpath:
            continue
        relative_path = os.path.relpath(dirpath, root_dir)
        if relative_path == ".":
            relative_path = ""
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
    print("=== AIOS Admin Tool ===")
    print("Choose an option:")
    print("1. Analyze Architect folder structure")
    print("2. Analyze chatgpt folder structure")
    print("3. Analyze AIOS folder structure")
    print("4. Tachyonic backup of path.md")
    print("5. Create/Update module summaries (from input file or interactively)")
    print("6. Exit")
    choice = input("Enter your choice (1/2/3/4/5/6): ").strip()
    return choice

def tachyonic_backup(
    path_md=r"C:\dev\AIOS\docs\path.md",
    archive_dir=TACHYONIC_DIR
):
    os.makedirs(archive_dir, exist_ok=True)
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{archive_dir}\\path_{now}.md"
    shutil.copy2(path_md, backup_path)
    print(f"Tachyonic backup created: {backup_path}")

def load_module_index(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_manual_summaries(input_path):
    summaries = {}
    if not os.path.exists(input_path):
        return summaries
    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("|", 2)
            if len(parts) == 3:
                module_path, lang, summary = parts
                summaries[(module_path.strip(), lang.strip())] = summary.strip()
    return summaries

def collect_summaries(module_index, manual_summaries, path_stack=None, summaries=None):
    if summaries is None:
        summaries = []
    if path_stack is None:
        path_stack = []
    for key, value in module_index.items():
        if isinstance(value, dict):
            collect_summaries(value, manual_summaries, path_stack + [key], summaries)
        else:
            module_path = "/".join(path_stack + [key])
            lang = value
            summary = manual_summaries.get((module_path, lang), "")
            if not summary:
                print(f"Module: {module_path} ({lang})")
                summary = input(f"Enter summary for {module_path}: ")
            summaries.append(f"### {module_path} ({lang})\n{summary}\n")
    return summaries

def write_summaries(summaries, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(summaries))
    print(f"Module summaries written to {path}")

if __name__ == "__main__":
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
            tachyonic_backup()
        elif choice == "5":
            if not os.path.exists(MODULE_INDEX_PATH):
                print(f"ERROR: {MODULE_INDEX_PATH} not found.")
                continue
            module_index = load_module_index(MODULE_INDEX_PATH)
            manual_summaries = load_manual_summaries(MANUAL_SUMMARY_PATH)
            summaries = collect_summaries(module_index, manual_summaries)
            write_summaries(summaries, SUMMARY_MD_PATH)
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")