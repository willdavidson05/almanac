"""
Setup repo_entropy CLI through python-fire
"""

import pathlib

import fire

from almanack.report import repo_entropy_report
from almanack.repository_processing import process_entire_repo


def repo_entropy(repo_path: str, output_path: str = "entropy_report.json") -> None:
    """
    CLI entry point to process a repository and generate an entropy report.

    Args:
        repo_path (str): The local path to the Git repository.
        output_path (str, optional): Path to the output JSON file.Currently is "entropy_report.json".
    """

    repo_path = pathlib.Path.cwd()  # Use the current working directory

    repo_path = pathlib.Path(repo_path).resolve()

    # Check if the directory contains a Git repository
    if not repo_path.exists() or not (repo_path / ".git").exists():
        raise FileNotFoundError

    # Process the repository and generate the JSON file
    process_entire_repo(str(repo_path), output_path)

    # Generate and print the report
    repo_entropy_report(output_path)

    # Delete the JSON file after the report is generated and printed
    json_path = pathlib.Path(output_path)
    if json_path.exists():
        json_path.unlink()  # Remove the file


if __name__ == "__main__":
    fire.Fire(repo_entropy)
