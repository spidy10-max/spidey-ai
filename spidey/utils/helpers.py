"""
Spidey AI — Helper Utilities
Common functions used across the project
"""
import os
import json
from datetime import datetime


def get_timestamp():
    """Get current timestamp as formatted string"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_date_string():
    """Get current date as string"""
    return datetime.now().strftime("%Y-%m-%d")


def format_file_size(size_bytes):
    """
    Convert bytes to human readable format

    Args:
        size_bytes: File size in bytes

    Returns:
        Formatted string like '2.5 KB' or '1.3 MB'
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{round(size_bytes / 1024, 1)} KB"
    else:
        return f"{round(size_bytes / (1024 * 1024), 1)} MB"


def safe_json_load(filepath, default=None):
    """
    Safely load JSON file with error handling

    Args:
        filepath: Path to JSON file
        default: Default value if file not found or invalid

    Returns:
        Parsed JSON data or default value
    """
    if default is None:
        default = {}

    try:
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError):
        pass

    return default


def safe_json_save(filepath, data):
    """
    Safely save data to JSON file

    Args:
        filepath: Path to save file
        data: Data to save

    Returns:
        True if saved successfully, False otherwise
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except (IOError, OSError) as e:
        print(f"Error saving file: {e}")
        return False


def truncate_text(text, max_length=50):
    """
    Truncate text to max length with ellipsis

    Args:
        text: Text to truncate
        max_length: Maximum length

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def count_files(directory, extension=None):
    """
    Count files in a directory

    Args:
        directory: Path to directory
        extension: Optional file extension filter (e.g., '.json')

    Returns:
        Number of files
    """
    if not os.path.exists(directory):
        return 0

    files = os.listdir(directory)
    if extension:
        files = [f for f in files if f.endswith(extension)]
    return len(files)


def clear_screen():
    """Clear terminal screen"""
    os.system("cls" if os.name == "nt" else "clear")


def print_separator(char="=", length=55):
    """Print a separator line"""
    print(char * length)


def print_header(title, char="=", length=55):
    """Print a formatted header"""
    print()
    print(char * length)
    print(f"   {title}")
    print(char * length)
