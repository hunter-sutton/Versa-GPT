import dotenv
import openai
import datetime
import tokenizer

import plugins.pdfReader.readPDF as readPDF

openai.api_key = dotenv.get_key(dotenv.find_dotenv(), "OPENAI_API_KEY")

def chatInfo(chat_name, model, prompt):
    print("\033c")
    print("===", chat_name, "===")
    print("=== Model: ", model, "===")
    print("=== Prompt: ", prompt, "===")

def modelSelect():
    # User selects the model to use
    print("Please select a model:")
    print("1. gpt-4")
    print("2. gpt-4-32k")
    print("3. gpt-3.5-turbo")
    print("4. gpt-3.5-turbo-16k")

    model_choice = input("Your choice: ")

    if model_choice == '1':
        model = 'gpt-4'
    elif model_choice == '2':
        model = 'gpt-4-32k'
    elif model_choice == '3':
        model = 'gpt-3.5-turbo'
    elif model_choice == '4':
        model = 'gpt-3.5-turbo-16k'
    else:
        model = 'gpt-3.5-turbo'

    return model

def chatHistoryInit(prompt):
    chat_history = [
        {
            "role": "system",
            "content": prompt
        }
    ]

    return chat_history

def chatHistoryAppend(chat_history, userOrSystem, content):
    role = "user" if userOrSystem == "user" else "assistant"

    chat_history.append({
        "role": role,
        "content": content
    })

def printChatHistory(chat_history):
    for message in chat_history:
        if message["role"] == "user":
            print("\033[30;47mYou\033[0m")
        else:
            print("\033[30;47mAssistant\033[0m")
        print(message["content"])
        print()

# Clear the terminal
print("\033c")

# User selects the model to use
model = modelSelect()

chat_name = input("Name of Chatbot: ")
if chat_name == '':
    chat_name = "ChatGPT"

prompt = input("Your prompt: ")
if prompt == '':
    prompt = "You are a helpful assistant."

# Store the prompt in a file for if the user wants to use it again
# Check if the file already exists, if it does, append to it
try:
    with open("prompts.txt", "a") as prompts_file:
        prompts_file.write("\n\n" + chat_name + " - " + str(datetime.datetime.now()) + "\n\n" + prompt)
except:
    with open("prompts.txt", "w") as prompts_file:
        prompts_file.write("\n\n" + chat_name + " - " + str(datetime.datetime.now()) + "\n\n" + prompt)

# Initialize the chat history
chat_history = chatHistoryInit(prompt)

chatInfo(chat_name, model, prompt)

# Create a while loop that allows the user to keep chatting
print()
while True:
    # Holds each line of the user's input for a single message
    user_input = []

    # Get the user's input. If the user enters a blank line, send the message
    # Otherwise, keep appending to the user_input list
    print("\033[30;47mYou\033[0m")
    while True:
        line = input("> ")
        if line == '':
            break
        else:
            user_input.append(line)

    # Join the user_input list into a single string where each line is separated by a newline
    user_input = '\n'.join(user_input)
    
    if user_input.lower() == 'quit':
        break

    elif user_input.lower() == 'clear':
        chat_history = chatHistoryInit(prompt)
        chatInfo(chat_name, model, prompt)
        continue

    elif user_input.lower() == 'pdf':
        pdf_name = input("PDF Name: ")
        pdf_text = readPDF.readTextFromFile(pdf_name)
        pdf_text = readPDF.addPrefixSuffix("", "", pdf_text, pdf_name)
        tokens = tokenizer.calculateTokens(pdf_text, model)
        print("Number of tokens: " + str(len(tokens)))
        print("Is this acceptable? (y/n)")
        user_input = input("> ")
        if user_input.lower() == 'y':
            chatHistoryAppend(chat_history, "user", pdf_text)
        else:
            continue
        chatHistoryAppend(chat_history, "user", pdf_text)

    elif user_input.lower() == 'history':
        printChatHistory(chat_history)
        continue

    elif user_input.lower() == 'help':
        print("quit - quit the program")
        print("clear - clear the chat history")
        print("pdf - read a PDF file")
        print("history - print the chat history")
        print("help - print this help message")
        continue

    elif user_input.lower() == '':
        print("Please enter a message.")
        continue

    else:
        chatHistoryAppend(chat_history, "user", user_input)

    # Request a response from the selected model
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=chat_history, # Pass the updated chat history
            temperature=1,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
    except openai.error.APIError as e:
        #Handle API error here, e.g. retry or log
        print(f"OpenAI API returned an API Error: {e}")
        continue
    except openai.error.APIConnectionError as e:
        #Handle connection error here
        print(f"Failed to connect to OpenAI API: {e}")
        continue
    except openai.error.RateLimitError as e:
        #Handle rate limit error (we recommend using exponential backoff)
        print(f"OpenAI API request exceeded rate limit: {e}")
        continue

    # Print the model's response
    print()
    print("\033[30;47m" + "==" + chat_name + "==" + "\033[0m")
    print(response["choices"][0]["message"]["content"])
    print()

    # Append the model's response to the chat history
    chatHistoryAppend(chat_history, "system", response["choices"][0]["message"]["content"])