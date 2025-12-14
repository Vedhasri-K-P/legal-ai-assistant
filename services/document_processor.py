"""
Document processing service for the Legal AI Platform
"""
import os
import uuid
from typing import Dict, List, Any, Tuple

from utils.document_utils import (
    save_uploaded_file, 
    extract_text_from_document, 
    preprocess_text,
    extract_document_metadata
)
from models.summarization import summarize_document
from models.risk_detection import detect_risky_clauses
from models.simplification import simplify_legal_jargon
from services.risk_scoring import calculate_risk_score

class DocumentProcessor:
    """Service for processing legal documents"""
    
    def __init__(self):
        """Initialize the document processor"""
        pass
    
    def process_document(self, uploaded_file) -> Dict[str, Any]:
        """
        Process an uploaded document and return analysis results
        
        Args:
            uploaded_file: Streamlit UploadedFile object
            
        Returns:
            Dict containing analysis results
        """
        try:
            # Generate a unique ID for this document
            doc_id = str(uuid.uuid4())
            
            # Save the uploaded file
            file_path = save_uploaded_file(uploaded_file)
            
            # Extract text from the document
            raw_text = extract_text_from_document(file_path)
            
            # Preprocess the text
            processed_text = preprocess_text(raw_text)
            
            # Extract metadata
            metadata = extract_document_metadata(processed_text)
            
            # Summarize the document
            summary = summarize_document(processed_text)
            
            # Detect risky clauses
            risky_clauses = detect_risky_clauses(processed_text)
            
            # Calculate risk score
            risk_score, risk_level = calculate_risk_score(risky_clauses)
            
            # Simplify legal jargon
            simplified_text = simplify_legal_jargon(processed_text)
            
            # Clean up temporary file
            try:
                os.remove(file_path)
            except:
                pass
            
            # Return the processed document
            return {
                "id": doc_id,
                "filename": uploaded_file.name,
                "file_type": os.path.splitext(uploaded_file.name)[1].lower(),
                "file_size": uploaded_file.size,
                "raw_text": raw_text,
                "processed_text": processed_text,
                "metadata": metadata,
                "summary": summary,
                "risky_clauses": risky_clauses,
                "risk_score": risk_score,
                "risk_level": risk_level,
                "simplified_text": simplified_text
            }
        
        except Exception as e:
            # Handle errors
            return {
                "error": str(e)
            }
    
    def translate_document(self, doc_data: Dict[str, Any], target_language: str) -> Dict[str, Any]:
        """
        Translate the document to the target language
        
        Args:
            doc_data: Document data dictionary
            target_language: Target language code
            
        Returns:
            Updated document data with translations
        """
        from models.translation import translate_text
        
        try:
            # Translate document text
            translated_text = translate_text(doc_data["processed_text"], target_language)
            
            # Translate summary
            translated_summary = translate_text(doc_data["summary"], target_language)
            
            # Update document data
            doc_data["translations"] = doc_data.get("translations", {})
            doc_data["translations"][target_language] = {
                "text": translated_text,
                "summary": translated_summary
            }
            
            return doc_data
        
        except Exception as e:
            # Handle translation errors
            return {
                **doc_data,
                "translation_error": str(e)
            }
    
    def get_document_comparison(self, doc_id1: str, doc_id2: str) -> Dict[str, Any]:
        """
        Compare two documents and return comparison data
        
        Args:
            doc_id1: First document ID
            doc_id2: Second document ID
            
        Returns:
            Comparison results
        """
        # This method can be implemented later to compare two documents
        pass