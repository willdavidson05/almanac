"""
This module processes GitHub repositories
"""

import pathlib
import shutil
import tempfile
from datetime import datetime, timezone

import pygit2

from .data_management import save_data_to_json
from .entropy import aggregate_entropy_calculation
from .git_operations import clone_repository, get_commits, get_edited_files


def process_entire_repo(repo_path: str, output_path: str) -> None:
    """
    Processes a repository path to calculate entropy.

    Args:
        repo_path (str): The local path to the Git repository.
        output_path (str): Path to the output JSON file.

    Returns:
        None: Saves the entropy data to a JSON file.
    """
    try:
        repo_path = pathlib.Path(repo_path).resolve()
        repo = pygit2.Repository(str(repo_path))

        commits = get_commits(repo)
        most_recent_commit = commits[0]
        first_commit = commits[-1]

        file_names = get_edited_files(repo, first_commit, most_recent_commit)

        normalized_total_entropy = aggregate_entropy_calculation(
            repo_path,
            str(first_commit.id),
            str(most_recent_commit.id),
            file_names,
        )

        # Prepare the data structure
        data = {
            "repo_path": str(repo_path),
            "total_normalized_entropy": normalized_total_entropy,
        }

        # Save the data to a JSON file
        save_data_to_json(data, output_path)

    except Exception as e:
        print(f"Error processing repository {repo_path}: {e}")


def process_repo_for_analysis(
    repo_url: str,
):
    """
    Processes GitHub repository URL's to calculate entropy and other metadata.
    This is used to prepare data for analysis, particularly for the seedbank notebook
    that process PUBMED repositories.

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
