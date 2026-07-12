## DORIS
---
### Digital Organized Recall & Intelligence System
### A notes application that interfaces with an LLM for storage and retrieval of notes.

## Current Features
---
### Ask an LLM a question - the question and answer will be stored in the notes directory as a .md file with timestamp.

## Installation
---
### Placeholder

## Configuration (.env)
---
### API_Route = path to ollama service
### MODEL = model you would like to run
### DIR_PATH = directory in which notes will be stored

## Running the application
---
### Application runs from the CLI and requires either the -r (--read) argument or the -w (--write) argument. -r will use the notes_repository as it's context for the generated output. -w will use the models full context for the generated output. -w will also save the input and response as a unique note file with the input, response, and timestamp. -w will also save the input and response into the notes_repo to be used for future -r context builds.

## Project Structure
---
### Placeholder

## Planned Features
---
### Text Based UI
### GUI
### Per Session context for conversational interactions

## License
---
### Placeholder
