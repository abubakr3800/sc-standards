"""
AI Standards Training System

A comprehensive AI system for processing, understanding, and comparing 
lighting standards from PDF documents in multiple languages.
"""

__version__ = "1.0.0"
__author__ = "Short Circuit Company"
__email__ = "Scc@shortcircuitcompany.com"

from .core.config import config
# from .core.pdf_processor import PDFProcessor  # Commented out to avoid spaCy import issues
# from .models.ai_trainer import AIStandardsTrainer  # Commented out to avoid heavy imports
# from .models.comparison_model import StandardsComparisonModel  # Commented out to avoid heavy imports

__all__ = [
    "config"
    # "PDFProcessor", 
    # "AIStandardsTrainer",
    # "StandardsComparisonModel"
]
