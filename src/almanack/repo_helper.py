import json
import pathlib
import shutil
import tempfile
from datetime import datetime, timezone
from typing import Dict, List, Union

import pygit2

from .entropy import calculate_normalized_entropy, aggregate_entropy_calculation

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
    walker = repo.walk(head.id, pygit2.GIT_SORT_NONE)  # Use GIT_SORT_NONE to ensure all commits are included
    commits = [commit for commit in walker]
    
    return commits

def get_edited_files(repo: pygit2.Repository, commits: List[pygit2.Commit]) -> List[str]:
    """
    Finds all files that have been edited in the repository.
    
    Args:
        repo (pygit2.Repository): The Git repository.
        commits (List[pygit2.Commit]): List of commits in the repository.
    
    Returns:
        List[str]: List of file names that have been edited.
    """
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
    return list(file_names)

def save_entropy_to_json(repo_url: str, file_level_entropy: Dict[str, float], normalized_total_entropy: float, output_path: str) -> None:
    """
    Saves the entropy values and the top 5 files with the most entropy to a JSON file.
    
    Args:
        repo_url (str): The URL of the GitHub repository.
        file_level_entropy (Dict[str, float]): Entropy values for each file.
        normalized_total_entropy (float): Total normalized entropy for the repository.
        output_path (str): Path to the output JSON file.
    """
    # Sort the files by entropy in descending order and get the top 5
    sorted_files_by_entropy = sorted(file_level_entropy.items(), key=lambda item: item[1], reverse=True)[:5]

    data = {
        "repo_url": repo_url,
        "total_normalized_entropy": normalized_total_entropy,
        "file_level_entropy": file_level_entropy,
        "top_5_files_with_most_entropy": sorted_files_by_entropy
    }

    with open(output_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def print_entropy_from_json(output_path: str) -> None:
    """
    Prints the entropy values from a JSON file.
    
    Args:
        output_path (str): Path to the output JSON file.
    """
    with open(output_path, 'r') as json_file:
        data = json.load(json_file)
    
    print(f"Repository URL: {data['repo_url']}")
    print(f"Total Normalized Entropy: {data['total_normalized_entropy']:.4f}")
    print("Top 5 Files with Most Entropy:")
    for file_name, entropy in data['top_5_files_with_most_entropy']:
        print(f"  {file_name}: {entropy:.4f}")

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
        
        file_names = get_edited_files(repo, commits)
        
        normalized_total_entropy = aggregate_entropy_calculation(
            repo_path, str(second_most_recent_commit.id), str(most_recent_commit.id), file_names
        )

        file_level_entropy = calculate_normalized_entropy(
            repo_path, str(second_most_recent_commit.id), str(most_recent_commit.id), file_names
        )

        save_entropy_to_json(repo_url, file_level_entropy, normalized_total_entropy, output_path)
        print_entropy_from_json(output_path)

    except Exception as e:
        print(f"Error processing repository {repo_url}: {e}")

    finally:
        shutil.rmtree(temp_dir)

