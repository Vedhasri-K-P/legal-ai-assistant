"""
Risk detection model for identifying risky clauses in legal documents
"""
import os
import re
from typing import Dict, List, Any
from config.config import RISK_DETECTION_MODEL
from services.risk_scoring import load_risk_keywords

def detect_risky_clauses(text: str) -> List[Dict[str, Any]]:
    """
    Detect risky clauses in the document text
    
    Args:
        text: Document text
        
    Returns:
        List of detected risky clauses
    """
    # Load risk keywords
    risk_keywords = load_risk_keywords()
    
    risky_clauses = []
    
    # Split text into paragraphs
    paragraphs = text.split('\n\n')
    
    # Track current position in the text
    current_pos = 0
    
    for paragraph in paragraphs:
        if not paragraph.strip():
            # Skip empty paragraphs
            current_pos += len(paragraph) + 2  # +2 for newlines
            continue
        
        # Check if paragraph contains any risk keywords
        for risk_type, keywords in risk_keywords.items():
            for keyword in keywords:
                if keyword.lower() in paragraph.lower():
                    # Found a risk keyword
                    start_index = current_pos
                    end_index = current_pos + len(paragraph)
                    
                    # Calculate confidence based on keyword match strength
                    # More exact matches have higher confidence
                    matches = re.findall(re.escape(keyword.lower()), paragraph.lower())
                    confidence = min(0.9, 0.5 + 0.2 * len(matches))
                    
                    # Add the risky clause
                    risky_clauses.append({
                        "text": paragraph,
                        "risk_type": risk_type,
                        "start_index": start_index,
                        "end_index": end_index,
                        "confidence": confidence
                    })
                    
                    # Move to next risk type once we find a match
                    break
        
        # Update position
        current_pos += len(paragraph) + 2  # +2 for newlines
    
    # Remove duplicates (same paragraph, different risk types)
    unique_clauses = []
    seen_indices = set()
    
    for clause in risky_clauses:
        index_key = f"{clause['start_index']}-{clause['end_index']}"
        if index_key not in seen_indices:
            unique_clauses.append(clause)
            seen_indices.add(index_key)
    
    return unique_clauses