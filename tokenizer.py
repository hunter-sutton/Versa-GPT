import tiktoken

def calculateTokens(pdf_text, model):
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(pdf_text)
    return tokens

# Verify with the user that the number of tokens is acceptable
def verifyTokens(tokens):
    print("Number of tokens: " + str(len(tokens)))
    print("Is this acceptable? (y/n)")
    user_input = input("> ")
    if user_input.lower() == 'y':
        return True
    else:
        return False