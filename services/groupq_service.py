"""
Service for interacting with the Groq API
"""
import json
import requests
from typing import Dict, List, Any, Optional, Union

from config.config import GROUPQ_API_KEY

class GroupQService:
    """Service for interacting with the Groq API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Groq API service
        
        Args:
            api_key: Groq API key (defaults to config value)
        """
        self.api_key = api_key or GROUPQ_API_KEY
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        
        if not self.api_key:
            print("Warning: Groq API key not set. Using mock responses.")
    
    def _make_groq_request(self, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 1024) -> str:
        """
        Make a request to the Groq API
        
        Args:
            messages: List of chat messages
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            
        Returns:
            AI response text
        """
        if not self.api_key:
            return f"⚠️ API Key not configured. Please add your GROUPQ_API_KEY to the .env file to enable AI responses."
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": 1,
                "stream": False
            }
            
            print(f"Making request to Groq API...")  # Debug
            print(f"API Key (first 10 chars): {self.api_key[:10]}...")  # Debug
            
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=60  # Increased timeout for longer responses
            )
            
            print(f"Response status code: {response.status_code}")  # Debug
            
            # Handle different error codes
            if response.status_code == 401:
                return "⚠️ Authentication failed. Please check your Groq API key in the .env file. Visit https://console.groq.com to get a valid API key."
            elif response.status_code == 429:
                return "⚠️ Rate limit exceeded. Please wait a moment and try again."
            elif response.status_code >= 500:
                return "⚠️ Groq API server error. Please try again in a few moments."
            
            response.raise_for_status()
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                return "⚠️ Unexpected response format from API. Please try again."
        
        except requests.exceptions.Timeout:
            return "⚠️ Request timed out. The AI service is taking too long to respond. Please try again."
        except requests.exceptions.RequestException as e:
            print(f"Groq API error: {e}")
            error_msg = str(e)
            if "401" in error_msg:
                return "⚠️ Authentication failed. Your API key may be invalid or expired. Please check your Groq API key at https://console.groq.com"
            return f"⚠️ Connection error: {error_msg}. Please check your internet connection and try again."
        except Exception as e:
            print(f"Unexpected error: {e}")
            return f"⚠️ An unexpected error occurred: {str(e)}"
    
    def summarize_text(self, text: str, max_length: int = 500) -> str:
        """
        Summarize text using the Groq API
        
        Args:
            text: Text to summarize
            max_length: Maximum summary length
            
        Returns:
            Summarized text
        """
        messages = [
            {
                "role": "system",
                "content": """You are a legal document summarization expert specializing in Indian legal documents. Provide clear, concise summaries that highlight key clauses, obligations, parties involved, and important terms. 

When analyzing documents, consider Indian legal context, Indian contract law principles, and common practices in Indian legal documents."""
            },
            {
                "role": "user",
                "content": f"Please summarize the following legal document in approximately {max_length} words. Focus on Indian legal context if applicable:\n\n{text}"
            }
        ]
        
        return self._make_groq_request(messages, temperature=0.3)
    
    def simplify_text(self, text: str) -> str:
        """
        Simplify legal jargon to plain English
        
        Args:
            text: Legal text to simplify
            
        Returns:
            Simplified text
        """
        messages = [
            {
                "role": "system",
                "content": "You are a legal language simplification expert. Convert complex legal jargon into simple, easy-to-understand English that anyone can comprehend."
            },
            {
                "role": "user",
                "content": f"Please simplify the following legal text into plain English:\n\n{text}"
            }
        ]
        
        return self._make_groq_request(messages, temperature=0.3)
    
    def chat_query(self, query: str, chat_history: Optional[List[Dict[str, str]]] = None) -> str:
        """
        Get a response to a chat query about legal topics
        
        Args:
            query: User's query
            chat_history: Previous chat history
            
        Returns:
            Response to the query
        """
        messages = [
            {
                "role": "system",
                "content": """You are a helpful legal information assistant specializing in Indian law. You provide clear, accurate information about legal concepts, processes, and terminology with a focus on the Indian legal system.

Important guidelines:
- ALWAYS provide answers based on Indian law, Indian Constitution, and Indian legal framework UNLESS the user specifically asks about another country
- Reference specific Indian acts, sections, and legal provisions (e.g., IPC, CrPC, Indian Constitution, Hindu Marriage Act, Companies Act 2013, etc.)
- Provide detailed, informative answers about legal topics
- Use numbered lists and structured formatting when helpful
- Explain concepts in simple terms while being accurate
- Mention relevant Supreme Court and High Court precedents when applicable
- Always include a disclaimer that this is general information, not legal advice
- Be comprehensive but concise
- Answer ANY legal question the user asks, no matter what topic
- When discussing procedures, use Indian court systems, Indian legal processes, and Indian regulations
- Use Indian legal terminology and context"""
            }
        ]
        
        # Add chat history if available (last 5 messages for context)
        if chat_history:
            for msg in chat_history[-10:]:  # Last 5 exchanges (10 messages)
                if msg.get("role") and msg.get("content"):
                    messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
        
        # Add current query
        messages.append({
            "role": "user",
            "content": query
        })
        
        return self._make_groq_request(messages, temperature=0.7)
    
    def generate_legal_guide(self, topic: str) -> str:
        """
        Generate a comprehensive legal guide on a specified topic
        
        Args:
            topic: Legal topic
            
        Returns:
            Generated guide content in markdown format
        """
        messages = [
            {
                "role": "system",
                "content": """You are a legal education expert specializing in Indian law. Create EXTREMELY DETAILED, comprehensive, well-structured guides on legal topics based on the Indian legal system, Indian Constitution, and Indian regulations.

CRITICAL: Always provide information in the context of Indian law unless explicitly asked about another jurisdiction.

Your guides must be COMPREHENSIVE and DETAILED - include every single step, every document, every fee, every timeline. Make it so detailed that someone with NO legal knowledge can follow it successfully."""
            },
            {
                "role": "user",
                "content": f"""Create an EXTREMELY DETAILED and COMPREHENSIVE legal guide about '{topic}' specifically for India. This guide should be thorough enough that someone with zero legal knowledge can successfully navigate the process.

## Required Structure:

### 1. Introduction and Overview (Detailed)
- What exactly is {topic} in the Indian legal context
- Why it matters in India (constitutional and practical reasons)
- Who can use this (eligibility criteria)
- When to use this process

### 2. Applicable Indian Laws and Regulations (Complete List)
- ALL relevant Acts with full names and years
- Specific sections and sub-sections that apply
- Constitutional provisions if applicable
- Recent amendments (with dates)
- Rules and regulations under each Act
- Relevant notifications and circulars

### 3. EXTREMELY DETAILED Step-by-Step Procedures in India
Break down the ENTIRE process into granular steps:

For EACH step, include:
a) **What to do** (exact action required)
b) **Where to go** (specific office/court/online portal with address/URL)
c) **Documents required** (complete list with format specifications)
d) **How to prepare each document** (templates, format, contents)
e) **Forms to fill** (form numbers, where to get, how to fill)
f) **Fees to pay** (exact amounts in ₹, payment methods)
g) **Timeline** (how long this step takes)
h) **What happens next** (immediate next step)
i) **Common issues** at this step and solutions

Include:
- Pre-filing requirements and preparations
- Document collection and preparation
- Where to file (physical address and online options)
- How to file (offline and online procedures)
- Payment of fees (challan, online payment, DD)
- Submission process
- Acknowledgment receipt
- Case number allocation
- Notice serving procedures
- Hearing dates
- Appearance requirements
- Evidence submission
- Arguments
- Interim orders
- Final orders
- Implementation/execution of orders
- Appeals process
- Follow-up actions

### 4. Documents Required (Exhaustive Checklist)
For EACH document:
- Document name
- Why it's needed
- Where to obtain it
- Format required (original/copy/notarized)
- Number of copies needed
- Valid period
- Alternative if not available

### 5. Fees and Costs (Complete Breakdown)
- Court fees (category-wise)
- Stamp duty (if applicable)
- Lawyer fees (typical range)
- Documentation costs
- Notary charges
- Miscellaneous expenses
- Total estimated cost (minimum to maximum)
- Fee exemptions/waivers available

### 6. Timeline Expectations (Realistic)
- Each step duration
- Total minimum time
- Total maximum time
- Factors that can delay
- How to expedite

### 7. Key Concepts and Legal Terminology (Explained)
- Every legal term explained in simple language
- Indian legal terms with meanings
- Important definitions from relevant Acts

### 8. Important Considerations for India
- State-specific variations (list major states)
- Urban vs rural differences
- Jurisdiction rules (detailed)
- Practical challenges in Indian system
- Language issues
- Documentation requirements in different states

### 9. Common Mistakes to Avoid (With Solutions)
For EACH common mistake:
- What the mistake is
- Why people make it
- What happens if you make it
- How to avoid it
- How to fix it if already made

### 10. Relevant Case Law
- 5-10 important Supreme Court judgments with:
  - Case name and citation
  - Year
  - Key ruling
  - How it affects this topic
- Important High Court judgments

### 11. Practical Tips and Best Practices
- Do's and Don'ts
- Insider tips from legal practice
- How to work with lawyers
- How to prepare for hearings
- Documentation best practices
- Communication strategies
- Legal aid options in India

### 12. Troubleshooting Common Issues
- What if petition is rejected?
- What if documents are incomplete?
- What if opposite party doesn't respond?
- What if hearing is delayed?
- What if order is not favorable?
- Solutions for each scenario

### 13. Alternative Options
- Mediation
- Arbitration
- Lok Adalat
- Online Dispute Resolution
- When to use each alternative

### 14. Additional Resources
- Government websites (with exact URLs)
- Relevant ministry/department
- Helpline numbers
- Legal aid organizations
- Online portals
- Mobile apps (official)
- Downloadable forms
- Sample documents
- FAQs pages

### 15. Frequently Asked Questions
- 10-15 most common questions with detailed answers

Format everything in clear markdown with:
- Proper headings (###, ####)
- Bullet points for lists
- Numbered lists for sequential steps
- Bold for emphasis
- Tables where helpful
- Clear organization

Make it EXTREMELY DETAILED - this should be a complete manual that someone can follow from start to finish without any prior legal knowledge. Include real examples where helpful."""
            }
        ]
        
        return self._make_groq_request(messages, temperature=0.4, max_tokens=8000)  # Much higher limit for detailed guides