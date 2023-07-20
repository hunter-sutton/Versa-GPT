import tiktoken

def calculateTokens(pdf_text, model):
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(pdf_text)
    return tokens