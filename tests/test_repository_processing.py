"""
Testing repository_processing functionality
"""

from almanack.repository_processing import process_entire_repo
import pathlib
import tempfile
import shutil

def test_repo_helper(repository_paths: dict[str, pathlib.Path]) -> None:
    """
    Test process_entire_repo function.
    """
    output_path = "/home/willdavidson/Desktop/Almanack/almanac/tests/entropy_report.json"

    for label, repo_path in repository_paths.items():
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_repo_path = pathlib.Path(temp_dir) / "repo"
            shutil.copytree(repo_path, temp_repo_path)
            process_entire_repo(temp_repo_path, output_path)