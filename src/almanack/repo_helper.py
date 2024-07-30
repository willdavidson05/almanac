import json
import pathlib
import shutil
import tempfile
from datetime import datetime, timezone
from typing import Dict, List

import pygit2

from .entropy import (
    aggregate_entropy_calculation,
    calculate_normalized_entropy,
    get_edited_files,
)


def clone_repository(repo_url: str) -> pathlib.Path:
    """
    Clones the GitHub repository to a temporary directory.

    Args:
        repo_url (str): The URL of the GitHub repository.

    Returns:
        pathlib.Path: Path to the cloned repository.
    """
    temp_dir = tempfile.mkdtemp()
    repo_path = pathlib.Path(temp_dir) / "repo"
    pygit2.clone_repository(repo_url, str(repo_path))
    return repo_path


def get_commits(repo: pygit2.Repository) -> List[pygit2.Commit]:
    """
    Retrieves the list of commits from the main branch.

    Args:
        repo (pygit2.Repository): The Git repository.

    Returns:
        List[pygit2.Commit]: List of commits in the repository.
    """
    head = repo.revparse_single("HEAD")
    walker = repo.walk(
        head.id, pygit2.GIT_SORT_NONE
    )  # Use GIT_SORT_NONE to ensure all commits are included
    commits = [commit for commit in walker]

    return commits


def save_entropy_to_json(
    repo_url: str,
    file_level_entropy: Dict[str, float],
    normalized_total_entropy: float,
    output_path: str,
) -> None:
    """
    Saves the entropy values and the top 5 files with the most entropy to a JSON file.

    Args:
        repo_url (str): The URL of the GitHub repository.
        file_level_entropy (Dict[str, float]): Entropy values for each file.
        normalized_total_entropy (float): Total normalized entropy for the repository.
        output_path (str): Path to the output JSON file.
    """
    # Sort the files by entropy in descending order and get the top 5
    sorted_files_by_entropy = sorted(
        file_level_entropy.items(), key=lambda item: item[1], reverse=True
    )[:5]

    data = {
        "repo_url": repo_url,
        "total_normalized_entropy": normalized_total_entropy,
        "file_level_entropy": file_level_entropy,
        "5_files_with_most_entropy": sorted_files_by_entropy,
    }

    with open(output_path, "w") as json_file:
        json.dump(data, json_file, indent=4)


def print_entropy_report(output_path: str) -> None:
    """
    Prints the entropy values from a JSON file.

    Args:
        output_path (str): Path to the output JSON file.
    """
    with open(output_path, "r") as json_file:
        data = json.load(json_file)

    border = "=" * 50
    separator = "-" * 50
    title = "Entropy Report"

    print(border)
    print(f"{title:^50}")  # Centers the title
    print(border)

    # Print repository details
    print(f"Repository URL: {data['repo_url']}")
    print(f"Total Normalized Entropy: {data['total_normalized_entropy']:.4f}")

    # Print top 5 files with most entropy
    print("\nTop 5 Files with Most Entropy:")
    print(separator)
    for file_name, entropy in data["5_files_with_most_entropy"]:
        print(f"  {file_name:<40} {entropy:>8.4f}")
    print(separator)

    # Print the report footer
    print(border)


def process_repository(repo_url: str, output_path: str) -> None:
    """
    Processes a GitHub repository URL to calculate entropy and other metadata.

    Args:
        repo_url (str): The URL of the GitHub repository.
        output_path (str): Path to the output JSON file.

    Returns:
        None: Saves the entropy data to a JSON file and prints it.
    """
    temp_dir = tempfile.mkdtemp()
    try:
        repo_path = clone_repository(repo_url)
        repo = pygit2.Repository(str(repo_path))

        commits = get_commits(repo)
        most_recent_commit = commits[0]
        second_most_recent_commit = commits[1]

        file_names = get_edited_files(
            repo, second_most_recent_commit, most_recent_commit
        )

        normalized_total_entropy = aggregate_entropy_calculation(
            repo_path,
            str(second_most_recent_commit.id),
            str(most_recent_commit.id),
            file_names,
        )

        file_level_entropy = calculate_normalized_entropy(
            repo_path,
            str(second_most_recent_commit.id),
            str(most_recent_commit.id),
            file_names,
        )

        save_entropy_to_json(
            repo_url, file_level_entropy, normalized_total_entropy, output_path
        )
        print_entropy_report(output_path)

    except Exception as e:
        print(f"Error processing repository {repo_url}: {e}")

    finally:
        shutil.rmtree(temp_dir)


def process_repo_to_parquet(
    repo_url: str,
):  # Tuple[Union[float, None], Union[str, None], Union[str, None], Union[int, None]]
    """
    Processes a GitHub repository URL to calculate entropy and other metadata.

    Args:
        repo_url (str): The URL of the GitHub repository.

    Returns:
        tuple: A tuple containing the normalized total entropy, the date of the first commit,
               the date of the most recent commit, and the total time of existence in days.
    """
    temp_dir = tempfile.mkdtemp()
    try:
        repo_path = clone_repository(repo_url)
        repo = pygit2.Repository(str(repo_path))

        commits = get_commits(repo)

        first_commit = commits[-1]
        most_recent_commit = commits[0]

        time_of_existence = (
            most_recent_commit.commit_time - first_commit.commit_time
        ) // (24 * 3600)

        first_commit_date = (
            datetime.fromtimestamp(first_commit.commit_time, tz=timezone.utc)
            .date()
            .isoformat()
        )
        most_recent_commit_date = (
            datetime.fromtimestamp(most_recent_commit.commit_time, tz=timezone.utc)
            .date()
            .isoformat()
        )

        file_names = get_edited_files(repo, commits)

        normalized_total_entropy = aggregate_entropy_calculation(
            repo_path, str(first_commit.id), str(most_recent_commit.id), file_names
        )

        return (
            normalized_total_entropy,
            first_commit_date,
            most_recent_commit_date,
            time_of_existence,
        )

    except Exception:
        return None, None, None, None

    finally:
        shutil.rmtree(temp_dir)
