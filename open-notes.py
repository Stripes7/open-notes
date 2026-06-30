from dotenv import load_dotenv
import os
import requests


load_dotenv()
api_route = os.getenv("API_ROUTE")
model = os.getenv("MODEL")

user_question = input("Type you note here: ")

payload = {
    "model": model,
    "prompt": user_question,
    "stream": False
}

response = requests.post(api_route, json=payload)

data = response.json()

if response.status_code == 200:
    print(data["response"])
