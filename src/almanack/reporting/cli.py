"""
Setup process_repo_entropy CLI through python-fire
"""
import fire

from almanack.reporting.report import process_repo_entropy


def run_cli() -> None:
    """
    Run the CLI command to process repository entropy using python-fire.
    """
    fire.Fire(process_repo_entropy)


if __name__ == "__main__":
    """
    Setup the CLI with python-fire for the almanack package.

    This allows the function `check` to be ran through the
    command line interface.
    """
    run_cli()
