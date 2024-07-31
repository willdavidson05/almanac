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
    # Define a relative path for the output file
    relative_output_path = "src/almanack/entropy_report.json"
    output_path = pathlib.Path(__file__).parent / relative_output_path

    for _, repo_path in repository_paths.items():
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_repo_path = pathlib.Path(temp_dir) / "repo"
            shutil.copytree(repo_path, temp_repo_path)

            # Ensure the directory exists before running the function
            output_dir = output_path.parent
            output_dir.mkdir(parents=True, exist_ok=True)

            process_entire_repo(temp_repo_path, output_path)

            # Check if the output file was created
            assert output_path.exists()
