"""
Configuration settings for the AI Standards Training System
"""
import os
from pathlib import Path
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the AI training system"""
    
    # Base paths
    BASE_DIR = Path(__file__).parent.parent.parent  # Go up to project root
    DATA_DIR = BASE_DIR / "data"
    MODELS_DIR = BASE_DIR / "models"
    UPLOADS_DIR = BASE_DIR / "uploads"
    OUTPUTS_DIR = BASE_DIR / "outputs"
    BASE_PDFS_DIR = BASE_DIR / "base"
    
    # Create directories if they don't exist
    for dir_path in [DATA_DIR, MODELS_DIR, UPLOADS_DIR, OUTPUTS_DIR, BASE_PDFS_DIR]:
        dir_path.mkdir(exist_ok=True)
    
    # PDF processing settings
    PDF_PROCESSING = {
        "max_pages": 1000,
        "supported_languages": ["en", "de", "fr", "es", "it", "pt", "nl", "sv", "no", "da", "fi"],
        "extraction_methods": ["pdfplumber", "pymupdf", "pdfminer"],
        "chunk_size": 1000,
        "chunk_overlap": 200
    }
    
    # AI model settings
    AI_MODELS = {
        "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
        "translation_model": "Helsinki-NLP/opus-mt-en-mul",
        "classification_model": "distilbert-base-uncased",
        "max_sequence_length": 512,
        "batch_size": 16,
        "learning_rate": 2e-5,
        "num_epochs": 3
    }
    
    # Database settings
    DATABASE = {
        "path": DATA_DIR / "standards.db",
        "vector_db_path": DATA_DIR / "vector_db"
    }
    
    # Comparison model settings
    COMPARISON = {
        "similarity_threshold": 0.7,
        "max_comparisons": 100,
        "feature_weights": {
            "illuminance": 0.3,
            "color_rendering": 0.2,
            "glare_control": 0.2,
            "energy_efficiency": 0.15,
            "safety": 0.15
        }
    }
    
    # API settings
    API = {
        "host": os.getenv("API_HOST", "0.0.0.0"),
        "port": int(os.getenv("API_PORT", 8000)),
        "debug": os.getenv("API_DEBUG", "true").lower() == "true"
    }
    
    # Logging settings
    LOGGING = {
        "level": os.getenv("LOG_LEVEL", "INFO"),
        "format": "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
        "file": BASE_DIR / "logs" / os.getenv("LOG_FILE", "app.log")
    }
    
    # Create logs directory
    (BASE_DIR / "logs").mkdir(exist_ok=True)

# Global config instance
config = Config()
