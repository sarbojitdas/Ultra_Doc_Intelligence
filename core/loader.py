import fitz

def load_document(file):
    content = file.file.read()
    doc = fitz.open(stream=content, filetype="pdf")
    return "\n".join(page.get_text() for page in doc)