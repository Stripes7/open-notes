from dotenv import load_dotenv
import os
import requests
from pathlib import Path
from datetime import datetime

################################# TO DO's ###############################################################################################
# Add docstrings to each function
# Create a generate timestamp function to be used in save notes and load notes (or maybe just create file?) or two separate functions
# User question needs to change to user_input or something more generic since it won't always be a question, could be a directive
#########################################################################################################################################

def load_config():

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
    user_question = input("Type your note here: ")

    return user_question

def build_payload(model, user_question, stream=False):
    payload = {
        "model": model,
        "prompt": user_question,
        "stream": stream
    }
    return payload

def call_llm(api_route, payload):
    response = requests.post(api_route, json=payload)

    if response.status_code != 200:
        print("Communication issue with the LLM, please try again.")
        return

    data = response.json()
    return data

def print_response(data):
        llm_response = data["response"]
        print(llm_response)
    
        return llm_response

def create_note(question, llm_response):
    new_note = (f"User Input: {question} \n\nLLM Output: {llm_response}")
    
    return new_note

def save_note(new_note, notes_path):
    time_stamp = datetime.now().strftime("%Y_%m_%d %H-%M-%S")
    file_name = f"{time_stamp}.md"
    file_path = (notes_path / file_name)

    with open(file_path, "w") as file:
        file.write(new_note)

    print(f"\nNote saved successfully as {file_name}")

def load_notes(notes_path, notes_repo_path):
    """Takes a path object - iterates through files in the directory - copies contents of each file to a central repository file"""
    # I only want to create a file once 
    time_stamp = datetime.now().strftime("%Y_%m_%d %H-%M-%S")
    file_name = f"Note_Repo_{time_stamp}.md"
    file_path = (notes_path / file_name)

    for note in notes_path:
        with open(notes_repo_path, "w") as file:
            file.write(note)
    
    print(f"All notes copied and saved successfully as {file_path}")



def main():
    api_route, model, notes_path = load_config()
    user_question = get_user_input()
    payload = build_payload(model, user_question)
    data = call_llm(api_route, payload)

    if data is None:
        return

    llm_response = print_response(data)
    new_note = create_note(user_question, llm_response)
    save_note(new_note, notes_path)
   
if __name__ == "__main__":
    main()