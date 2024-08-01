"""
This module assists with data processing the almanack package.
"""

import json


def save_data_to_json(data: dict, output_path: str) -> None:
    """
    Saves the provided data to a JSON file.

    Args:
        data (dict): The data to be saved in JSON format.
        output_path (str): Path to the output JSON file.
    """
    # Open the output file in write mode and save the data as JSON
    with open(output_path, "w") as json_file:
        # Write the data to the file with an indentation of 4 spaces for readability
        json.dump(data, json_file, indent=4)