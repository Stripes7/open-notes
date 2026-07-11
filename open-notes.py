from dotenv import load_dotenv
import os
import requests
from pathlib import Path
from datetime import datetime
import argparse

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


def build_context(notes_repo_file_path, user_input):
    """Builds the payload creating a prompt which uses the note_repo as the context for the LLM to use."""

    notes_context = notes_repo_file_path.read_text()
    prompt = (f"""

You are answering questions using only the notes below.
                        
If the answer is not in the notes, say you don't know based on the saved notes.

Notes:
{notes_context}

Question:
{user_input}

""")
    
    return prompt


def build_payload(model, user_input, isNote, notes_repo_file_path, stream=False) :
    """Builds the payload to be sent to the model."""

    # Is a note to be saved - Prompts the LLM with the user input only
    if isNote:
        payload = {
            "model": model,
            "prompt": user_input,
            "stream": stream
            }
        
    # Is not a note to be saved - Prompts the LLM with the user input and adds context to only use the notes_repo as it's source
    else:
        payload = {
            "model": model,
            "prompt": build_context(notes_repo_file_path, user_input),
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


def create_note(user_input, llm_response):
    """Creates a string using the user input and llm response to be later converted in a note."""

    time_stamp = datetime.now().strftime("%Y_%m_%d %H-%M-%S")
    new_note = (f"""## {time_stamp}

### User Input

{user_input}

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


def main():
    arguments = parse_args()

    # Checking if the user indicated the input is a note
    if arguments.write is not None:
        isNote = True
        user_input = arguments.write

    elif arguments.read is not None:
        isNote = False
        user_input = arguments.read

    else:
        return print("ERROR: Missing argument.")

    api_route, model, notes_path, notes_repo_file_path = load_config()
    payload = build_payload(model, user_input, isNote, notes_repo_file_path)
    data = call_llm(api_route, payload)

    if data is None:
        return

    llm_response = print_response(data)

    if isNote:
        new_note, time_stamp = create_note(user_input, llm_response)
        save_note(new_note, notes_path, notes_repo_file_path, time_stamp)
   
if __name__ == "__main__":
    main()