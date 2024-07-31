"""
This module prccesess data
"""

import json


def save_entropy_to_json(
    repo_path: str,
    normalized_total_entropy: float,
    output_path: str,
) -> None:
    """
    Saves the entropy values to a JSON file.

    Args:
        repo_path (str): The path of the repository.
        normalized_total_entropy (float): Total normalized entropy for the repository.
        output_path (str): Path to the output JSON file.
    """
    # Create a dictionary to hold the data to be saved
    data = {
        "repo_path": repo_path,
        "total_normalized_entropy": normalized_total_entropy,
    }
    # Open the output file in write mode and save the data as JSON
    with open(output_path, "w") as json_file:
        # Write the data to the file with an indentation of 4 spaces for readability
        json.dump(data, json_file, indent=4)
