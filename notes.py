from datetime import datetime

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