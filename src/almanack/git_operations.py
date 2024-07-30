import pathlib
from typing import List, Dict
import pygit2
import tempfile

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

def get_edited_files(
    repo: pygit2.Repository, source_commit: pygit2.Commit, target_commit: pygit2.Commit
) -> List[str]:
    """
    Finds all files that have been edited between two specific commits.

    Args:
        repo (pygit2.Repository): The Git repository.
        source_commit (pygit2.Commit): The source commit.
        target_commit (pygit2.Commit): The target commit.

    Returns:
        List[str]: List of file names that have been edited between the two commits.
    """
    file_names = set()
    diff = repo.diff(source_commit, target_commit)
    for patch in diff:
        if patch.delta.old_file.path:
            file_names.add(patch.delta.old_file.path)
        if patch.delta.new_file.path:
            file_names.add(patch.delta.new_file.path)
    return list(file_names)

def get_loc_changed(
    repo_path: pathlib.Path, source: str, target: str, file_names: List[str]
) -> Dict[str, int]:
    """
    Finds the total number of code lines changed for each specified file between two commits.

    Args:
        repo_path (pathlib.Path): The path to the git repository.
        source (str): The source commit hash.
        target (str): The target commit hash.
        file_names (List[str]): List of file names to calculate changes for.

    Returns:
        Dict[str, int]: A dictionary where the key is the filename, and the value is the lines changed (added and removed).
    """
    repo = pygit2.Repository(str(repo_path))

    # Resolve the source and target commits by their hashes
    source_commit = repo.revparse_single(source)
    target_commit = repo.revparse_single(target)

    changes = {}
    # Compute the diff between the source and target commits
    diff = repo.diff(source_commit, target_commit)

    # Iterate over each patch in the diff
    for patch in diff:
        if patch.delta.new_file.path in file_names:
            additions = 0
            deletions = 0
            # Iterate over each hunk in the patch
            for hunk in patch.hunks:
                # Iterate over each line in the hunk
                for line in hunk.lines:
                    if line.origin == "+":
                        additions += 1
                    elif line.origin == "-":
                        deletions += 1
            lines_changed = additions + deletions
            # Store the number of lines changed for the file
            changes[patch.delta.new_file.path] = lines_changed

    return changes

