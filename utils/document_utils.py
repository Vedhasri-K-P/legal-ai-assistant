"""
Utility functions for handling legal documents
"""
import os
import re
import tempfile
from pathlib import Path
import PyPDF2
import docx
import nltk
from typing import Dict, List, Any

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

def save_uploaded_file(uploaded_file) -> str:
    """Save an uploaded file to a temporary location and return the path"""
    try:
        # Create a temporary file with the same extension
        suffix = Path(uploaded_file.name).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.getvalue())
            return tmp.name
    except Exception as e:
        raise Exception(f"Error saving uploaded file: {e}")

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text content from a PDF file"""
    text = ""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {e}")
    return text

def extract_text_from_docx(file_path: str) -> str:
    """Extract text content from a DOCX file"""
    try:
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        raise Exception(f"Error extracting text from DOCX: {e}")
    return text

def extract_text_from_document(file_path: str) -> str:
    """Extract text from a document based on its file extension"""
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext == '.docx':
        return extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

def preprocess_text(text: str) -> str:
    """Preprocess extracted text for better analysis"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove headers/footers (common patterns)
    text = re.sub(r'Page \d+ of \d+', '', text)
    text = re.sub(r'^\d+$', '', text, flags=re.MULTILINE)
    
    # Clean up special characters
    text = re.sub(r'[\u0000-\u001F\u007F-\u009F]', '', text)
    
    return text.strip()

def split_into_sentences(text: str) -> List[str]:
    """Split text into sentences using NLTK's sentence tokenizer"""
    return nltk.sent_tokenize(text)

def split_into_clauses(text: str) -> List[str]:
    """Split legal text into logical clauses"""
    # Basic splitting by common legal separators
    clauses = []
    raw_splits = re.split(r';|\.(?=\s[A-Z])', text)
    
    for split in raw_splits:
        if split.strip():
            clauses.append(split.strip())
    
    return clauses

def extract_document_metadata(text: str) -> Dict[str, Any]:
    """Extract useful metadata from the document text"""
    metadata = {
        "length": len(text),
        "num_sentences": len(split_into_sentences(text)),
        "num_clauses": len(split_into_clauses(text))
    }
    
    return metadata