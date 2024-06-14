# split-json-to-md
Splits a json file into a folder of md files. Useful for Astro content collections.

split_json_to_md.py

Version: 1.2

By Ashwin Philips - Emergent Solutions

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
