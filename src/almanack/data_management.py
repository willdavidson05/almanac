import json
from typing import Dict

# If using pathlib for paths:


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
    print(f"Total Commit Normalized Entropy: {data['total_normalized_entropy']:.4f}")

    # Print top 5 files with most entropy
    print("\nTop 5 Files with Most Entropy:")
    print(separator)
    for file_name, entropy in data["5_files_with_most_entropy"]:
        print(f"  {file_name:<40} {entropy:>8.4f}")
    print(separator)

    # Print the report footer
    print(border)

