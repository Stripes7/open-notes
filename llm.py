import requests

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