"""
Setup process_repo_entropy CLI through python-fire
"""

import pathlib

import fire

from almanack.reporting.report import repo_entropy_report
from almanack.processing.repository_processing import process_entire_repo


def process_repo_entropy(
    repo_path: str, output_path: str = "entropy_report.json"
) -> None:
    """
    CLI entry point to process a repository and generate an entropy report based on the change
    between commits. The results are output to a .JSON file

    Args:
        repo_path (str): The local path to the Git repository.
        output_path (str, optional): Path to the output JSON file. Default is "repo_entropy_report.json".
    """

    repo_path = pathlib.Path(repo_path).resolve()

    # Check if the directory contains a Git repository
    if not repo_path.exists() or not (repo_path / ".git").exists():
        raise FileNotFoundError(f"The directory {repo_path} is not a repository")

    # Process the repository and generate the JSON file
    process_entire_repo(str(repo_path), output_path)

    # Generate and return the report
    repo_entropy_report(output_path)

    # Return the path to the generated JSON report file
    return output_path


if __name__ == "__main__":
    """
    Setup the CLI with python-fire for the almanack package.

    This allows the function `process_repo_entropy` to be ran through the
    command line interface.
    """
    fire.Fire(process_repo_entropy)
