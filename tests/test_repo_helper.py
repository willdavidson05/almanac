from almanack.repo_helper import process_repository


def test_repo_helper():
    output_path = "/home/willdavidson/Desktop/Almanack/almanac/tests/entropy_report.json"
    process_repository("https://github.com/software-gardening/almanack", output_path)