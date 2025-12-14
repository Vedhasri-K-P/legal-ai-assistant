"""
Document summarization model for legal documents
"""
import nltk
from config.config import SUMMARIZATION_MODEL

# Ensure NLTK punkt tokenizer is available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

def summarize_document(text: str) -> str:
    """
    Summarize a legal document
    
    Args:
        text: Document text
        
    Returns:
        Summarized text
    """
    # Simple extractive summarization
    sentences = nltk.sent_tokenize(text)
    
    # If very few sentences, return as is
    if len(sentences) <= 5:
        return text
    
    # Calculate sentence scores based on position and length
    scores = {}
    for i, sentence in enumerate(sentences):
        # Position score (first few and last few sentences are more important)
        position_score = 1.0
        if i < 3:
            position_score = 1.5  # Boost first few sentences
        elif i >= len(sentences) - 3:
            position_score = 1.2  # Boost last few sentences
            
        # Length score (penalize very short or very long sentences)
        words = len(sentence.split())
        if words < 5:
            length_score = 0.8
        elif words > 30:
            length_score = 0.9
        else:
            length_score = 1.0
            
        # Keyword score (boost sentences with important legal keywords)
        legal_keywords = ["agree", "contract", "party", "oblig", "right", "term", "condit", "law"]
        keyword_count = sum(1 for keyword in legal_keywords if keyword in sentence.lower())
        keyword_score = 1.0 + (0.1 * keyword_count)
        
        # Final score
        scores[i] = position_score * length_score * keyword_score
    
    # Select top sentences (about 20% of original)
    num_sentences = max(5, int(len(sentences) * 0.2))
    top_indices = sorted(scores, key=scores.get, reverse=True)[:num_sentences]
    
    # Reconstruct summary in original order
    summary_sentences = [sentences[i] for i in sorted(top_indices)]
    summary = " ".join(summary_sentences)
    
    return summary