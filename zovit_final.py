# importing all necessary libraries
import os
import PyPDF2
import pytesseract
from PIL import Image
import re
import pandas as pd
import docx # to load word document
from pdf2image.exceptions import PDFPageCountError

# Function extract_data for importing text from various pdf types (regular, OCR and mixed text/image)
def extract_data(pdf_path): # PDF path with function call
    with open(pdf_path, 'rb') as pdf_file: # The PDF file is opened in binary read mode ('rb')
        reader = PyPDF2.PdfReader(pdf_file) # Reads the pdf
        text = ''
        for page in reader.pages:
            text += page.extract_text()#   # Text is extracted from each page


        # OCR for scanned pages. If the extracted text is empty (indicating it might be a scanned image) or too short (indicating it might be a mixed text/image)  , the code attempts to read the PDF as an image and apply OCR to extract text.
        if not text or len(text) < 100:
            image = Image.open(pdf_path)
            text = pytesseract.image_to_string(image)

    return text

# Function invoice_details for extracting invoice number, invoice date, due date, customer name, total amount and total discount
def invoice_details(text):
    # Extract specific data fields using regular expressions or NLP.Regular expressions are used to find and extract the invoice number and date from the text.
    invoice_number = re.search(r'(Invoice\s+#:)(\s*(INV-\d+))', text).group(2)#Invoice No.:
    invoice_date = re.search(r'(Invoice Date:)(\s+\d{1,2}\s+\b[a-zA-Z]*\s\d{4})', text).group(2) #invoice date
    due_Date=re.search(r'(Due Date:)(.*)',text).group(2) # due date
    customer_Details = re.search(r'Customer Details:\s*(.*)', text).group(1) #customer name
    total_amount=re.search(r'(Total)(.*)', text).group(2) #total amount
    #total_discount = re.search(r'(Total Discount)(.*)', text).group(2) #total discount
        ## ... extract other fields

    return {'Invoice number': invoice_number, 'Invoice date': invoice_date,'Due date':due_Date,'Customer details':customer_Details,'Total amount':total_amount}#,'total_discount':total_discount

#Function to preprocess text to extract data items
def preprocess_text_data_item(text):
    start_keyword='#Item Rate'
    start_index = text.find(start_keyword)
    end_keyword='Taxable Amount'
    end_index = text.find(end_keyword)

    print("start index is",start_index)
    print("End index is",end_index)
    item_text=text[start_index:end_index]
    print("Selected text is",item_text)
    return item_text

# Function extract_items for extracting data items
def extract_items(text):
    item_text = preprocess_text_data_item(text)
    # Regular expression to capture table rows
    invoice_items = re.findall(r'(\d)([a-zA-Z].*)(\d{3})',item_text)#(\d{3}$)
    print(f"Invoice items: {invoice_items}")
    return invoice_items

# Function to store the extracted data items in a list
def invoice_list_extract(text):
    invoice_items = extract_items(text)
    m,n=len(invoice_items),len(invoice_items[0])
    invoice_item_list=[]#List of items
    print("Number of rows of invoice items",m,", Number of columns of invoice items",n)
    for i in range (m):
        inv_temp=invoice_items[i]
        invoice_item_list.append(inv_temp[1])
    print(f"Invoice items list: {invoice_item_list}")
    return invoice_item_list

# Function to check accuracy of invoice number
def check_invoice_number(invoice_number,all_paragraphs_text):
    accuracy = 0
    pattern = re.search(r'(Invoice\s+#:)(\s*(INV-\d+))', all_paragraphs_text).group(2)
    if (pattern==invoice_number):
        accuracy+=1
    return accuracy

# Function to check accuracy of invoice date
def check_invoice_date(invoice_date,all_paragraphs_text):
    accuracy = 0
    pattern = re.search(r'(Invoice Date:)(\s+\d{1,2}\s+\b[a-zA-Z]*\s\d{4})', all_paragraphs_text).group(2)
    if (pattern==invoice_date):
        accuracy+=1
    return accuracy

# Function to check accuracy of due date
def check_due_date(due_date,all_paragraphs_text):
    accuracy = 0
    pattern = re.search(r'(Due Date:)(.*)',all_paragraphs_text).group(2)
    if (pattern==due_date):
        accuracy+=1
    return accuracy

