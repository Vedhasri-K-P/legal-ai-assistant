"""
Main Streamlit application for Legal AI Platform
"""
import os
import sys
import streamlit as st
from dotenv import load_dotenv  # Added: Load environment variables
from groq import Groq           # Added: Groq API Client

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import pages
from pages.home import show_home_page
from pages.document_analysis import show_document_analysis_page
from pages.insights import show_insights_page
from pages.chatbot import show_chatbot_page
from pages.legal_guides import show_legal_guides_page

# Page configuration
st.set_page_config(
    page_title="Legal AI Platform",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
def load_css():
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5em;
            color: #1E3A8A;
            margin-bottom: 0.5em;
        }
        .subheader {
            font-size: 1.5em;
            color: #475569;
            margin-bottom: 1em;
        }
        .risk-high {
            color: #DC2626;
            font-weight: bold;
        }
        .risk-medium {
            color: #F59E0B;
            font-weight: bold;
        }
        .risk-low {
            color: #10B981;
            font-weight: bold;
        }
        .highlight {
            background-color: #FEF3C7;
            padding: 0.2em;
            border-radius: 0.2em;
        }
        .card {
            background-color: #F8FAFC;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .sidebar-header {
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 1em;
        }
        /* New Styles for API Status */
        .status-connected {
            color: #10B981;
            font-size: 0.8em;
            font-weight: bold;
        }
        .status-error {
            color: #DC2626;
            font-size: 0.8em;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state & Groq Connection
def init_session_state():
    # 1. Navigation & Data State
    if 'page' not in st.session_state:
        st.session_state.page = 'Home'
    if 'uploaded_docs' not in st.session_state:
        st.session_state.uploaded_docs = {}
    if 'analyzed_docs' not in st.session_state:
        st.session_state.analyzed_docs = {}
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # 2. Initialize Groq API (New Logic)
    if 'groq_client' not in st.session_state:
        load_dotenv()  # Load variables from .env file
        api_key = os.getenv("GROQ_API_KEY")
        
        if api_key:
            try:
                # Initialize the client and store it in session state
                st.session_state.groq_client = Groq(api_key=api_key)
                st.session_state.api_status = "connected"
                # Optional: specific model to use
                st.session_state.model_name = "llama-3.3-70b-versatile" 
            except Exception as e:
                st.session_state.groq_client = None
                st.session_state.api_status = f"error: {str(e)}"
        else:
            st.session_state.groq_client = None
            st.session_state.api_status = "missing_key"

# Sidebar navigation
def sidebar():
    with st.sidebar:
        st.markdown('<div class="sidebar-header">Legal AI Platform</div>', unsafe_allow_html=True)
        
        # --- API Status Indicator (New) ---
        if st.session_state.get('api_status') == "connected":
            st.markdown('🟢 <span class="status-connected">AI System Online</span>', unsafe_allow_html=True)
        elif st.session_state.get('api_status') == "missing_key":
            st.markdown('🔴 <span class="status-error">API Key Missing</span>', unsafe_allow_html=True)
            st.caption("Check .env file")
        else:
            st.markdown('⚠️ <span class="status-error">Connection Failed</span>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation
        st.subheader("Navigation")
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = 'Home'
            st.rerun()
        if st.button("📄 Document Analysis", use_container_width=True):
            st.session_state.page = 'Document Analysis'
            st.rerun()
        if st.button("📊 Insights Dashboard", use_container_width=True):
            st.session_state.page = 'Insights'
            st.rerun()
        if st.button("💬 Legal Chatbot", use_container_width=True):
            st.session_state.page = 'Chatbot'
            st.rerun()
        if st.button("📚 Legal Guides", use_container_width=True):
            st.session_state.page = 'Legal Guides'
            st.rerun()
            
        # App info
        st.sidebar.markdown("---")
        st.sidebar.info(
            "This platform helps you analyze legal documents, detect risks, "
            "simplify legal jargon, and provide insights about your legal documents."
        )
        
        # Footer
        st.sidebar.markdown("---")
        st.sidebar.caption("© 2025 Legal AI Platform")

def main():
    # Initialize app
    load_css()
    init_session_state()
    sidebar()
    
    # Debug information (Uncomment if needed)
    # st.write(f"Current page: {st.session_state.page}")
    
    # Show selected page
    if st.session_state.page == 'Home':
        show_home_page()
    elif st.session_state.page == 'Document Analysis':
        show_document_analysis_page()
    elif st.session_state.page == 'Insights':
        show_insights_page()
    elif st.session_state.page == 'Chatbot':
        show_chatbot_page()
    elif st.session_state.page == 'Legal Guides':
        show_legal_guides_page()
    else:
        # Fallback to home page if unknown page is selected
        st.warning(f"Unknown page: {st.session_state.page}. Showing home page instead.")
        show_home_page()

if __name__ == "__main__":
    main()