
import json
from typing import Dict
import json
from typing import Dict

def repo_entropy_report(output_path: str) -> None:
    """
    Prints the entropy values from a JSON file.

    Args:
        output_path (str): Path to the output JSON file.
    """
    with open(output_path, "r") as json_file:
        data = json.load(json_file)

    border = "=" * 50
    separator = "-" * 50
    title = "Entropy Report"

    print(border)
    print(f"{title:^50}")  # Centers the title
    print(border)

    # Print repository details
    print(f"Repository Path: {data['repo_path']}")
    print(f"Total Repository Normalized Entropy: {data['total_normalized_entropy']:.4f}")
    
    print(separator)

    # Print the report footer
    print(border)
