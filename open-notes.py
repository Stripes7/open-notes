from dotenv import load_dotenv
import os
import requests
from pathlib import Path
from datetime import datetime

def load_config():

    load_dotenv()
    api_route = os.getenv("API_ROUTE")
    model = os.getenv("MODEL")

    return api_route, model

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
    data = response.json()

    return response, data

def save_note(cleaned_note):
    dir_path = Path("open-notes/notes")
    dir_path.mkdir(parents=True, exist_ok=True)
    time_stamp = datetime.now().strftime("%Y_%m_%d_%H:%M:%S")
    file_name = f"{time_stamp}.md"
    file_path = os.path.join(dir_path, file_name)

    print(file_path)

    with open(file_path, "w") as file:
        file.write(cleaned_note)

def print_response(response, data):

    if response.status_code == 200:
        note = data["response"]
        print(note)

    return note

def main():

    api_route, model = load_config()
    user_question = get_user_input()
    payload = build_payload(model, user_question)
    response, data = call_llm(api_route, payload)
    note = print_response(response, data)
    save_note(note)

if __name__ == "__main__":
    main()