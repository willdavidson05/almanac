"""
Testing repo_helper functionality
"""

from almanack.repository_processing import process_repository

def test_repo_helper() -> None:
    """
    Test process_repository function.
    """
    output_path = (
        "/home/willdavidson/Desktop/Almanack/almanac/tests/entropy_report.json"
    )
    process_repository("https://github.com/software-gardening/almanack", output_path)
