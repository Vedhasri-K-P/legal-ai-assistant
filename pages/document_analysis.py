"""
Document analysis page for the Legal AI Platform
"""
import streamlit as st
import os
import time
import uuid

from config.config import SUPPORTED_LANGUAGES, MAX_FILE_SIZE_MB, SUPPORTED_EXTENSIONS
from utils.document_utils import (
    save_uploaded_file,
    extract_text_from_document,
    preprocess_text,
    extract_document_metadata
)
from models.summarization import summarize_document
from models.risk_detection import detect_risky_clauses
from models.simplification import simplify_legal_jargon
from services.risk_scoring import calculate_risk_score, get_risk_recommendations

def show_document_analysis_page():
    """Display the document analysis page"""
    
    # Main heading
    st.markdown('<h1 class="main-header">Document Analysis</h1>', unsafe_allow_html=True)
    
    # Create tabs for different document analysis views
    tabs = st.tabs(["Upload", "Summary", "Risk Analysis", "Simplification"])
    
    # Upload tab
    with tabs[0]:
        show_upload_tab()
    
    # Summary tab
    with tabs[1]:
        show_summary_tab()
    
    # Risk Analysis tab
    with tabs[2]:
        show_risk_analysis_tab()
    
    # Simplification tab
    with tabs[3]:
        show_simplification_tab()

def show_upload_tab():
    """Display the document upload tab"""
    
    st.markdown("### Upload Legal Document")
    st.markdown("Upload your legal document for analysis. Supported formats: PDF, DOCX")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "docx"],
        help=f"Maximum file size: {MAX_FILE_SIZE_MB}MB"
    )
    
    if uploaded_file is not None:
        # Check file size
        if uploaded_file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
            st.error(f"File size exceeds the {MAX_FILE_SIZE_MB}MB limit.")
            return
        
        # Check file extension
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        if file_ext not in SUPPORTED_EXTENSIONS:
            st.error(f"Unsupported file format. Please upload a PDF or DOCX file.")
            return
        
        # Show file details
        st.markdown(f"**File name:** {uploaded_file.name}")
        st.markdown(f"**File size:** {uploaded_file.size / (1024 * 1024):.2f} MB")
        
        # Process button
        if st.button("Process Document"):
            with st.spinner("Processing document..."):
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
                    
                    # Store the processed document
                    doc_data = {
                        "id": doc_id,
                        "filename": uploaded_file.name,
                        "file_type": file_ext,
                        "file_size": uploaded_file.size,
                        "raw_text": raw_text,
                        "processed_text": processed_text,
                        "metadata": metadata,
                        "summary": summary,
                        "risky_clauses": risky_clauses,
                        "risk_score": risk_score,
                        "risk_level": risk_level
                    }
                    
                    # Initialize if not exists
                    if 'uploaded_docs' not in st.session_state:
                        st.session_state.uploaded_docs = {}
                    if 'analyzed_docs' not in st.session_state:
                        st.session_state.analyzed_docs = {}
                    
                    # Store in session state
                    st.session_state.uploaded_docs[doc_id] = doc_data
                    st.session_state.analyzed_docs[doc_id] = doc_data
                    
                    # Set active document
                    st.session_state.active_doc_id = doc_id
                    
                    # Clean up temporary file
                    try:
                        os.remove(file_path)
                    except:
                        pass
                    
                    # Success message
                    st.success("Document processed successfully!")
                    
                    # Navigation message
                    st.markdown("👉 Navigate to the **Summary** tab to view document analysis.")
                    
                except Exception as e:
                    st.error(f"Error processing document: {str(e)}")

