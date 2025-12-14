"""
Legal chatbot page for the Legal AI Platform
"""
import streamlit as st
import random
import json
import os
from config.config import DATA_DIR

# --- HELPER: Generate Response using Groq ---
def get_ai_response(user_query, chat_history):
    """
    Get response from Groq API using the client stored in session state.
    """
    client = st.session_state.get('groq_client')
    
    if not client:
        return "⚠️ Error: AI Client not connected. Please check your API Key in the .env file."

    try:
        # 1. Prepare the messages list
        messages = [
            {
                "role": "system", 
                "content": (
                    "You are an expert Indian Legal Assistant. "
                    "Provide accurate, helpful, and clear legal information based on Indian laws (IPC, CrPC, Contract Act, etc.). "
                    "If you are unsure, state that. Always clarify that you are an AI and this is not professional legal advice."
                    "Keep answers concise and structured."
                )
            }
        ]
        
        # 2. Add history context (limit to last 5 pairs to save tokens)
        for msg in chat_history[-10:]: 
            messages.append({"role": msg["role"], "content": msg["content"]})
            
        # 3. Add current query
        messages.append({"role": "user", "content": user_query})

        # 4. Call Groq API
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile", # Using the model you tested successfully
            temperature=0.5,
            max_tokens=1024,
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"⚠️ API Error: {str(e)}"

