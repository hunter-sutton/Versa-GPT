class Chat:
    chat_history = []
    user_message = ""
    chat_name = ""
    model = ""
    system_prompt = ""
    temperature = 1

    def __init__(self):
        self.initChatName()
        self.initSystemPrompt()
        self.initModel()
        self.chatHistoryAppend("system", self.system_prompt)
    
    # Gets the model from the user and saves it to self.model
    def initModel(self):
        # User selects the model to use
        print("Please select a model:")
        print("1. gpt-4")
        print("2. gpt-4-32k")
        print("3. gpt-3.5-turbo")
        print("4. gpt-3.5-turbo-16k")

        model_choice = input("Your choice: ")

        if model_choice == '1':
            self.model = 'gpt-4'
        elif model_choice == '2':
            self.model = 'gpt-4-32k'
        elif model_choice == '3':
            self.model = 'gpt-3.5-turbo'
        elif model_choice == '4':
            self.model = 'gpt-3.5-turbo-16k'
        else:
            self.model = 'gpt-3.5-turbo'

    # Gets chat name from the user and saves it to self.chat_name
    def initChatName(self):
        user_input = input("Name of Chatbot: ")
        if user_input == '':
            self.chat_name = "ChatGPT"
        else:
            self.chat_name = user_input
    
    # Gets system prompt from the user and saves it to self.system_prompt
    def initSystemPrompt(self):
        user_input = input("Your prompt: ")
        if user_input == '':
            self.system_prompt = "You are a helpful assistant."
        else:
            self.system_prompt = user_input

    # Appends a message to the chat history with the desired role
    def chatHistoryAppend(self, role, content):
        self.chat_history.append({
            "role": role,
            "content": content
        })
    
    # Gets input from user, joins it into a string, and save it to self.user_message
    def getInputFromUser(self):
        user_input = []
        print("\033[30;47mYou\033[0m")
        while True:
            line = input("> ")
            if line == '':
                break
            else:
                user_input.append(line)
        user_input = '\n'.join(user_input)
        self.user_message = user_input
    
    def printCommands(self):
        print("quit - quit the program")
        print("clear - clear the chat history")
        print("pdf - read a PDF file")
        print("history - print the chat history")
        print("help - print this help message")

    def printChatInfo(self):
        print("===", self.chat_name, "===")
        print("=== Model: ", self.model, "===")
        print("=== Prompt: ", self.system_prompt, "===")

    def printTitle(self):
        print("\033c")
        # ASCII Art below from https://patorjk.com/software/taag/#p=display&f=Sub-Zero&t=Versa%20GPT
        print(" __   __   ______     ______     ______     ______        ______     ______   ______  \n/\ \ / /  /\  ___\   /\  == \   /\  ___\   /\  __ \      /\  ___\   /\  == \ /\__  _\ \n\ \ \\'/   \ \  __\   \ \  __<   \ \___  \  \ \  __ \     \ \ \__ \  \ \  _-/ \/_/\ \/ \n \ \__|    \ \_____\  \ \_\ \_\  \/\_____\  \ \_\ \_\     \ \_____\  \ \_\      \ \_\ \n  \/_/      \/_____/   \/_/ /_/   \/_____/   \/_/\/_/      \/_____/   \/_/       \/_/ \n                                                                                      ")

    def printChatHistory(self):
        for message in self.chat_history:
            if message["role"] == "user":
                print("\033[30;47mYou\033[0m")
            else:
                print("\033[30;47m" + message["role"] + "\033[0m")
            print(message["content"])
            print()