"""
Testing repository_processing functionality
"""

import pathlib
import shutil
import tempfile

from almanack.repository_processing import process_entire_repo


def test_process_entire_repo(repository_paths: dict[str, pathlib.Path]) -> None:
    """
    Test process_entire_repo function.
    """
    # Define the relative path for the output file
    relative_output_path = "src/almanack/entropy_report.json"

    # Resolve the absolute path for the output file relative to the project root
    output_path = pathlib.Path(__file__).parent.parent / relative_output_path

    for _, repo_path in repository_paths.items():
        # Create a temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Set up a path for the temporary repository
            temp_repo_path = pathlib.Path(temp_dir) / "repo"
            # Copy the contents of the original repository to the temporary directory
            shutil.copytree(repo_path, temp_repo_path)

            # Ensure the output directory exists
            output_dir = output_path.parent
            output_dir.mkdir(parents=True, exist_ok=True)

            # Call the function with the temporary repository path and output path
            process_entire_repo(temp_repo_path, str(output_path))

            # Check if the output file was created
            assert output_path.exists()
