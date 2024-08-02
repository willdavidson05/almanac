"""
Testing repository_processing functionality
"""

import pathlib
import shutil
import tempfile

from almanack.processing.repository_processing import process_entire_repo
from almanack.reporting.report import repo_entropy_report


def test_process_entire_repo(repository_paths: dict[str, pathlib.Path]) -> None:
    """
    Test process_entire_repo function.
    """
    for _, repo_path in repository_paths.items():
        # Create a temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Set up a path for the temporary repository
            temp_repo_path = pathlib.Path(temp_dir) / "repo"
            # Copy the contents of the original repository to the temporary directory
            shutil.copytree(repo_path, temp_repo_path)

            # Call the function with the temporary repository path
            entropy_data = process_entire_repo(str(temp_repo_path))

            # Check if the entropy data is not empty
            assert entropy_data

            # Call the function to print the entropy report from the JSON string
            repo_entropy_report(entropy_data)
