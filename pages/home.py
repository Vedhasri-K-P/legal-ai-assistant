"""
Home page for the Legal AI Platform
"""
import streamlit as st

def show_home_page():
    """Display the home page of the application"""
    
    # Main heading
    st.markdown('<h1 class="main-header">Legal AI Platform</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subheader">AI-powered legal document analysis and insights</p>', unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    Welcome to the Legal AI Platform! This tool helps you analyze legal documents, 
    identify risks, simplify legal jargon, and gain valuable insights from your legal documents.
    """)
    
    # Features overview
    st.markdown("---")
    st.markdown("### Key Features")
    
    # Create columns for features
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 📄 Document Analysis")
        st.markdown("""
        * Upload PDF and DOCX legal documents
        * Get AI-powered document summaries
        * Identify risky clauses and potential issues
        * Calculate overall risk scores
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 🔄 Translation & Simplification")
        st.markdown("""
        * Translate legal documents to regional languages
        * Convert complex legal jargon to plain English
        * Side-by-side comparison of original and simplified text
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 📊 Legal Insights")
        st.markdown("""
        * View analytics on your document portfolio
        * Track risk trends over time
        * Identify common risk patterns
        * Compare documents side-by-side
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 💬 Legal Chatbot & Guides")
        st.markdown("""
        * Interactive legal chatbot for questions
        * Generate legal guides on specific topics
        * Learn about legal concepts and processes
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Call to action
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("Get Started with Document Analysis", use_container_width=True):
            st.session_state.page = 'Document Analysis'
            st.rerun()