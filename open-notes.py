from dotenv import load_dotenv
import os
import requests
from pathlib import Path
from datetime import datetime


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

    return api_route, model, notes_path, notes_repo_path


def get_user_input():
    """Gets user input to be sent to the model."""
    user_question = input("Type your note here: ")

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
        print(llm_response)
    
        return llm_response


def create_note(question, llm_response):
    """Creates a string using the user input and llm response to be later converted in a note."""
    new_note = (f"User Input: {question} \n\nLLM Output: {llm_response}")
    
    return new_note


def save_note(new_note, notes_path):
    """Creates a new note file and saves to the defined path."""
    time_stamp = datetime.now().strftime("%Y_%m_%d %H-%M-%S")
    file_name = f"{time_stamp}.md"
    file_path = (notes_path / file_name)

    with open(file_path, "w") as file:
        file.write(new_note)

    print(f"\nNote saved successfully as {file_name}")


def load_notes(notes_path, notes_repo_path):
    """Takes a path object - iterates through files in the directory - copies contents of each file to a central repository file"""
    # I only want to create a file once - this is fine for now though
    # Logic is broken for now - look at pathlib Path functions
    time_stamp = datetime.now().strftime("%Y_%m_%d %H-%M-%S")
    file_name = f"Note_Repo_{time_stamp}.md"
    file_path = (notes_repo_path / file_name)

    for note in notes_path.iterdir():
        with note.open() as current_note:
            current_note = note.read_text()
        with open(file_path, "w") as note_repo:
            note_repo.write(current_note)
    
    print(f"All notes copied and saved successfully as {file_path}")


def main():
    api_route, model, notes_path, notes_repo_path = load_config()
    user_question = get_user_input()
    payload = build_payload(model, user_question)
    data = call_llm(api_route, payload)

    if data is None:
        return

    llm_response = print_response(data)
    new_note = create_note(user_question, llm_response)
    save_note(new_note, notes_path)
    load_notes(notes_path, notes_repo_path)
   
if __name__ == "__main__":
    main()