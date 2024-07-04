import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
print("This is the current dir: "+ os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from pdf_processing import extract_text_from_pdfs
from image_processing import text_to_image_and_extract
from document_processing import get_documents_from_file, create_vector_db
from chat_handler import create_chain, process_chat

import fitz

from dotenv import load_dotenv
load_dotenv()
from langchain_core.messages import HumanMessage, AIMessage


def handle_pdf_text_extraction(pdf_files):
    combined_text = extract_text_from_pdfs(pdf_files)
    extracted_text, buffer = text_to_image_and_extract(combined_text)

    output_format = input("Which format? ['pdf' or 'txt']: ")
    if output_format == 'pdf':
        pdf_output = fitz.open()
        page = pdf_output.new_page(width=1000, height=20 * (len(combined_text.split('\n')) + 1))
        img = fitz.Pixmap(buffer)
        page.insert_image(page.rect, pixmap=img)
        pdf_output.save('data/output/output.pdf')
        print("Saved extracted text to data/output/output.pdf")
    elif output_format == 'txt':
        with open('data/output/output.txt', 'w', encoding='utf-8') as f:
            f.write(extracted_text)
        print("Saved extracted text to data/output/output.txt")

    return extracted_text

if __name__ == '__main__':
    # Part 1: Handle PDF/Text extraction
    pdf_files = ['data/input/dummy.pdf', 'data/input/pdf-table.pdf', 'data/input/solar1.pdf']
    extracted_text = handle_pdf_text_extraction(pdf_files)

    # Save extracted text to a temporary file for document processing
    temp_file = 'data/output/output.txt'
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(extracted_text)

    # Part 2: Document processing and chat handling
    docs = get_documents_from_file(temp_file)
    vector_store = create_vector_db(docs)
    chain = create_chain(vector_store)

    chat_history = []

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        response = process_chat(chain, user_input, chat_history)
        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=response))

        print("Assistant: ", response)
