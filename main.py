import config
import llm
import notes

def main():
    arguments = config.parse_args()

    # Checking if the user indicated the input is a note
    if arguments.write is not None:
        isNote = True
        user_input = arguments.write

    elif arguments.read is not None:
        isNote = False
        user_input = arguments.read

    else:
        return print("ERROR: Missing argument.")

    api_route, model, notes_path, notes_repo_file_path = config.load_config()
    payload = llm.build_payload(model, user_input, isNote, notes_repo_file_path)
    data = llm.call_llm(api_route, payload)

    if data is None:
        return

    llm_response = llm.print_response(data)

    if isNote:
        new_note, time_stamp = notes.create_note(user_input, llm_response)
        notes.save_note(new_note, notes_path, notes_repo_file_path, time_stamp)
   
if __name__ == "__main__":
    main()