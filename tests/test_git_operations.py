"""
Test git operations functionality
"""

import pathlib

import pygit2

from almanack.git_operations import get_commits, get_loc_changed

def test_clone_reopsitory():
    pass
def test_get_commits():
    pass
def test_get_edited_files():
    pass

def get_most_recent_commits(repo_path: pathlib.Path) -> tuple[str, str]:
    """
    Retrieves the two most recent commit hashes in the test repositories

    Args:
        repo_path (pathlib.Path): The path to the git repository.

    Returns:
        tuple[str, str]: Tuple containing the source and target commit hashes.
    """
    repo = pygit2.Repository(str(repo_path))
    commits = get_commits(repo)

    # Assumes that commits are sorted by time, with the most recent first
    source_commit = commits[1]  # Second most recent
    target_commit = commits[0]  # Most recent

    return str(source_commit.id), str(target_commit.id)


def test_get_loc_changed(
    repository_paths: dict[str, pathlib.Path], repo_file_sets: dict[str, list[str]]
) -> None:
    """
    Test the calculate_loc_changes function.
    """

    results = {}
    

    for label, repo_path in repository_paths.items():
        # Extract two most recent commits: source and target
        source_commit, target_commit = get_most_recent_commits(repo_path)
        # Call loc_changes function on test repositories
        loc_changes = get_loc_changed(
            repo_path, source_commit, target_commit, repo_file_sets[label]
        )
        results[label] = loc_changes
    assert all(
        file_name in loc_changes for file_name in repo_file_sets[label]
    )  # Check that file_sets[label] are present keys
    assert all(
        change >= 0 for change in loc_changes.values()
    )  # Check that all values are non-negative
