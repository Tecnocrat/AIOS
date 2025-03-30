import os


def get_valid_file_path(prompt="Enter file path: "):
    """
    Prompts the user for a file path and validates its existence.
    """
    while True:
        file_path = input(prompt).strip()
        if os.path.exists(file_path):
            return file_path
        print("Invalid file path. Please try again.")