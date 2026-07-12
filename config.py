import argparse
from dotenv import load_dotenv
import os
from pathlib import Path

# Setup the argument parser
def parse_args():
    """Adds arguments to the CLI - currently only supports -a for indicating the user wants to ask the LLM to use their notes as the context for the question."""
    parser = argparse.ArgumentParser(description="Parses the arguments passed through the CLI")
    parser.add_argument("-r", "--read")
    parser.add_argument("-w", "--write")
    args = parser.parse_args()
    return args

def load_config():
    """Loads dotenv variables and creates required directories if they don't already exist."""

    # Get env variables
    load_dotenv()
    api_route = os.getenv("API_ROUTE")
    model = os.getenv("MODEL")
    notes_dir = os.getenv("NOTES_DIR")
    notes_repo_dir = os.getenv("NOTES_REPO_DIR")

    # Create required directories if not exist
    notes_path = Path(notes_dir)
    notes_path.mkdir(parents=True, exist_ok=True)
    notes_repo_path = Path(notes_repo_dir)
    notes_repo_path.mkdir(parents=True, exist_ok=True)

    # Create file path for Notes_Repo
    file_name = "Notes_Repo.md"
    notes_repo_file_path = (notes_repo_path / file_name)

    return api_route, model, notes_path, notes_repo_file_path