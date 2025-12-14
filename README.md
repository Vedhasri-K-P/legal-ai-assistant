# ⚖️ Legal AI Assistant

An AI-powered legal document analysis and assistance tool built with Python and Streamlit. This application helps users simplify legal jargon, analyze contracts for risks and answer legal queries using the Groq API (Llama-3).

# 🚀 Features
* 📄 Document Analysis:Upload PDF/Word documents to extract key clauses and detect potential risks.
* 💬 AI Legal Chatbot:Ask questions about Indian laws (IPC, CrPC, Contract Act) and get instant answers.
* 📊 Insights Dashboard:Visual breakdown of document risks and categories.
* 🧠 Quiz Mode:Test your legal knowledge with an interactive quiz.

## 🛠️ Tech Stack
* Frontend:Streamlit
* AI Model:Llama(via Groq API)
* Data Processing:Pandas, PyPDF2
* Language:Python

## ⚙️ Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/legal-ai-assistant.git](https://github.com/YOUR_USERNAME/legal-ai-assistant.git)
    cd legal-ai-assistant
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up Environment Variables:**
    * Create a `.env` file in the root directory.
    * Add your Groq API key:
        ```
        GROQ_API_KEY=gsk_your_api_key_here
        ```

4.  **Run the App:**
    ```bash
    streamlit run app.py
    ```
