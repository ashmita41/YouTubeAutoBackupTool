"""
Utility functions for YouTube Auto Backup
"""

import os
import re
import unicodedata
import shutil
from datetime import datetime


def sanitize_filename(filename):
    """
    Replace invalid characters with an underscore
    
    Args:
        filename (str): The filename to sanitize
        
    Returns:
        str: Sanitized filename
    """
    return unicodedata.normalize('NFKD', re.sub(r'[<>:"/\\|?*]', '_', filename))


def format_filename(date, title, extension):
    """
    Format the filename with the given date, title, and extension.
    
    Args:
        date (datetime): The date to use
        title (str): The title of the video
        extension (str): The file extension
        
    Returns:
        str: Formatted filename
    """
    formatted_date = date.strftime("%d-%m-%Y")
    
    # Replace invalid characters with underscores or remove them
    safe_title = "".join(
        c if c.isalnum() or c in " _-" else "_" for c in title
    )
    
    # Construct the final filename
    return sanitize_filename(f"{formatted_date} - {safe_title}.{extension}")


def delete_https_subfolders(folder_path):
    """
    Scan the given folder and delete any subfolder starting with 'https'.

    Args:
        folder_path (str): Path to the folder to scan.
    """
    try:
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for dir_name in dirs:
                if dir_name.startswith("https"):
                    dir_path = os.path.join(root, dir_name)
                    print(f"Deleting folder: {dir_path}")
                    try:
                        shutil.rmtree(dir_path)
                    except OSError as e:
                        print(f"Error deleting folder {dir_path}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def write_to_csv(file_path, channel_name, title, url):
    """
    Write video data to CSV file
    
    Args:
        file_path (str): Path to the CSV file
        channel_name (str): Name of the channel
        title (str): Video title
        url (str): Video URL
    """
    import csv
    
    # Check if the file exists
    file_exists = os.path.exists(file_path)
    
    # Open the file in append mode
    with open(file_path, mode='a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        
        # Write header if file doesn't exist
        if not file_exists:
            writer.writerow(["Channel Name", "Video Title", "Video URL"])
        
        # Write the row data
        writer.writerow([channel_name, title, url]) 