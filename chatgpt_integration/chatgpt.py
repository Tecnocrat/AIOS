import os
import json
import csv
import xml.etree.ElementTree as ET
import shutil
from datetime import datetime

def move_to_archive(output_folder):
    archive_folder = os.path.join(output_folder, 'archive')
    os.makedirs(archive_folder, exist_ok=True)

    for file_name in os.listdir(output_folder):
        if file_name != 'archive':
            file_path = os.path.join(output_folder, file_name)
            archive_path = os.path.join(archive_folder, file_name)

            if os.path.exists(archive_path):
                file_type = file_name.split('.')[-1]
                type_folder = os.path.join(archive_folder, file_type)
                os.makedirs(type_folder, exist_ok=True)

                type_file_path = os.path.join(type_folder, file_name)
                if os.path.exists(type_file_path):
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    new_file_name = f"{file_name.split('.')[0]}_{timestamp}.{file_type}"
                    shutil.move(file_path, os.path.join(type_folder, new_file_name))
                else:
                    shutil.move(file_path, type_file_path)
            else:
                shutil.move(file_path, archive_path)

def convert_md_to_formats(md_file_path, output_folder):
    if os.listdir(output_folder):
        move_to_archive(output_folder)

    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        content = md_file.read()

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Convert to .txt
    with open(os.path.join(output_folder, os.path.basename(md_file_path).replace('.md', '.txt')), 'w', encoding='utf-8') as txt_file:
        txt_file.write(content)

    # Convert to .csv
    csv_content = "Title,Description\n" + content.replace('\n', '\n')
    with open(os.path.join(output_folder, os.path.basename(md_file_path).replace('.md', '.csv')), 'w', encoding='utf-8') as csv_file:
        csv_file.write(csv_content)

    # Convert to .json
    json_content = {"content": content}
    with open(os.path.join(output_folder, os.path.basename(md_file_path).replace('.md', '.json')), 'w', encoding='utf-8') as json_file:
        json.dump(json_content, json_file, indent=4)

    # Convert to .xml
    xml_content = f"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<document>\n<content>{content}</content>\n</document>"
    with open(os.path.join(output_folder, os.path.basename(md_file_path).replace('.md', '.xml')), 'w', encoding='utf-8') as xml_file:
        xml_file.write(xml_content)

def process_md_files(input_folder, output_folder):
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.md'):
            convert_md_to_formats(os.path.join(input_folder, file_name), output_folder)

def create_vscopilot_iteration():
    vscopilot_path = 'md/vscopilot.md'
    vscopilot_ark_path = 'md/vscopilot_ark.md'

    # Ensure vscopilot.md exists
    if not os.path.exists(vscopilot_path):
        print("vscopilot.md does not exist.")
        return

    # Read contents of vscopilot.md
    with open(vscopilot_path, 'r', encoding='utf-8') as vscopilot_file:
        vscopilot_content = vscopilot_file.read()

    # Append contents to vscopilot_ark.md
    with open(vscopilot_ark_path, 'a', encoding='utf-8') as vscopilot_ark_file:
        vscopilot_ark_file.write(f"\n--- Iteration {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
        vscopilot_ark_file.write(vscopilot_content)

    # Clear vscopilot.md for next iteration
    with open(vscopilot_path, 'w', encoding='utf-8') as vscopilot_file:
        vscopilot_file.write("")

def create_engine_iteration(engine_name):
    engine_path = f'md/{engine_name}.md'
    ark_folder = 'md/ark'
    os.makedirs(ark_folder, exist_ok=True)
    engine_ark_path = f'{ark_folder}/{engine_name}_ark.md'

    # Ensure engine.md exists
    if not os.path.exists(engine_path):
        print(f"{engine_name}.md does not exist.")
        return

    # Read contents of engine.md
    with open(engine_path, 'r', encoding='utf-8') as engine_file:
        engine_content = engine_file.read()

    # Append contents to engine_ark.md
    with open(engine_ark_path, 'a', encoding='utf-8') as engine_ark_file:
        engine_ark_file.write(f"\n--- Iteration {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
        engine_ark_file.write(engine_content)

    # Clear engine.md for next iteration
    with open(engine_path, 'w', encoding='utf-8') as engine_file:
        engine_file.write("")

def engines_submenu():
    print("Choose an engine:")
    print("1. chatgpt")
    print("2. copilot")
    print("3. gemini")
    print("4. vscopilot")
    engine_choice = input("Enter your choice: ")

    engine_map = {
        "1": "chatgpt",
        "2": "copilot",
        "3": "gemini",
        "4": "vscopilot"
    }

    if engine_choice in engine_map:
        create_engine_iteration(engine_map[engine_choice])
    else:
        print("Invalid choice.")

def main():
    print("Choose an option:")
    print("1. Create ingestion")
    print("2. Engines submenu")
    choice = input("Enter your choice: ")

    if choice == "1":
        process_md_files('md', 'ingestion')
    elif choice == "2":
        engines_submenu()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
