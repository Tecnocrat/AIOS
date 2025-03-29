import os
import json

def analyze_folder_structure(base_dir, max_depth=10, current_depth=0):
    if current_depth > max_depth:
        return {"error": "Max depth exceeded"}

    structure = {}
    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        if os.path.isdir(item_path):
            structure[item] = analyze_folder_structure(item_path, max_depth, current_depth + 1)
        else:
            structure[item] = "file"
    return structure

def save_structure_to_json(base_dir, output_dir):
    folder_name = os.path.basename(base_dir)
    output_file = os.path.join(output_dir, f"folder_{folder_name}_structure.json")
    structure = analyze_folder_structure(base_dir)
    with open(output_file, "w") as f:
        json.dump(structure, f, indent=4)
    print(f"Folder structure saved to {output_file}")

if __name__ == "__main__":
    base_dir = input("Enter the folder to analyze (e.g., C:\\dev): ").strip()
    output_dir = os.path.join("c:\\dev\\CodeBot", "storage")
    os.makedirs(output_dir, exist_ok=True)
    save_structure_to_json(base_dir, output_dir)