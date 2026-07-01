from dotenv import load_dotenv
import os
import requests

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

def print_response(response, data):

    if response.status_code == 200:
        print(data["response"])

def main():

    api_route, model = load_config()
    user_question = get_user_input()
    payload = build_payload(model, user_question)
    response, data = call_llm(api_route, payload)
    print_response(response, data)

if __name__ == "__main__":
    main()