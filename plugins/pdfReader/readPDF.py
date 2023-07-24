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

    # Create a list to hold the text from each page in the PDF file
    pdf_text = []

    # Loop through each page in the PDF file and append the text to the list
    for page in range(num_pages):
        pdf_text.append(pdf_reader.pages[page].extract_text())

    # Close the PDF file
    pdf_file.close()

    pdf_text = addPrefixSuffix(pdf_text, fileName)

    # Return the text from the PDF file
    return pdf_text

def addPrefixSuffix(pdfText, pdfName):
    prefix = "Here is a PDF file. It is called " + pdfName + ".\n\n```"
    suffix = "```"    

    # Join the pdfText list into a single string where each line is separated by a newline like the following:
    # Here is a PDF file. It is called <pdfName>.
    # 
    # ```
    # <pdfText>
    # ```
    pdfText = ''.join(pdfText)
    pdfText = prefix + pdfText + suffix

    return pdfText

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