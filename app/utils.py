import os
import PyPDF2
from docx import Document
from typing import List
import uuid
from typing import List, Tuple

def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file_path: str) -> str:
    doc = Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def extract_text_from_txt(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
        
        if i + chunk_size >= len(words):
            break
    
    return chunks


def process_document(file_path: str, filename: str) -> Tuple[str, List[str]]:
    # Generate unique document ID
    document_id = str(uuid.uuid4())
    
    # Extract text based on file type
    if filename.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif filename.endswith('.docx'):
        text = extract_text_from_docx(file_path)
    else:  # Assume txt file
        text = extract_text_from_txt(file_path)
    
    # Chunk text
    chunks = chunk_text(text)
    
    return document_id, chunks

def search_documents(query: str, document_index, k: int = 5):
    return document_index.search(query, k)