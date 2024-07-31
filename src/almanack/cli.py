
import fire

from almanack.report import repo_entropy_report
from almanack.repository_processing import process_entire_repo


def repo_entropy(repo_path: str, output_path: str) -> None:
    """
    CLI entry point to process a repository and generate an entropy report.

    Args:
        repo_path (str): The local path to the Git repository.
        output_path (str): Path to the output JSON file.
    """
    # Process the repository and generate the JSON file
    process_entire_repo(repo_path, output_path)

    # Generate and print the report
    repo_entropy_report(output_path)


if __name__ == "__main__":
    fire.Fire(repo_entropy)
