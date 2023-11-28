import dotenv
import openai
import datetime

from Chat import Chat
from plugins.pdfReader import readPDF

openai.api_key = dotenv.get_key(dotenv.find_dotenv(), "OPENAI_API_KEY")

print("\033c")

# Create a new chat instance. During initialization, the user is prompted
# to enter a chat name, system prompt, and model.
chat = Chat()

# Save the system prompt to a file, prompts.txt
try:
    # If the file exists, append the system prompt to the end of the file
    with open("prompts.txt", "a") as prompts_file:
        prompts_file.write("\n\n" + chat.chat_name + " - " + str(datetime.datetime.now()) + "\n\n" + chat.system_prompt)
except:
    # If the file does not exist, create it and write the system prompt to it
    with open("prompts.txt", "w") as prompts_file:
        prompts_file.write("\n\n" + chat.chat_name + " - " + str(datetime.datetime.now()) + "\n\n" + chat.system_prompt)

# Clear the terminal and print the chat name, model, and system prompt
chat.printTitle()
chat.printChatInfo()
print()

# Start the conversation
while True:
    chat.getInputFromUser()

    if chat.user_message.lower() == 'quit':
        break
    elif chat.user_message.lower() == 'clear':
        chat.clear()
        continue
    elif chat.user_message.lower() == 'pdf':
        readPDF.run(chat)
        continue
    elif chat.user_message.lower() == 'history':
        chat.history()
        continue
    elif chat.user_message.lower() == 'name':
        chat.initChatName()
        continue
    elif chat.user_message.lower() == 'prompt':
        chat.prompt()
        continue
    elif chat.user_message.lower() == 'help':
        chat.help()
        continue
    elif chat.user_message.lower() == '':
        print("Please enter a message or `help` to see other commands.")
        continue
    else:
        chat.chatHistoryAppend("user", chat.user_message)

    # Request a response from the selected model
    try:
        response = openai.chat.completions.create(
            model=chat.model,
            messages=chat.chat_history, # Pass the updated chat history
            temperature=chat.temperature,
            max_tokens=748,
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
    print(response.choices[0].message.content)
    print()

    # Append the model's response to the chat history
    chat.chatHistoryAppend("assistant", response.choices[0].message.content)