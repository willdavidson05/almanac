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
    data = {
        "repo_path": repo_path,
        "total_normalized_entropy": normalized_total_entropy,
    }

    with open(output_path, "w") as json_file:
        json.dump(data, json_file, indent=4)
