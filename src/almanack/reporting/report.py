"""
This module creates entropy reports
"""



def repo_entropy_report(data: str) -> None:
    """
    Prints the entropy values from a JSON string.

    Args:
        json_string (str): JSON string with the entropy data.
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
    print(report_content)
