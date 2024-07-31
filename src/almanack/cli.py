import fire
from almanack.report import repo_entropy_report

def repo_entropy(repo_path: str) -> None:
    """
    Prints the entropy report for the given repository.

    Args:
        repo_path (str): The path to the repository.
    """
    report = repo_entropy_report(repo_path)
    print(report)

if __name__ == "__main__":
    fire.Fire(repo_entropy)