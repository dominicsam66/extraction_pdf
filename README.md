# extraction_pdf
Project to extract data from pdf consisting of mix of images and text.


Invoice Bill Data Extraction

This project is done to extract data from pdf files in a folder. The pdf files are invoice bills of a pharmacy which contains mix of images and text.
1)	Technical documentation of the code: -

Libraries used: -
•	OS
•	PyPDF2
•	Pytesseract
•	re
•	pandas
•	docx

Functions used: -
•	extract_data(pdf_path): - Function extract_data for importing text from various pdf types (regular, OCR and mixed text/image).
•	invoice_details(text): - Function invoice_details for extracting invoice number, invoice date, due date, customer name, total amount and total discount.
•	preprocess_text_data_item(text):- Function to preprocess text to extract data items.
•	extract_items(text):- Function extract_items for extracting data items.
•	invoice_list_extract(text):- Function to store the extracted data items in a list.
•	check_invoice_number(invoice_number,all_paragraphs_text):- Function to check accuracy of invoice number.
•	check_invoice_date(invoice_date,all_paragraphs_text):- Function to check accuracy of invoice date.
•	check_due_date(due_date,all_paragraphs_text):- Function to check accuracy of due date
•	check_customer_Details(customer_Details,all_paragraphs_text):- Function to check accuracy of customer details

Algorithm and approach :- 
	 
Step 1:- The pdf files in the folder will be read using the folder destination path. Then function ‘extract_data(pdf_path)’ is used to extract the data using ‘PyPDF2’ library (for regular pdf) and store them in the variable ‘text’. But, if the pdf file is scanned document or mix of image and text, then using an ‘if’ statement the type of data is checked. For scanned document and mix of images and text, ‘pytesseract’ library is used to convert the image into string and then store them in variable ‘text’.
 
Step 2:- The pdf files in the folder were converted to word document (using online pdf to word converter I love pdf), and uploaded into the program using ‘ground_truth’ variable and its text is stored in ‘all_paragraphs_text’. This text would be compared with the extracted data from the pdf using the code developed, for accuracy and trust determination check.

Step 3:- Function ‘invoice_details(text)’ is executed using ‘text’ from step 2 as input. With the help of ‘RegEx’, or Regular Expression module, data like invoice number, invoice date, due date, customer detail (name of customer) and total amount was extracted by comparing the text with specified pattern provided in ‘re.search()’ function.  

Step 4:- In order to extract the list of items purchased from the pharmacy, three functions were used. First function ‘preprocess_text_data_item(text)’ was used to crop only the part of the text that contains list or table of items purchased.

Step 5:- Inside function ‘extract_items(text)’, preprocessed or cropped text from step 4 is assigned to variable ‘item_text’. RegEx function ‘re.findall()’ is used to extract a list of data based on specified pattern (i.e., a digit followed by space (group 1) , a group of letters till a 3 digit number (group 2) and three digit number (group3). This function returns a list of tuples. Each tuple has three element resembling the three groups. For eg:- from bill invoice number ‘INV-100’ , the list of tuples are [('1', 'Acne UV Gel - 30 SPF  ', '531'), ('2', 'Clindac-A mist spray ', '392'), ('3', 'AKNAYBAR soap ', '184')]. The first group is item number, second group is item name and third one for cost of item. 

Step 6:- Aim of function ‘invoice_list_extract(text)’ is to extract only item names purchased from these tuples. Using a ‘for’ loop, items are stored in ‘invoice_item_list’. 

Step 7:- Function ‘check_invoice_number()’,‘check_invoice_date()’,‘check_due_date()’ and ‘check_customer_Details()’ are used to check the accuracy of the extracted invoice number, invoice date, due date and customer details. The same pattern expression used for extracting invoice number was used here on ‘all_paragraphs_text’ (the text from pdf converted to word using online converter) and stored in variable ‘pattern’. Then, ‘if’ statement was used to check whether variable ‘pattern’ matches extracted invoice number using code. If it matches one point will be added to accuracy. The same method was implemented in functions ‘check_invoice_date()’,‘check_due_date()’ and ‘check_customer_Details()’ with the same patterns used for extracting  invoice date, due date and customer details. When the variable ‘pattern’ (extracted data from  ‘all_paragraphs_text’) matches with data, one point is added for accuracy.

Step 8:- In each pdf file, accuracy of four types of extracted data are checked and the accuracy percentage for one pdf file will be sum of accuracy from four types of data divided by four and whole multiplied by 100.

Step 9:- Extracted datas like invoice number, invoice date, due date, customer details and list of items purchased were successfully written to an excel sheet.

Step 10:- For trust determination of data extraction, the average of accuracy for all pdf files were estimated and then a threshold of 99% was used. If the combined accuracy (‘accuracy_whole’) is above 90%, then the system can be trusted for data extraction. If it is less, then it is unreliable. This was executed using an ‘if’ statement.

2)	Accuracy and trust Assessment approach :-
Overall accuracy (‘accuracy_whole’) of the system was 94.375%. This was above the threshold given in the assignment question of 90%. Therefore, the system is reliable or trust worthy for extracting data.

Breakdown of accuracy by invoice type and datafield :-
Invoice number accuracy=100%
Invoice date accuracy=100%
Due date accuracy=100%
Customer detail accuracy=77.5%

For accuracy check and trust determination logic procedure explained in steps 7,8  and 10 was followed.
