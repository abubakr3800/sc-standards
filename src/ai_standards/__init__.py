"""
AI Standards Training System

A comprehensive AI system for processing, understanding, and comparing 
lighting standards from PDF documents in multiple languages.
"""

__version__ = "1.0.0"
__author__ = "AI Standards Team"
__email__ = "team@aistandards.com"

from .core.config import config
from .core.pdf_processor import PDFProcessor
from .models.ai_trainer import AIStandardsTrainer
from .models.comparison_model import StandardsComparisonModel

__all__ = [
    "config",
    "PDFProcessor", 
    "AIStandardsTrainer",
    "StandardsComparisonModel"
]
