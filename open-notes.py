from dotenv import load_dotenv
import os
import requests
from pathlib import Path
from datetime import datetime
import argparse

# Setup the argument parser
def parse_args():
    parser = argparse.ArgumentParser(description="Parses the arguments passed through the CLI")
    parser.add_argument("-a", "--ask")
    args = parser.parse_args()

    if args.ask:
        return True
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


def get_user_input():
    """Gets user input to be sent to the model."""

    user_question = input("User Input: ")

    return user_question


def build_payload(model, user_question, stream=False):
    """Builds the payload to be sent to the model."""

    payload = {
        "model": model,
        "prompt": user_question,
        "stream": stream
    }
    return payload


def call_llm(api_route, payload):
    """Sends payload to the model and converts the response body to json upon successful response code."""

    response = requests.post(api_route, json=payload)

    if response.status_code != 200:
        print("Communication issue with the LLM, please try again.")
        return

    data = response.json()
    return data


def print_response(data):
    """Extracts the response from the llm response."""

    llm_response = data["response"]
    print(f"LLM Response: {llm_response}")

    return llm_response


def create_note(question, llm_response):
    """Creates a string using the user input and llm response to be later converted in a note."""

    time_stamp = datetime.now().strftime("%Y_%m_%d %H-%M-%S")
    new_note = (f"""## {time_stamp}

### User Input

{question}

### LLM Output

{llm_response}

---

""")
    
    return new_note, time_stamp


def save_note(new_note, notes_path, notes_repo_file_path, time_stamp):
    """Creates a new note file and saves to the defined path. Also saves note to the Notes_Repo."""

    file_name = f"{time_stamp}.md"
    file_path = (notes_path / file_name)

    file_path.write_text(new_note)

    with notes_repo_file_path.open("a") as file:
        file.write(new_note)

    print(f"""
          Note saved successfully as {file_name}.
          Note copied to repo file at file path: {notes_repo_file_path} and saved successfully.""")


def ask_notes():
    """Enables the user to ask a question with their Notes_Repo as the context for the LLM to use for it's reply"""


def main():
    api_route, model, notes_path, notes_repo_file_path = load_config()
    user_question = get_user_input()
    payload = build_payload(model, user_question)
    data = call_llm(api_route, payload)

    if data is None:
        return

    llm_response = print_response(data)
    new_note, time_stamp = create_note(user_question, llm_response)
    save_note(new_note, notes_path, notes_repo_file_path, time_stamp)
   
if __name__ == "__main__":
    main()