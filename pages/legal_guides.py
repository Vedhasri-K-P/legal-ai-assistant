"""
Legal guides page for the Legal AI Platform
"""
import streamlit as st
import random
from typing import Dict, List, Any
from services.groupq_service import GroupQService

def show_legal_guides_page():
    """Display the legal guides page"""
    
    # Initialize Groq service if not already initialized
    if 'groupq_service' not in st.session_state:
        st.session_state.groupq_service = GroupQService()
    
    # Main heading
    st.markdown('<h1 class="main-header">AI-Generated Legal Guides</h1>', unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    Get personalized legal guides on various topics. Whether you're trying to understand a legal process,
    prepare for a legal proceeding, or learn about your rights, these AI-generated guides can help.
    """)
    
    st.markdown("**Note:** These guides provide general information only and not legal advice.")
    
    # Topic selection
    st.markdown("### Select a Topic or Enter Your Own")
    
    # Common legal topics
    common_topics = [
        "Filing a Consumer Complaint",
        "Starting a Business in India",
        "Understanding Rental Agreements",
        "Filing an RTI Application",
        "Divorce Procedure in India",
        "Motor Vehicle Accident Claims",
        "Copyright Protection",
        "Employment Contract Rights",
        "Property Registration Process",
        "Wills and Succession Planning"
    ]
    
    # Topic selection method
    topic_method = st.radio(
        "Choose a method to select a topic:",
        ["Select from common topics", "Enter your own topic"]
    )
    
    if topic_method == "Select from common topics":
        selected_topic = st.selectbox(
            "Select a legal topic",
            common_topics
        )
    else:
        selected_topic = st.text_input(
            "Enter a legal topic",
            placeholder="e.g., How to file a trademark in India"
        )
    
    # Generate guide button
    if selected_topic and st.button("Generate Guide"):
        with st.spinner(f"Generating comprehensive guide on '{selected_topic}'..."):
            # Get guide content from Groq API
            guide_content = st.session_state.groupq_service.generate_legal_guide(selected_topic)
            
            # Store in session state
            st.session_state.current_guide = {
                "topic": selected_topic,
                "content": guide_content
            }
        
        # Show success message
        st.success(f"Guide on '{selected_topic}' generated successfully!")
    
    # Display guide if available
    if hasattr(st.session_state, 'current_guide') and st.session_state.current_guide:
        st.markdown("---")
        st.markdown(f"### Guide: {st.session_state.current_guide['topic']}")
        
        # Display guide content (expected to be in Markdown format)
        st.markdown(st.session_state.current_guide['content'])
        
        # Download button
        guide_content = st.session_state.current_guide['content']
        topic = st.session_state.current_guide['topic']
        
        st.download_button(
            label="📥 Download Guide as Markdown",
            data=guide_content,
            file_name=f"{topic.replace(' ', '_')}_guide.md",
            mime="text/markdown"
        )
    
    # Display example guides or suggestions
    if not hasattr(st.session_state, 'current_guide') or not st.session_state.current_guide:
        st.markdown("---")
        st.markdown("### Example Topics")
        
        # Display random suggestions each time
        sample_topics = random.sample(common_topics, 6)
        
        # Display topic suggestions in columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("#### Personal Legal Matters")
            for topic in sample_topics[:3]:
                st.markdown(f"* {topic}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("#### Business Legal Matters")
            for topic in sample_topics[3:]:
                st.markdown(f"* {topic}")
            st.markdown('</div>', unsafe_allow_html=True)