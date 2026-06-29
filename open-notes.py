from dotenv import load_dotenv
import os
import requests

load_dotenv()
api_route = os.environ.get("API_ROUTE")
model = "llama3.2"

user_question = input("What is your question? ")

payload = {
    "model": model,
    "prompt": user_question
}

print(type(payload))
response = requests.post(api_route, json=payload)

print(dir(response))

if response.status_code == 200:
    print(response.text)
