import PyPDF2
import sys

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page_num in range(len(reader.pages)):
                text += reader.pages[page_num].extract_text()
            return text
    except FileNotFoundError:
        return f"Error: The file at '{pdf_path}' was not found."
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_text.py <pdf_file_path>")
        sys.exit(1)

    pdf_file_path = sys.argv[1]
    extracted_text = extract_text_from_pdf(pdf_file_path)
    print(extracted_text)