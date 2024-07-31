import pathlib

import fire

from almanack.report import repo_entropy_report
from almanack.repository_processing import process_entire_repo


def repo_entropy(repo_path: str, output_path: str = "entropy_report.json") -> None:
    """
    CLI entry point to process a repository and generate an entropy report.

    Args:
        repo_path (str | None, optional): The local path to the Git repository. Defaults to None, which uses the current working directory.
        output_path (str, optional): Path to the output JSON file. Defaults to "entropy_report.json".
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


if __name__ == "__main__":
    fire.Fire(repo_entropy)
