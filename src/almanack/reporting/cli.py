"""
Setup process_repo_entropy CLI through python-fire
"""

import json
import pathlib

import fire

from almanack.processing.repository_processing import process_entire_repo
from almanack.reporting.report import repo_entropy_report


def process_repo_entropy(repo_path: str) -> None:
    """
    CLI entry point to process a repository for calculating entropy changes between commits and
    generate a report. The results are output to a .JSON file.

    Args:
        repo_path (str): The local path to the Git repository.
        output_path (str, optional): Path to the output JSON file. Default is "repo_entropy_report.json".
    """

    repo_path = pathlib.Path(repo_path).resolve()

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
    return json_string, report_content


if __name__ == "__main__":
    """
    Setup the CLI with python-fire for the almanack package.

    This allows the function `process_repo_entropy` to be ran through the
    command line interface.
    """
    fire.Fire(process_repo_entropy)
