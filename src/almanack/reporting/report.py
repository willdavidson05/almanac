"""
This module creates entropy reports
"""

from typing import Dict


def repo_entropy_report(data: Dict[str, any]) -> str:
    """
    Returns the formatted entropy report as a string.

    Args:
        data (Dict[str, any]): Dictionary with the entropy data.

    Returns:
        str: Formatted entropy report.
    """

    border = "=" * 50
    separator = "-" * 50
    title = "Entropy Report"

    # Format the report
    report_content = f"""
    {border}
    {title:^50}
    {border}
    Repository Path: {data['repo_path']}
    Total Repository Normalized Entropy: {data['total_normalized_entropy']:.4f}
    {separator}
    {border}
    """
    return report_content
