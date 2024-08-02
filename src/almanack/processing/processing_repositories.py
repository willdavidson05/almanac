"""
This module processes GitHub repositories
"""

import pathlib
import shutil
import tempfile
from datetime import datetime, timezone
from typing import Optional, Tuple

import pygit2

from .calculate_entropy import calculate_aggregate_entropy
from .git_operations import clone_repository, get_commits, get_edited_files


def process_entire_repo(repo_path: str) -> None:
    """
    Processes a repository path to calculate entropy.

    Args:
        repo_path (str): The local path to the Git repository.

    Returns:
        Dict: Key Value pair containing repository path and normalized entropy
    """
    try:
        # Convert repo_path to an absolute path and initialize the repository
        repo_path = pathlib.Path(repo_path).resolve()
        repo = pygit2.Repository(str(repo_path))

        # Retrieve the list of commits from the repository
        commits = get_commits(repo)
        most_recent_commit = commits[0]
        first_commit = commits[-1]

        # Get a list of files that have been edited between the first and most recent commit
        file_names = get_edited_files(repo, first_commit, most_recent_commit)

        # Calculate the normalized total entropy for the repository
        normalized_total_entropy = calculate_aggregate_entropy(
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

        return data

    except Exception as e:
        # If processing fails, return an error dictionary
        error_data = {"repo_path": str(repo_path), "error": str(e)}
        return error_data


def process_repo_for_analysis(
    repo_url: str,
) -> Tuple[Optional[float], Optional[str], Optional[str], Optional[int]]:
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
        # Load the cloned repo
        repo = pygit2.Repository(str(repo_path))

        # Retrieve the list of commits from the repo
        commits = get_commits(repo)
        # Select the first and most recent commits from the list
        first_commit = commits[-1]
        most_recent_commit = commits[0]

        # Calculate the time span of existence between the first and most recent commits in days
        time_of_existence = (
            most_recent_commit.commit_time - first_commit.commit_time
        ) // (24 * 3600)
        # Calculate the time span between commits in days. Using UTC for date conversion ensures uniformity
        # and avoids issues related to different time zones and daylight saving changes.
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
        # Get a list of all files that have been edited between the commits
        file_names = get_edited_files(repo, commits)
        # Calculate the normalized entropy for the changes between the first and most recent commits
        normalized_total_entropy = calculate_aggregate_entropy(
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
