import dotenv
import openai
import datetime
import tokenizer

from Chat import Chat
from plugins.pdfReader import readPDF

openai.api_key = dotenv.get_key(dotenv.find_dotenv(), "OPENAI_API_KEY")

print("\033c")

# Create a new chat instance
chat = Chat()

# Save the system prompt to a file
try:
    with open("prompts.txt", "a") as prompts_file:
        prompts_file.write("\n\n" + chat.chat_name + " - " + str(datetime.datetime.now()) + "\n\n" + chat.system_prompt)
except:
    with open("prompts.txt", "w") as prompts_file:
        prompts_file.write("\n\n" + chat.chat_name + " - " + str(datetime.datetime.now()) + "\n\n" + chat.system_prompt)

chat.printTitle()
chat.printChatInfo()
print()

# Create a while loop that allows the user to keep chatting
while True:
    chat.getInputFromUser()

    # quit by breaking the loop
    if chat.user_message.lower() == 'quit':
        break

    # clear the chat history
    elif chat.user_message.lower() == 'clear':
        chat.chat_history = []
        chat.chatHistoryAppend("system", chat.system_prompt)
        print("\033c")
        chat.printChatInfo()
        continue

    # read a PDF file
    elif chat.user_message.lower() == 'pdf':
        print("*** PDF Reader ***")
        # get a list of the available PDFs
        pdfs = readPDF.listPdfs()

        print("PDFs:")
        for index, pdf in enumerate(pdfs):
            print(str(index + 1) + ". " + pdf)

        print("Which PDF would you like to read?")
        user_input = input("> ")

        pdf_text = readPDF.readTextFromFile(pdfs[int(user_input) - 1])
        tokens = tokenizer.calculateTokens(pdf_text, chat.model)

        if tokenizer.verifyTokens(tokens):
            print("You may now choose an action to perform on the PDF.")
            print("1. Simply give the PDF text to the chatbot")
            print("2. Summarize the PDF")
            action = input("> ")

            if action.isdigit():
                action = int(action)
            else:
                action = 1

            user_message = readPDF.addPrefixSuffix(action, pdf_text)

            chat.chatHistoryAppend("user", user_message)
        else:
            continue

    # print the chat history
    elif chat.user_message.lower() == 'history':
        chat.printChatHistory()
        continue

    elif chat.user_message.lower() == 'name':
        chat.initChatName()
        continue

    elif chat.user_message.lower() == 'prompt':
        chat.initSystemPrompt()
        chat.chat_history = []
        chat.chatHistoryAppend("system", chat.system_prompt)
        print("New system prompt accepted")
        continue

    # print the help message
    elif chat.user_message.lower() == 'help':
        chat.printCommands()
        continue

    # if the user enters nothing, print a message
    elif chat.user_message.lower() == '':
        print("Please enter a message or `help` to see other commands.")
        continue

    # if the input is not a command, append it to the chat history
    else:
        chat.chatHistoryAppend("user", chat.user_message)

    # Request a response from the selected model
    try:
        response = openai.ChatCompletion.create(
            model=chat.model,
            messages=chat.chat_history, # Pass the updated chat history
            temperature=chat.temperature,
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
    print("\033[30;47m" + "==" + chat.chat_name + "==" + "\033[0m")
    print(response["choices"][0]["message"]["content"])
    print()

    # Append the model's response to the chat history
    chat.chatHistoryAppend("assistant", response["choices"][0]["message"]["content"])