import subprocess
import json
import pathlib
from almanack.reporting.cli import process_repo_entropy
import pytest

# def test_process_repo_entropy(
#     repository_paths: dict[str, pathlib.Path], repo_file_sets: dict[str, list[str]]
# ) -> None:
#     """
#     Test that the CLI function produces the expected output for given repositories.
#     """
#     for label, repo_path in repository_paths.items():
#         # Call the CLI function directly
#         json_string, report_content = process_repo_entropy(str(repo_path))

#         # Ensure the output contains expected content
#         assert "Repository Path" in report_content
#         assert f"Repository Path: {str(repo_path)}" in report_content
#         assert "Total Repository Normalized Entropy" in report_content

#         # Optionally, you can also validate the JSON output
#         entropy_data = json.loads(json_string)
#         assert isinstance(entropy_data, dict)
#         assert "total_normalized_entropy" in entropy_data

def test_process_repo_entropy(repository_paths: dict[str, pathlib.Path]) -> None:
    """
    Test that the CLI function `process_repo_entropy` produces the expected JSON output for given repositories.
    """
    for label, repo_path in repository_paths.items():
        # Call the CLI function directly
        json_string = process_repo_entropy(str(repo_path))
        
        # Check that the JSON string is not empty
        assert json_string.strip() != ""  
        # Load the JSON string into a dictionary
        entropy_data = json.loads(json_string)
        # Check for expected keys in the JSON output
        expected_keys = ['repo_path', 'total_normalized_entropy']
        for key in expected_keys:
            assert key in entropy_data, f"Missing key {key} in JSON output for {label}"


