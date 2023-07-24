import PyPDF2
import os

# Set the path to the folder where the PDF files are located
pdf_folder = os.path.join(os.path.dirname(__file__), "pdfs\\")

# Function to read text from a PDF file by name from pdf_folder
def readTextFromFile(fileName):
    # Open the PDF file in read binary mode
    pdf_file = open(pdf_folder + fileName, 'rb')

    # Create a PdfFileReader object to read the PDF file
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Get the number of pages in the PDF file
    num_pages = len(pdf_reader.pages)
    print("Number of pages: " + str(num_pages))
    print("Enter the pages you'd like to read (e.g. '1-4, 6, 7-9').")
    desired_pages = input("> ")
    pages_array = []

    if desired_pages == "":
        # fill pages_array with numbers from 1 to num_pages
        for i in range(num_pages):
            pages_array.append(i+1)
    else:
        pages_array = parsePageInput(desired_pages)
    
    pdf_text = ""

    for num in pages_array:
        # check if num is larger than the number of pages
        if num > len(pdf_reader.pages):
            break

        page = pdf_reader.pages[num-1]
        page_text = page.extract_text()
        pdf_text += page_text

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