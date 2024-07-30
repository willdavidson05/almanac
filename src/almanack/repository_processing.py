"""
This module processes GitHub repositories
"""

import shutil
import tempfile
from datetime import datetime, timezone

import pygit2

from .data_management import print_entropy_report, save_entropy_to_json
from .entropy import aggregate_entropy_calculation, calculate_normalized_entropy
from .git_operations import clone_repository, get_commits, get_edited_files


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
