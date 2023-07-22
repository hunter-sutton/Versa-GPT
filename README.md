# VersaGPT

## Introduction
VersaGPT is an application that uses the OpenAI API to allow the user to engage in a conversation with a GPT model. Plugins are included in the application and allow VersaGPT to do things that a chatbot cannot normall do.

## Installation
1. Clone the repository.
2. Install the requirements.
    - `pip install -r requirements.txt`
3. Create a `.env` file in the root directory.
4. Add the following to the `.env` file:
    - `OPENAI_API_KEY="<your-openai-api-key>"`
5. Run the application.

### Chat Commands
Run these by sending a message containing only the command.

- `quit` - Quits the application
- `help` - Displays a list of commands
- `history` - Prints the chat history
- `clear` - Clears the chat history. This is like starting a new conversation using the same system prompt.
- `pdf` - Starts the PDF Reader plugin. More information on plugins can be found [below](Plugins).

## Usage
1. Run the application.
    - `python main.py`
2. Choose a model.
3. Enter a name for the chatbot.
    - This has no effect on the chatbot's behavior and can be left blank for a default name.
4. Enter a system prompt.
    - This is the prompt that the chatbot will use to guide its behavior.
    - If left blank, the prompt defaults to "You are a helpful assistant."
5. Begin chatting with the chatbot.
    - Plugins can be used by sending a message containing only the name of the plugin. More information on plugins can be found [below](Plugins).

## Plugins
VersaGPT includes the following plugins and more are being developed.
- PDF Reader
    - The PDF Reader plugin can read PDF files and feed them to the GPT model.
    - You must store files that you want to read in the `/plugins/pdfReader/pdfFolder` directory.
    - Send a message containing only `pdf` to the bot to start the plugin.

## TODO
### General
- [ ] Prettify
    - [ ] Add colors
    - [ ] Display messages in a more readable way
- [ ] Model modification during conversation
    - [ ] Change model
    - [ ] Change system prompt
    - [ ] Change chatbot name
    - [ ] Change temperature, top_p, and frequency_penalty
    - [ ] Change max_tokens
- [ ] Allow user to save conversations and prompts to be loaded later
### Plugins
- [ ] PDF Reader Improvements
    - [ ] List PDFs for the user to choose from
    - [ ] Allow user to specify page numbers to read
- [ ] Google Search
- [ ] Wolfram Alpha
- [ ] Write/Execute Code
- [ ] Prompt Improver