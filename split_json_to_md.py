"""
split_json_to_md.py
Version: 1.2
By Ashwin Philips
Date: 2024-06-13
Time: 16:00:00

This script processes a JSON file containing an array of objects and splits each object into separate .md files.
If no specific JSON file is specified at runtime, it processes all JSON files in the directory from which it is run.
Each generated .md file contains frontmatter with the object's fields. If the script is not called from a directory
that matches the JSON file name, it creates a directory with the same name as the JSON file (without .json) and 
places the .md files inside it.

Usage:
    python split_json_to_md.py [optional_path/to/data.json]

    - If a specific JSON file path is provided, the script processes that file.
    - If no file path is provided, the script processes all JSON files in the current directory.

"""

import os
import json
import re
import sys
from glob import glob

# Function to create a valid filename from a given string
def make_valid_filename(name):
    """
    Create a valid filename from a given string by replacing spaces with underscores
    and removing invalid characters.

    Args:
        name (str): The string to convert into a filename.

    Returns:
        str: A valid filename.
    """
    return re.sub(r'[^a-zA-Z0-9_]', '', name.replace(' ', '_'))

# Function to split a JSON file into separate .md files
def split_json_file(json_file_path):
    """
    Split a JSON file into separate .md files based on the array of objects.

    Args:
        json_file_path (str): Path to the JSON file to process.
    """
    # Load the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Print the type and structure of the data for diagnostics
    print(f"Data type: {type(data)}")
    print(f"Data: {data}")

    # Ensure the JSON data is a list of dictionaries
    if not isinstance(data, list):
        # Check if the data contains a key that holds the list of objects
        if isinstance(data, dict):
            keys = list(data.keys())
            print(f"Top-level keys in the JSON: {keys}")
            # Check if any of the keys contain a list of dictionaries
            for key in keys:
                if isinstance(data[key], list) and all(isinstance(item, dict) for item in data[key]):
                    data = data[key]
                    break
            else:
                raise ValueError(f"The JSON file {json_file_path} does not contain an array of objects.")
        else:
            raise ValueError(f"The JSON file {json_file_path} does not contain an array of objects.")

    for entry in data:
        if not isinstance(entry, dict):
            raise ValueError(f"An entry in the JSON file {json_file_path} is not an object.")

    # Determine output directory
    json_file_name = os.path.splitext(os.path.basename(json_file_path))[0]
    current_dir_name = os.path.basename(os.getcwd())

    if current_dir_name != json_file_name:
        output_dir = json_file_name
        os.makedirs(output_dir, exist_ok=True)
    else:
        output_dir = "."

    # Split the JSON into separate .md files
    for i, entry in enumerate(data):
        # Use the "title" field for the filename if it exists, otherwise use a generic name
        title = entry.get('title', f"entry_{i+1}")
        file_name = f"{make_valid_filename(title)}.md"
        file_path = os.path.join(output_dir, file_name)
        
        # Create the content for the .md file with frontmatter
        content = "---\n"
        for key, value in entry.items():
            if isinstance(value, list):
                content += f"{key}:\n"
                for item in value:
                    content += f"  - \"{item}\"\n"
            else:
                content += f"{key}: \"{value}\"\n"
        content += "---\n"
        
        # Write the content to the .md file
        with open(file_path, 'w') as md_file:
            md_file.write(content)

    print(f"Processed {len(data)} entries from {json_file_path} into .md files in the directory: {output_dir}")

# Main function to process files
def main():
    """
    Main function to process JSON files. Processes a specific file if provided,
    or all JSON files in the current directory if no specific file is mentioned.
    """
    # Check if a specific JSON file was passed as an argument
    if len(sys.argv) > 1:
        json_file_path = sys.argv[1]
        split_json_file(json_file_path)
    else:
        # Process all JSON files in the current directory
        json_files = glob('*.json')
        for json_file_path in json_files:
            split_json_file(json_file_path)

if __name__ == "__main__":
    main()
