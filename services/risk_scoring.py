"""
Risk scoring service for legal documents
"""
from typing import Dict, List, Tuple, Any
import json
import os
from config.config import (
    RISK_THRESHOLD_LOW,
    RISK_THRESHOLD_MEDIUM,
    RISK_THRESHOLD_HIGH,
    DICTIONARIES_DIR
)

# Risk types and their weights
RISK_WEIGHTS = {
    "auto_renewal": 0.8,
    "termination_restrictions": 0.7,
    "unilateral_changes": 0.9,
    "liability_limitations": 0.6,
    "indemnification": 0.5,
    "jurisdiction": 0.4,
    "confidentiality": 0.3,
    "payment_terms": 0.4,
    "ip_rights": 0.6,
    "vague_terms": 0.7
}

def load_risk_keywords():
    """Load risk keywords from JSON file"""
    risk_keywords_path = os.path.join(DICTIONARIES_DIR, "risk_keywords.json")
    
    # Create default risk keywords if file doesn't exist
    if not os.path.exists(risk_keywords_path):
        default_risk_keywords = {
            "auto_renewal": [
                "automatically renew",
                "auto renewal",
                "auto-renewal"
            ],
            "termination_restrictions": [
                "may not terminate",
                "termination fee",
                "early termination"
            ],
            "unilateral_changes": [
                "sole discretion",
                "modify without notice",
                "unilaterally amend"
            ],
            "liability_limitations": [
                "no liability",
                "not be liable",
                "limit liability"
            ],
            "indemnification": [
                "indemnify",
                "hold harmless",
                "defend against"
            ]
        }
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(risk_keywords_path), exist_ok=True)
        
        # Save default risk keywords
        with open(risk_keywords_path, 'w') as f:
            json.dump(default_risk_keywords, f, indent=2)
        
        return default_risk_keywords
    
    # Load risk keywords from file
    try:
        with open(risk_keywords_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading risk keywords: {e}")
        return {}

def calculate_risk_score(risky_clauses: List[Dict[str, Any]]) -> Tuple[float, str]:
    """
    Calculate risk score based on detected risky clauses
    
    Args:
        risky_clauses: List of detected risky clauses
        
    Returns:
        Tuple of (risk_score, risk_level)
    """
    if not risky_clauses:
        return 0.0, "low"
    
    total_risk_weight = 0.0
    
    # Calculate weighted risk score
    for clause in risky_clauses:
        risk_type = clause.get("risk_type")
        risk_weight = RISK_WEIGHTS.get(risk_type, 0.5)  # Default weight of 0.5
        confidence = clause.get("confidence", 1.0)
        
        total_risk_weight += risk_weight * confidence
    
    # Normalize risk score (0.0 to 1.0)
    # We'll use a sigmoid-like function to ensure score is between 0 and 1
    # and increases faster with more high-weight risks
    num_clauses = len(risky_clauses)
    normalized_score = min(1.0, total_risk_weight / (num_clauses + 2))
    
    # Determine risk level
    if normalized_score < RISK_THRESHOLD_LOW:
        risk_level = "low"
    elif normalized_score < RISK_THRESHOLD_MEDIUM:
        risk_level = "medium"
    else:
        risk_level = "high"
    
    return normalized_score, risk_level

def get_risk_recommendations(risk_level: str) -> List[str]:
    """
    Get recommendations based on risk level
    
    Args:
        risk_level: Risk level ('low', 'medium', or 'high')
        
    Returns:
        List of recommendations
    """
    if risk_level == "low":
        return [
            "Review standard terms for clarity and understanding.",
            "Ensure all parties and dates are correctly identified.",
            "Verify that contract meets your business needs."
        ]
    elif risk_level == "medium":
        return [
            "Consider negotiating terms with higher risk weights.",
            "Have a legal professional review the contract before signing.",
            "Document any verbal agreements or clarifications in writing."
        ]
    else:  # high risk
        return [
            "Consult with legal counsel before proceeding.",
            "Negotiate to modify or remove high-risk clauses.",
            "Consider alternative options or contracts if available."
        ]