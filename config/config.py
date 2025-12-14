"""
Configuration settings for the Legal AI Platform
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GROUPQ_API_KEY = os.getenv("GROUPQ_API_KEY", "")
GROUPQ_API_URL = os.getenv("GROUPQ_API_URL", "https://api.groupq.ai/v1")

# Model Configuration
SUMMARIZATION_MODEL = os.getenv("SUMMARIZATION_MODEL", "groupq")  # Options: 'groupq', 'local'
RISK_DETECTION_MODEL = os.getenv("RISK_DETECTION_MODEL", "rule_based")  # Options: 'rule_based', 'tfidf'
TRANSLATION_MODEL = os.getenv("TRANSLATION_MODEL", "googletrans")  # Options: 'indictrans', 'googletrans', 'marianmt'
SIMPLIFICATION_MODEL = os.getenv("SIMPLIFICATION_MODEL", "groupq")  # Options: 'groupq', 'local'

# Path Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
TRAINING_DATA_DIR = os.path.join(DATA_DIR, "training")
DICTIONARIES_DIR = os.path.join(DATA_DIR, "dictionaries")
TEMP_DIR = os.path.join(BASE_DIR, "temp")

# Translation Configuration
SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "mr": "Marathi",
    "ta": "Tamil",
    "te": "Telugu",
    "kn": "Kannada",
    "ml": "Malayalam",
    "bn": "Bengali",
    "gu": "Gujarati",
    "pa": "Punjabi",
}

# Risk Scoring Configuration
RISK_THRESHOLD_LOW = 0.3
RISK_THRESHOLD_MEDIUM = 0.6
RISK_THRESHOLD_HIGH = 0.8

# Document Processing Configuration
MAX_FILE_SIZE_MB = 10
SUPPORTED_EXTENSIONS = [".pdf", ".docx"]

# Ensure directories exist
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(TRAINING_DATA_DIR, exist_ok=True)
os.makedirs(DICTIONARIES_DIR, exist_ok=True)