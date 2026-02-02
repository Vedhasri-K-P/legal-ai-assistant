# ⚖️ Legal AI Assistant — Document Intelligence Prototype

A Python-based **legal document intelligence system** designed to analyze unstructured legal text and assist users through **context-aware querying**, **risk surfacing**, and **simplification of legal language**.

This project focuses on **practical LLM integration with real documents**, not generic chatbot behavior.

---

## 🧠 What This System Does

- Ingests legal documents (PDF / Word)
- Extracts and structures raw legal text
- Identifies important clauses and potential risk areas
- Enables users to ask questions grounded in uploaded documents
- Assists with legal understanding using controlled LLM responses

Built as a **prototype to explore document-grounded AI workflows**.

---

## 🏗️ System Flow

Document Upload
↓
Text Extraction (PDF / DOC)
↓
Preprocessing & Structuring
↓
Context Selection
↓
LLM Query (Groq API - Llama)
↓
User-Facing Explanation

---

## 🚀 Key Features

- 📄 **Document Analysis**  
  Parses uploaded legal documents to extract key clauses and highlight potential risk areas.

- 💬 **Context-Aware Legal Q&A**  
  Allows users to ask questions based on uploaded documents or predefined legal text, reducing generic LLM responses.

- 📊 **Insights Dashboard**  
  Displays simplified summaries and categorized legal insights for easier understanding.

- 🧠 **Legal Quiz Mode**  
  Interactive quiz to reinforce legal concepts and test understanding.

---

## 🔧 Tech Stack

- **Language:** Python  
- **Frontend / Prototyping:** Streamlit  
- **LLM API:** Groq (Llama-based models)  
- **Document Processing:** PyPDF2  
- **Data Handling:** Pandas  

---

## 📌 Design Choices & Tradeoffs

- Focused on **fast prototyping and usability** over heavy abstractions
- Prioritized document grounding to reduce hallucinated responses
- Used Streamlit to quickly validate workflows and user interactions
- Kept the architecture simple to allow future expansion into RAG or agent-based systems

---

## ▶️ Running the Project

```bash
git clone https://github.com/YOUR_USERNAME/legal-ai-assistant.git
cd legal-ai-assistant
pip install -r requirements.txt
streamlit run app.py

⚠️ Limitations

This is a prototype and not a substitute for professional legal advice

Responses depend on document quality and extracted context

Retrieval logic can be further improved with vector-based indexing

🔮 Future Improvements

Integrate vector-based retrieval for large document sets

Add citation-based responses

Improve clause risk scoring

Introduce multi-step reasoning workflows