# Function to check accuracy of customer details
def check_customer_Details(customer_Details,all_paragraphs_text):
    accuracy = 0
    pattern = re.search(r'Customer Details:\s*(.*)', all_paragraphs_text).group(1)
    if (pattern==customer_Details):
        accuracy+=1
    return accuracy

accuracy_whole=0 #initiatilizing accuracy of the data extraction for all pdf files in the folder
count=0 # initializing count for estimating number of pdf files in the folder
invoice_number_accuracy = 0
invoice_date_accuracy = 0
due_date_accuracy = 0
customer_Detail_accuracy = 0

# Set the directory where your PDFs are located
folder_path = r'C:\MY DRIVE\Placement test\Zolvit'

# Get all files in the directory
files = os.listdir(folder_path)

# Loop through the files and read each PDF in the folder. Scalability to handle large amount of data
for file in files:
    # Split the filename and extension
    name, ext = os.path.splitext(file)

    # Define paths for PDF and Word files
    pdf_path = os.path.join(folder_path, f"{name}.pdf")
    word_path = os.path.join(folder_path, f"{name}.docx")
    print("pdf file path",pdf_path)
    text = extract_data(pdf_path)
    print(text)

    # Load the Word document
    ground_truth = docx.Document(word_path)
    # Initialize an empty string to store all paragraphs
    all_paragraphs_text = ""
    # Read and print all paragraphs
    for para in ground_truth.paragraphs:
        print(para.text)
        all_paragraphs_text += para.text + "\n"  # Add a newline for separation

    invoice_data = invoice_details(text)
    print(f"Invoice details: {invoice_data}")
    invoice_item_list = invoice_list_extract(text)

    # Steps for checking accuracy for each data item
    invoice_number = invoice_data['Invoice number']
    invoice_date = invoice_data['Invoice date']
    due_date = invoice_data['Due date']
    customer_Details = invoice_data['Customer details']
    total_amount = invoice_data['Total amount']
    #total_discount = invoice_data['total_discount']

    print("Invoice_number is", invoice_number)
    print("Invoice date is", invoice_date)
    print("Due_date is", due_date)
    print("Customer details", customer_Details)
    print("Total amount", total_amount)
    #print("Total discount", total_discount)
    #Estimation of accuracy
    accuracy = (check_invoice_number(invoice_number,all_paragraphs_text) + check_invoice_date(invoice_date,all_paragraphs_text) + check_due_date(
        due_date,all_paragraphs_text) + check_customer_Details(customer_Details,all_paragraphs_text))*100/4

    invoice_number_accuracy+=check_invoice_number(invoice_number,all_paragraphs_text)
    invoice_date_accuracy+=check_invoice_date(invoice_date,all_paragraphs_text)
    due_date_accuracy+=check_due_date(due_date,all_paragraphs_text)
    customer_Detail_accuracy+=check_customer_Details(customer_Details,all_paragraphs_text)

    accuracy_whole+=accuracy
    count+=1

    print("Accuracy is", accuracy,"%")

    # Create DataFrames and to write them into an excel sheet
    invoice_df = pd.DataFrame([invoice_data])
    items_df = pd.DataFrame(invoice_item_list)
    result_filename = r"C:\MY DRIVE\Placement test\Zolvit question and answer\invoice_details"+invoice_number+customer_Details+".xlsx"
    with pd.ExcelWriter(result_filename, engine='openpyxl') as writer:
        invoice_df.to_excel(writer, sheet_name='Invoice', index=False)
        items_df.to_excel(writer, sheet_name='Invoice',startrow=4, index=False)
    print("Invoice details saved to", result_filename)

accuracy_whole=accuracy_whole/count # accuracy of all files
invoice_number_accuracy = invoice_number_accuracy/count*100
invoice_date_accuracy = invoice_date_accuracy/count*100
due_date_accuracy = due_date_accuracy/count*100
customer_Detail_accuracy = customer_Detail_accuracy/count*100

print("accuracy of all files:",accuracy_whole,"%")
print("Number of all files:",count/2)

print("Invoice number",invoice_number_accuracy)
print("Invoice date",invoice_date_accuracy)
print("due date accuracy",due_date_accuracy)
print("customer_Detail_accuracy",customer_Detail_accuracy)

# Trust determination logic
if accuracy_whole>99:
    print("System can be trusted in extracting features")
else:
    print("System is unreliable")
