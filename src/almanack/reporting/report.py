"""
This module creates entropy reports
"""

import json


def repo_entropy_report(output_path: str) -> None:
    """
    Prints the entropy values from a JSON file.

    Args:
        output_path (str): Path to the output JSON file.
    """
    # Read .JSON file
    with open(output_path, "r") as json_file:
        data = json.load(json_file)

    border = "=" * 50
    separator = "-" * 50
    title = "Entropy Report"

    # Format the report
    report_content = f"""
    {border}
    {title:^50}
    {border}
    Repository Path: {data['repo_path']}
    Total Repository Normalized Entropy: {data['total_normalized_entropy']:.4f}
    {separator}
    {border}
    """
    print(report_content)