# --- QUIZ DATA LOADING ---
def load_quiz_data():
    """Load quiz data from JSON file or create a default set"""
    # Create directory if it doesn't exist
    os.makedirs(os.path.join(DATA_DIR, "training"), exist_ok=True)
    quiz_data_path = os.path.join(DATA_DIR, "training", "legal_quiz.json")
    
    # Default quiz data if file doesn't exist
    if not os.path.exists(quiz_data_path):
        default_quiz_data = [
            {
                "question": "Under Indian Contract Act, what is the minimum age for entering into a valid contract?",
                "options": ["16 years", "18 years", "21 years", "No minimum age"],
                "correct_answer": 1,
                "explanation": "According to the Indian Contract Act, a person must be at least 18 years old to enter into a valid contract. Contracts made by minors (under 18) are typically void."
            },
            {
                "question": "Which of the following is NOT an essential element of a valid contract?",
                "options": ["Offer and acceptance", "Free consent", "Written documentation", "Lawful consideration"],
                "correct_answer": 2,
                "explanation": "Written documentation is NOT an essential element of a valid contract in India. Verbal contracts can be valid as long as they contain other essential elements."
            },
            {
                "question": "Under the Right to Information Act, within how many days must a public authority provide information?",
                "options": ["10 days", "30 days", "45 days", "60 days"],
                "correct_answer": 1,
                "explanation": "Under the Right to Information Act, 2005, a public authority is required to provide information within 30 days of receiving the request."
            },
            {
                "question": "What is the limitation period for filing a suit for recovery of movable property under the Limitation Act?",
                "options": ["1 year", "3 years", "7 years", "12 years"],
                "correct_answer": 1,
                "explanation": "Under the Limitation Act, 1963, the limitation period for filing a suit for recovery of movable property is 3 years."
            },
            {
                "question": "Which of the following is a valid ground for divorce under the Hindu Marriage Act?",
                "options": ["Different political opinions", "Conversion to another religion", "Financial disagreements", "Different food preferences"],
                "correct_answer": 1,
                "explanation": "Conversion to another religion is a valid ground for divorce under the Hindu Marriage Act, 1955."
            }
        ]
        
        # Save default quiz data
        with open(quiz_data_path, 'w') as f:
            json.dump(default_quiz_data, f, indent=2)
        
        return default_quiz_data
    
    # Load quiz data from file
    try:
        with open(quiz_data_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading quiz data: {e}")
        return []

def show_chatbot_page():
    """Display the legal chatbot page"""
    
    # Main heading
    st.markdown('<h1 class="main-header">Legal Chatbot & Quiz</h1>', unsafe_allow_html=True)
    
    # Create tabs for chatbot and quiz
    tabs = st.tabs(["Legal Chatbot", "Legal Quiz"])
    
    # Chatbot tab
    with tabs[0]:
        show_chatbot_tab()
    
    # Quiz tab
    with tabs[1]:
        show_quiz_tab()

def show_chatbot_tab():
    """Display the legal chatbot tab"""
    
    # Check API Status
    if not st.session_state.get('groq_client'):
        st.error("❌ API Not Connected. Please check your .env file for GROQ_API_KEY.")
        st.info("You can still use the Quiz tab, but the Chatbot requires the API key.")
    
    # Custom CSS for better chat styling
    st.markdown("""
    <style>
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 20px;
        margin-bottom: 20px;
    }
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 18px;
        margin: 10px 0;
        margin-left: 20%;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .assistant-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 18px;
        margin: 10px 0;
        margin-right: 20%;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .message-label {
        font-weight: bold;
        font-size: 0.9em;
        margin-bottom: 8px;
        opacity: 0.9;
    }
    .message-content {
        line-height: 1.6;
        font-size: 1em;
    }
    .info-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        border-left: 4px solid #667eea;
        color: #1a1a1a;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("### 💬 Legal Chatbot")
    
    # Info box
    st.markdown("""
    <div class="info-box">
        <strong>ℹ️ How to use:</strong> Ask questions about legal concepts, processes, or documents. 
        The chatbot uses <strong>Llama-3 (via Groq)</strong> to answer queries based on Indian Law.
        <br>
        <strong>⚠️ Note:</strong> This chatbot provides general information only and not legal advice.
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize chat history if not already in session
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    if not st.session_state.chat_history:
        st.markdown("""
        <div style="text-align: center; padding: 40px; color: #666;">
            <h3>👋 Welcome to Legal Assistant!</h3>
            <p>Ask me any legal question to get started.</p>
        </div>
        """, unsafe_allow_html=True)
    
    for message in st.session_state.chat_history:
        role = message.get("role", "user")
        content = message.get("content", "")
        
        if role == "user":
            st.markdown(f"""
            <div class="user-message">
                <div class="message-label">👤 You</div>
                <div class="message-content">{content}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="assistant-message">
                <div class="message-label">⚖️ Legal Assistant</div>
                <div class="message-content">{content}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Use a form to handle input submission
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        with col1:
            user_input = st.text_input("💭 Ask a legal question:", key="chat_input_field", label_visibility="collapsed", placeholder="Type your legal question here...")
        with col2:
            submit_button = st.form_submit_button("📤 Send", use_container_width=True)
        
        if submit_button and user_input and user_input.strip():
            # 1. Add user message to chat history
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_input
            })
            
            # 2. Get response from Groq API
            with st.spinner("Analyzing Indian Laws..."):
                response_text = get_ai_response(user_input, st.session_state.chat_history)
            
            # 3. Add assistant message to chat history
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response_text
            })
            
            # 4. Rerun to update chat display
            st.rerun()
    
    # Clear chat button
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        if st.button("🗑️ Clear Chat", key="clear_button", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    # Sample questions
    st.markdown("---")
    st.markdown("### 💡 Sample Questions")
    
    sample_questions = [
        "What is the legal age to marry in India?",
        "How do I file a police complaint (FIR)?",
        "What are my rights as a consumer?",
        "Explain the process of divorce in India."
    ]
    
    cols = st.columns(2)
    for i, q_text in enumerate(sample_questions):
        with cols[i % 2]:
            if st.button(q_text, key=f"sample_{i}", use_container_width=True):
                # Add to history
                st.session_state.chat_history.append({"role": "user", "content": q_text})
                # Get Response
                with st.spinner("Analyzing..."):
                    response_text = get_ai_response(q_text, st.session_state.chat_history)
                # Add response
                st.session_state.chat_history.append({"role": "assistant", "content": response_text})
                st.rerun()

def show_quiz_tab():
    """Display the legal quiz tab"""
    
    # Custom CSS for quiz
    st.markdown("""
    <style>
    .quiz-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
    .quiz-question {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border-left: 5px solid #667eea;
        font-size: 1.1em;
        font-weight: 600;
        color: #333;
    }
    .score-badge {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        display: inline-block;
        font-weight: bold;
        margin: 10px 0;
    }
    .explanation-box {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 15px;
        border-radius: 10px;
        margin-top: 15px;
        color: #333;
        border-left: 4px solid #f5576c;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="quiz-header"><h2>📚 Legal Knowledge Quiz</h2><p>Test your legal knowledge with interactive questions!</p></div>', unsafe_allow_html=True)
    
    # Load quiz data
    quiz_data = load_quiz_data()
    
    if not quiz_data:
        st.error("No quiz questions available.")
        return
    
    # Initialize quiz state if not already in session
    if 'quiz_state' not in st.session_state:
        st.session_state.quiz_state = {
            "current_question": 0,
            "score": 0,
            "questions_answered": set(),
            "last_answer": None,
            "last_correct": None,
            "available_questions": list(range(len(quiz_data)))
        }
    
    # Current question index
    current_idx = st.session_state.quiz_state["current_question"]
    
    # Ensure current index is valid
    if len(quiz_data) > 0:
        current_idx = current_idx % len(quiz_data)
        st.session_state.quiz_state["current_question"] = current_idx
        
        # Get current question
        question = quiz_data[current_idx]
        
        # Display score
        total_answered = len(st.session_state.quiz_state["questions_answered"])
        st.markdown(f'<div class="score-badge">📊 Score: {st.session_state.quiz_state["score"]} / {total_answered}</div>', unsafe_allow_html=True)
        
        # Display question
        st.markdown(f"**Question {current_idx + 1} of {len(quiz_data)}**")
        st.markdown(f'<div class="quiz-question">{question["question"]}</div>', unsafe_allow_html=True)
        
        # Check if this question has been answered
        already_answered = current_idx in st.session_state.quiz_state["questions_answered"]
        
        # Display options as buttons or show previous answer
        if not already_answered:
            st.markdown("**Select your answer:**")
            for i, option in enumerate(question["options"]):
                if st.button(f"{chr(65+i)}. {option}", key=f"option_{i}", use_container_width=True):
                    # Record answer
                    st.session_state.quiz_state["last_answer"] = i
                    st.session_state.quiz_state["last_correct"] = (i == question["correct_answer"])
                    
                    # Update score
                    if i == question["correct_answer"]:
                        st.session_state.quiz_state["score"] += 1
                    
                    # Mark question as answered
                    st.session_state.quiz_state["questions_answered"].add(current_idx)
                    
                    # Rerun to show result
                    st.rerun()
        else:
            # Show options with correct one highlighted
            st.markdown("**Your answer:**")
            for i, option in enumerate(question["options"]):
                if i == question["correct_answer"]:
                    st.success(f"✅ **{chr(65+i)}. {option}** (Correct Answer)")
                elif i == st.session_state.quiz_state["last_answer"]:
                    st.error(f"❌ {chr(65+i)}. {option} (Your Answer)")
                else:
                    st.info(f"{chr(65+i)}. {option}")
            
            # Show explanation
            st.markdown(f'<div class="explanation-box"><strong>💡 Explanation:</strong><br>{question["explanation"]}</div>', unsafe_allow_html=True)
        
        # Navigation buttons
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Previous Question", use_container_width=True):
                st.session_state.quiz_state["current_question"] = (current_idx - 1) % len(quiz_data)
                st.rerun()
        
        with col2:
            if st.button("Next Question", use_container_width=True):
                st.session_state.quiz_state["current_question"] = (current_idx + 1) % len(quiz_data)
                st.rerun()
        
        # Display score
        st.markdown("---")
        st.markdown(f"**Current Score:** {st.session_state.quiz_state['score']} / {len(st.session_state.quiz_state['questions_answered'])}")
        
        # Progress bar
        progress = len(st.session_state.quiz_state["questions_answered"]) / len(quiz_data)
        st.progress(progress)
    
    # Reset quiz button
    if st.button("Reset Quiz"):
        available_indices = list(range(len(quiz_data)))
        random.shuffle(available_indices)
        
        st.session_state.quiz_state = {
            "current_question": 0,
            "score": 0,
            "questions_answered": set(),
            "last_answer": None,
            "last_correct": None,
            "available_questions": available_indices
        }
        st.rerun()