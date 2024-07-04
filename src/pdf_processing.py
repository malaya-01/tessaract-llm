import fitz

def extract_text_from_pdfs(pdf_files):
    texts = []
    for pdf in pdf_files:
        with fitz.open(pdf) as doc:
            text = ""
            for page in doc:
                text += page.get_text()
            texts.append(text)
    return '\n\n'.join(texts)
