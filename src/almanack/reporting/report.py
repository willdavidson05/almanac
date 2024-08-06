"""
This module creates entropy reports
"""

import json
import pathlib
from typing import Dict

from almanack.processing.processing_repositories import process_entire_repo


def process_repo_entropy(repo_path: str) -> None:
    """
    CLI entry point to process a repository for calculating entropy changes between commits and
    generate a report.

    Args:
        repo_path (str): The local path to the Git repository.
    """

    repo_path = pathlib.Path(repo_path)

    # Check if the directory contains a Git repository
    if not repo_path.exists() or not (repo_path / ".git").exists():
        raise FileNotFoundError(f"The directory {repo_path} is not a repository")

    # Process the repository and get the dictionary
    entropy_data = process_entire_repo(str(repo_path))

    # Generate and print the report from the dictionary
    report_content = repo_entropy_report(entropy_data)

    # Convert the dictionary to a JSON string
    json_string = json.dumps(entropy_data, indent=4)

    print(report_content)

    # Return the JSON string and report content
    return json_string


def repo_entropy_report(data: Dict[str, any]) -> str:
    """
    Returns the formatted entropy report as a string.

    Args:
        data (Dict[str, any]): Dictionary with the entropy data.

    Returns:
        str: Formatted entropy report.
    """

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
    return report_content
