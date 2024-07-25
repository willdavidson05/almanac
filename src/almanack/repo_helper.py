"""
This module processes Git repositories
"""

import pathlib
import shutil
import tempfile
from datetime import datetime, timezone
from typing import Dict, List, Union

import pygit2

from .entropy import calculate_normalized_entropy, aggregate_entropy_calculation


# def process_repository(repo_url: str) -> (float, str, str, int):  # type: ignore
#     """
#     Processes a GitHub repository URL to calculate entropy and other metadata.

#     Args:
#         repo_url (str): The URL of the GitHub repository.

#     Returns:
#         tuple: A tuple containing the normalized total entropy, the date of the first commit,
#                the date of the most recent commit, and the total time of existence in days.

#     """
#     temp_dir = tempfile.mkdtemp()
#     try:
#         # Clone the repository into the temporary directory
#         repo_path = pathlib.Path(temp_dir) / "repo"
#         pygit2.clone_repository(repo_url, str(repo_path))

#         repo = pygit2.Repository(str(repo_path))

#         # Get the list of commits on the main branch
#         head = repo.revparse_single("HEAD")
#         walker = repo.walk(
#             head.id, pygit2.GIT_SORT_NONE
#         )  # Use GIT_SORT_NONE to ensure all commits are included
#         commits = [commit for commit in walker]

#         # Get the first and most recent commits
#         first_commit = commits[-1]
#         most_recent_commit = commits[0]

#         # Calculate the total existence time of the repository in days
#         time_of_existence = (
#             most_recent_commit.commit_time - first_commit.commit_time
#         ) // (24 * 3600)

#         # Find the dates of the first and most recent commits
#         first_commit_date = (
#             datetime.fromtimestamp(first_commit.commit_time, tz=timezone.utc)
#             .date()
#             .isoformat()
#         )
#         most_recent_commit_date = (
#             datetime.fromtimestamp(most_recent_commit.commit_time, tz=timezone.utc)
#             .date()
#             .isoformat()
#         )

#         # Find all files that have been edited in the repository
#         file_names = set()
#         for commit in commits:
#             if commit.parents:
#                 # Get the parent commit to calculate the diff
#                 parent = commit.parents[0]
#                 # Generate the diff between the current commit and its parent
#                 diff = repo.diff(parent, commit)
#                 # Iterate over each file change (patch) in the diff
#                 for patch in diff:
#                     # Add the old file path to the set if it exists
#                     if patch.delta.old_file.path:
#                         file_names.add(patch.delta.old_file.path)
#                     # Add the new file path to the set if it exists
#                     if patch.delta.new_file.path:
#                         file_names.add(patch.delta.new_file.path)
#         file_names = list(file_names)

#         # Calculate the total normalized entropy for the repository
#         normalized_total_entropy = aggregate_entropy_calculation(
#             repo_path, str(first_commit.id), str(most_recent_commit.id), file_names
#         )

#         return (
#             normalized_total_entropy,
#             first_commit_date,
#             most_recent_commit_date,
#             time_of_existence,
#         )

#     except Exception:
#         # Handle any exceptions by appending a row with None values
#         return None, None, None, None

#     finally:
#         # Clean up temp directory
#         shutil.rmtree(temp_dir)

"""
This module processes Git repositories
"""

import pathlib
import shutil
import tempfile
from datetime import datetime, timezone
from typing import Dict, List, Union

import pygit2

from .entropy import calculate_normalized_entropy, aggregate_entropy_calculation


def process_repository(repo_url: str) -> None:
    """
    Processes a GitHub repository URL to calculate entropy and other metadata.

    Args:
        repo_url (str): The URL of the GitHub repository.

    Returns:
        None: Prints the normalized total entropy for the repository and entropy values for each file.
    """
    temp_dir = tempfile.mkdtemp()
    try:
        # Clone the repository into the temporary directory
        repo_path = pathlib.Path(temp_dir) / "repo"
        pygit2.clone_repository(repo_url, str(repo_path))

        repo = pygit2.Repository(str(repo_path))

        # Get the list of commits on the main branch
        head = repo.revparse_single("HEAD")
        walker = repo.walk(
            head.id, pygit2.GIT_SORT_NONE
        )  # Use GIT_SORT_NONE to ensure all commits are included
        commits = [commit for commit in walker]

        if len(commits) < 2:
            raise ValueError("Repository does not have enough commits to compare.")

        # Get the most recent and second most recent commits
        most_recent_commit = commits[0]
        second_most_recent_commit = commits[-1]

        # Find all files that have been edited in the repository
        file_names = set()
        for commit in commits:
            if commit.parents:
                # Get the parent commit to calculate the diff
                parent = commit.parents[0]
                # Generate the diff between the current commit and its parent
                diff = repo.diff(parent, commit)
                # Iterate over each file change (patch) in the diff
                for patch in diff:
                    # Add the old file path to the set if it exists
                    if patch.delta.old_file.path:
                        file_names.add(patch.delta.old_file.path)
                    # Add the new file path to the set if it exists
                    if patch.delta.new_file.path:
                        file_names.add(patch.delta.new_file.path)
        file_names = list(file_names)

        # Calculate the total normalized entropy for the repository
        normalized_total_entropy = aggregate_entropy_calculation(
            repo_path, str(second_most_recent_commit.id), str(most_recent_commit.id), file_names
        )

        # Calculate the entropy for each file
        file_level_entropy = calculate_normalized_entropy(
            repo_path, str(second_most_recent_commit.id), str(most_recent_commit.id), file_names
        )

        # Print the entropy values
        print(f"Repository URL: {repo_url}")
        print(f"Total Normalized Entropy: {normalized_total_entropy:.4f}")
        print("File Level Entropy:")
        for file_name, entropy in file_level_entropy.items():
            print(f"  {file_name}: {entropy:.4f}")

    except Exception as e:
        print(f"Error processing repository {repo_url}: {e}")

    finally:
        # Clean up temp directory
        shutil.rmtree(temp_dir)
