import fitz  # PyMuPDF

def question_answer_content(pdf_path):
    """
    Extracts text from a PDF file.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from the PDF.
    """
    try:
        pdf_document = fitz.open(pdf_path)
        extracted_text = ""

        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            extracted_text += page.get_text() + "\n"  # Add text from each page

        pdf_document.close()
        return extracted_text

    except Exception as e:
        print(f"Error occurred while extracting text: {e}")
        return ""