def show_summary_tab():
    """Display the document summary tab"""
    
    # Check if a document is selected
    if not hasattr(st.session_state, 'active_doc_id') or not st.session_state.active_doc_id:
        st.info("Please upload and process a document first.")
        return
    
    # Get the active document
    doc_id = st.session_state.active_doc_id
    if doc_id not in st.session_state.analyzed_docs:
        st.error("Document not found. Please upload a document first.")
        return
    
    doc_data = st.session_state.analyzed_docs[doc_id]
    
    # Display document summary
    st.markdown(f"### Document Summary: {doc_data.get('filename', 'Unknown')}")
    
    # Document metadata
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Document Information")
        metadata = doc_data.get("metadata", {})
        st.markdown(f"**Document Type:** {doc_data.get('file_type', 'Unknown').upper()[1:]}")
        st.markdown(f"**Size:** {doc_data.get('file_size', 0) / (1024 * 1024):.2f} MB")
        st.markdown(f"**Length:** {metadata.get('length', 0)} characters")
        st.markdown(f"**Sentences:** {metadata.get('num_sentences', 0)}")
        st.markdown(f"**Clauses:** {metadata.get('num_clauses', 0)}")
    
    with col2:
        st.markdown("#### Risk Assessment")
        risk_score = doc_data.get("risk_score", 0)
        risk_level = doc_data.get("risk_level", "low")
        
        # Display risk score
        st.markdown(f"**Risk Score:** {risk_score:.2f}")
        
        # Risk level text
        if risk_level == "low":
            st.markdown('<p class="risk-low">Low Risk</p>', unsafe_allow_html=True)
        elif risk_level == "medium":
            st.markdown('<p class="risk-medium">Medium Risk</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="risk-high">High Risk</p>', unsafe_allow_html=True)
        
        # Recommendations based on risk level
        st.markdown("#### Recommendations")
        recommendations = get_risk_recommendations(risk_level)
        for rec in recommendations:
            st.markdown(f"- {rec}")
    
    # Show document summary
    st.markdown("### Document Summary")
    summary = doc_data.get("summary", "No summary available.")
    st.markdown(f"{summary}")
    
    # Full text expandable section
    with st.expander("View Full Document Text"):
        st.markdown(doc_data.get("processed_text", "No text available."))

def show_risk_analysis_tab():
    """Display the risk analysis tab"""
    
    # Check if a document is selected
    if not hasattr(st.session_state, 'active_doc_id') or not st.session_state.active_doc_id:
        st.info("Please upload and process a document first.")
        return
    
    # Get the active document
    doc_id = st.session_state.active_doc_id
    if doc_id not in st.session_state.analyzed_docs:
        st.error("Document not found. Please upload a document first.")
        return
    
    doc_data = st.session_state.analyzed_docs[doc_id]
    
    # Display risk analysis
    st.markdown(f"### Risk Analysis: {doc_data.get('filename', 'Unknown')}")
    
    # Detailed risk analysis
    st.markdown("### Risky Clauses Detected")
    
    risky_clauses = doc_data.get("risky_clauses", [])
    if not risky_clauses:
        st.info("No risky clauses detected in this document.")
    else:
        # Display each risky clause
        for i, clause in enumerate(risky_clauses):
            risk_type = clause.get("risk_type", "unknown").replace("_", " ").title()
            confidence = clause.get("confidence", 0)
            clause_text = clause.get("text", "")
            
            # Create expandable section for each clause
            with st.expander(f"{risk_type} ({confidence:.2f} confidence)"):
                st.markdown(f"**Risk Type:** {risk_type}")
                st.markdown(f"**Confidence:** {confidence:.2f}")
                
                # Clause text
                st.markdown("**Clause Text:**")
                st.markdown(f"<div class='highlight'>{clause_text}</div>", unsafe_allow_html=True)

def show_simplification_tab():
    """Display the document simplification tab"""
    
    # Check if a document is selected
    if not hasattr(st.session_state, 'active_doc_id') or not st.session_state.active_doc_id:
        st.info("Please upload and process a document first.")
        return
    
    # Get the active document
    doc_id = st.session_state.active_doc_id
    if doc_id not in st.session_state.analyzed_docs:
        st.error("Document not found. Please upload a document first.")
        return
    
    doc_data = st.session_state.analyzed_docs[doc_id]
    
    # Display simplification
    st.markdown(f"### Legal Jargon Simplification: {doc_data.get('filename', 'Unknown')}")
    
    # Explanation
    st.markdown("""
    Legal documents often use complex terminology and sentence structures. 
    This tab shows the original legal text alongside a simplified "plain English" version.
    """)
    
    # Only run simplification when button is clicked
    if st.button("Simplify Document"):
        with st.spinner("Simplifying document..."):
            try:
                # Get the text to simplify
                original_text = doc_data.get("processed_text", "")
                
                # Use the simplify_legal_jargon function to simplify the text
                simplified_text = simplify_legal_jargon(original_text)
                
                # Store the simplified text in the document data
                doc_data["simplified_text"] = simplified_text
                st.session_state.analyzed_docs[doc_id] = doc_data
                
                st.success("Document simplified successfully!")
                st.rerun()  # Rerun to display the simplified text
            except Exception as e:
                st.error(f"Error simplifying document: {str(e)}")
    
    # Display simplified text if available
    if "simplified_text" in doc_data and doc_data["simplified_text"]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Original Text")
            st.markdown(doc_data.get("processed_text", ""))
        
        with col2:
            st.markdown("### Simplified Text")
            st.markdown(doc_data.get("simplified_text", ""))