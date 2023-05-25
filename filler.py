import json
import re
import PyPDF2
import openai
from fpdf import FPDF

# Set OpenAI API key
openai.api_key = "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"

# pdf which has the information
input_pdf_path = "Bio-data3.pdf"

#pdf which is the form to fill
output_pdf_path = "Emp.pdf"

# add name and path for the result as filled form
result_pdf_path = "new.pdf"

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from the PDF.
    """
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        extracted_text = ""
        for i in range(len(reader.pages)):
            page = reader.pages[i]
            page_text = page.extract_text()
            page_text = re.sub(r' {2,}', '\n', page_text)  # Replace consecutive spaces with newline characters
            extracted_text += page_text
    return extracted_text

def analyze_text_with_openai(input_text, output_text):
    """
    Analyzes input text using OpenAI and generates output text.

    Args:
        input_text (str): Input text for analysis.
        output_text (str): Output text to be filled in.

    Returns:
        str: Edited output text.
    """
    prompt = f"extract information from input text and fill in output text\nreturn only edited output text without any other changes\ninput text: {input_text}\noutput text: {output_text}\ndo not perform any additional tasks"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.25,
    )
    return response.choices[0].text.strip()

def create_pdf_from_text(text, output_file_path):
    """
    Creates a PDF file from the given text.

    Args:
        text (str): Text content for the PDF.
        output_file_path (str): Path to save the PDF file.
    """
    pdf = FPDF()

    # Add a page
    pdf.add_page()

    # Set style and size of font
    pdf.set_font("Arial", size=15)

    final_text = text.split("\n\n")
    for t in final_text:
        cleaned_text = "".join(char for char in t if ord(char) < 256)
        pdf.cell(200, 10, txt=cleaned_text, ln=1)

    pdf.output(output_file_path)




def main_function(input_pdf_path, output_pdf_path, result_pdf_path):
    input_text = extract_text_from_pdf(input_pdf_path)
    output_text = extract_text_from_pdf(output_pdf_path)
    new_output = analyze_text_with_openai(input_text, output_text)
    create_pdf_from_text(new_output, result_pdf_path)

if __name__=="__main__":
    main_function(input_pdf_path, output_pdf_path, result_pdf_path)