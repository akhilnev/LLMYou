import pypdf
import docx

def parse_file_to_string(file_path: str) -> str:
    """
    Parses text from a PDF or Word file and returns it as a string.

    Parameters:
    file_path (str): The path to the file to be parsed.

    Returns:
    str: The parsed text.
    """
    if file_path.lower().endswith('.pdf'):
        return parse_pdf_to_string(file_path)
    elif file_path.lower().endswith('.docx'):
        return parse_docx_to_string(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a PDF or DOCX file.")

def parse_pdf_to_string(pdf_path: str) -> str:
    """
    Parses text from a PDF file.

    Parameters:
    pdf_path (str): The path to the PDF file.

    Returns:
    str: The parsed text.
    """
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = pypdf.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def parse_docx_to_string(docx_path: str) -> str:
    """
    Parses text from a DOCX file.

    Parameters:
    docx_path (str): The path to the DOCX file.

    Returns:
    str: The parsed text.
    """
    doc = docx.Document(docx_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

user_details = parse_file_to_string("AK_Resume.pdf")
user_details += parse_file_to_string("Akhilesh_Linkedin_Resume_2024.pdf")
print(user_details) 

# Example usage:
# file_path = 'path_to_your_file.pdf' or 'path_to_your_file.docx'
# file_text = parse_file_to_string(file_path)
# print(file_text)