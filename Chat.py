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
            self.system_prompt = ""
        else:
            self.system_prompt = user_input

    # Clears the chat history. This is like starting a new chat.
    def clear(self):
        self.chat_history = []
        self.chatHistoryAppend("system", self.system_prompt)
        print("\033c")
        self.printChatInfo()

    # Allows the user to change the system prompt
    def prompt(self):
        self.initSystemPrompt()
        self.chat_history = []
        self.chatHistoryAppend("system", self.system_prompt)
        print("New prompt set.")

    # Allows the user to change the temperature
    def temp(self):
        user_input = input("New temperature: ")

        if user_input == '':
            self.temperature = 1
            print("Temperature reset to 1.")
            return

        user_input = float(user_input)

        if user_input < 0 or user_input > 2:
            print("Temperature must be between 0 and 2.")
            return
        
        self.temperature = user_input
        print("Temperature set to", user_input)
    
    # Prints information about available commands
    def help(self):
        print("clear - clear the chat history")
        print("help - print this help message")
        print("history - print the chat history")
        print("name - change the chat name")
        print("pdf - read a PDF file")
        print("prompt - change the system prompt")
        print("quit - quit the program")

    # Prints the chat history
    def history(self):
        for message in self.chat_history:
            if message["role"] == "user":
                print("\033[30;47mYou\033[0m")
            else:
                print("\033[30;47m" + message["role"] + "\033[0m")
            print(message["content"])
            print()

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

    def printChatInfo(self):
        print("===", self.chat_name, "===")
        print("=== Model: ", self.model, "===")
        print("=== Prompt: ", self.system_prompt, "===")

    def printTitle(self):
        print("\033c")
        # ASCII Art below from https://patorjk.com/software/taag/#p=display&f=Sub-Zero&t=Versa%20GPT
        print(" __   __   ______     ______     ______     ______        ______     ______   ______  \n/\ \ / /  /\  ___\   /\  == \   /\  ___\   /\  __ \      /\  ___\   /\  == \ /\__  _\ \n\ \ \\'/   \ \  __\   \ \  __<   \ \___  \  \ \  __ \     \ \ \__ \  \ \  _-/ \/_/\ \/ \n \ \__|    \ \_____\  \ \_\ \_\  \/\_____\  \ \_\ \_\     \ \_____\  \ \_\      \ \_\ \n  \/_/      \/_____/   \/_/ /_/   \/_____/   \/_/\/_/      \/_____/   \/_/       \/_/ \n                                                                                      ")