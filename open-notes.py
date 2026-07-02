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

def save_note(new_note):
    dir_path = Path("notes")
    dir_path.mkdir(parents=True, exist_ok=True)
    time_stamp = datetime.now().strftime("%Y_%m_%d %H-%M-%S")
    file_name = f"{time_stamp}.md"
    file_path = (dir_path / file_name)

    with open(file_path, "w") as file:
        file.write(new_note)

    print(f"\nNote saved successfully as {file_name}")

def main():
    api_route, model = load_config()
    user_question = get_user_input()
    payload = build_payload(model, user_question)
    data = call_llm(api_route, payload)

    if data is None:
        return

    llm_response = print_response(data)
    new_note = create_note(user_question, llm_response)
    save_note(new_note)
   
if __name__ == "__main__":
    main()