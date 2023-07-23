import dotenv
import openai
import datetime
import tokenizer

from Chat import Chat
import plugins.pdfReader.readPDF as readPDF

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

    if chat.user_message.lower() == 'quit':
        break
    elif chat.user_message.lower() == 'clear':
        chat.chat_history = []
        chat.chatHistoryAppend("system", chat.system_prompt)
        print("\033c")
        chat.printChatInfo()
        continue
    elif chat.user_message.lower() == 'pdf':
        pdf_name = input("PDF Name: ")
        pdf_text = readPDF.readTextFromFile(pdf_name)
        tokens = tokenizer.calculateTokens(pdf_text, chat.model)
        if tokenizer.verifyTokens(tokens):
            chat.chatHistoryAppend("user", pdf_text)
        else:
            continue
    elif chat.user_message.lower() == 'history':
        chat.printChatHistory()
        continue
    elif chat.user_message.lower() == 'help':
        chat.printCommands()
        continue
    elif chat.user_message.lower() == '':
        print("Please enter a message or `help` to see other commands.")
        continue
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