import tokenizer
import PyPDF2
import os

from Chat import Chat

# PDF storage folder
pdf_folder = os.path.join(os.path.dirname(__file__), "pdfs\\")

# Function to read text from a PDF file by name from pdf_folder
def readTextFromFile(fileName):
    # Open the PDF file in read binary mode
    pdf_file = open(pdf_folder + fileName, 'rb')

    # Create a PdfFileReader object to read the PDF file
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Get the number of pages in the PDF file
    num_pages = len(pdf_reader.pages)
    
    # Prompt the user to enter the pages they would like to read
    print("Number of pages: " + str(num_pages))
    print("Enter the pages you'd like to read (e.g. '1-4, 6, 7-9').")
    desired_pages = input("> ")
    pages_array = []

    # If the user entered nothing, read all pages
    if desired_pages == "":
        for i in range(num_pages):
            pages_array.append(i+1)
    else:
        pages_array = parsePageInput(desired_pages)
    
    pdf_text = ""

    # Loop through the desired pages and extract the text
    for num in pages_array:
        if num > len(pdf_reader.pages):
            break

        page = pdf_reader.pages[num-1] # get the page
        page_text = page.extract_text() # extract the text
        pdf_text += page_text # append the text to the pdf_text string

    return pdf_text

# function to get array of numbers from input
# https://stackoverflow.com/questions/6405208/how-to-convert-numeric-string-ranges-to-a-list-in-python  
def parsePageInput(s):
    return sum(((list(range(*[int(j) + k for k,j in enumerate(i.split('-'))]))
         if '-' in i else [int(i)]) for i in s.split(',')), [])


def addPrefixSuffix(option, pdfText):
    actions = {
        1: "Here is the text from a PDF.\n\n```",
        2: "Summarize the following text from the PDF file named <pdfName>." 
    }

    formatted_pdf_text = actions[option] + pdfText + "```"

    return formatted_pdf_text

def listPdfs():
    # Create a list to hold the names of the PDF files
    pdfs = []

    # Loop through the files in the pdf_folder
    for file in os.listdir(pdf_folder):
        # If the file is a PDF file, append the name to the pdfs list
        if file.endswith(".pdf"):
            pdfs.append(file)

    # Return the list of PDF file names
    return pdfs

def run(chat: Chat):
    print("*** PDF Reader ***")

    # Get a list of the available PDFs
    pdfs = listPdfs()

    # Print the list of PDFs
    print("PDFs:")
    for index, pdf in enumerate(pdfs):
        print(str(index + 1) + ". " + pdf)

    # Ask the user which PDF they would like to read
    print("Which PDF would you like to read?")
    user_input = input("> ")

    if user_input.isdigit():
        user_input = int(user_input)
    else:
        user_input = 1

    # Read the text from the PDF file
    pdf_text = readTextFromFile(pdfs[user_input - 1])

    # Calculate the number of tokens in the PDF text
    tokens = tokenizer.calculateTokens(pdf_text, chat.model)

    # Verify with the user that the number of tokens is acceptable
    if tokenizer.verifyTokens(tokens):
        print("You may now choose an action to perform on the PDF.")
        print("1. Simply give the PDF text to the chatbot")
        print("2. Summarize the PDF")
        action = input("> ")

        if action.isdigit():
            action = int(action)
        else:
            action = 1

        user_message = addPrefixSuffix(action, pdf_text)

        chat.user_message = user_message
        chat.chatHistoryAppend("user", chat.user_message)
    else:
        print("Leaving PDF Reader...")