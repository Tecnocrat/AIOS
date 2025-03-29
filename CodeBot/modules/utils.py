import os

def sanitize_input(user_input):
    """
    Strips whitespace and converts input to lowercase.
    """
    return user_input.strip().lower()


def get_valid_file_path(prompt="Enter file path: "):
    """
    Prompts the user for a file path and validates its existence.
    """
    while True:
        file_path = input(prompt).strip()
        if os.path.exists(file_path):
            return file_path
        print("Invalid file path. Please try again.")


def handle_exception(logger, error_message, exception):
    """
    Logs an error and returns a user-friendly error message.
    """
    logger.error(f"{error_message}: {exception}")
    return error_message