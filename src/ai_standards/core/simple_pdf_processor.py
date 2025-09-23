"""
Simplified PDF Processing Module for Standards Documents
Handles text extraction without complex NLP dependencies
"""
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re
import json
from datetime import datetime

import pdfplumber
import fitz  # PyMuPDF
from pdfminer.high_level import extract_text
from langdetect import detect, LangDetectException
from loguru import logger

from .config import config

class SimplePDFProcessor:
    """Simplified PDF processor that works without complex dependencies"""
    
    def __init__(self):
        self.supported_languages = ["en", "de", "fr", "es", "it", "nl", "sv", "no", "da", "fi"]
        
    def extract_text_from_pdf(self, pdf_path: Path, method: str = "pdfplumber") -> str:
        """
        Extract text from PDF using specified method
        
        Args:
            pdf_path: Path to PDF file
            method: Extraction method ("pdfplumber", "pymupdf", "pdfminer")
            
        Returns:
            Extracted text
        """
        try:
            if method == "pdfplumber":
                return self._extract_with_pdfplumber(pdf_path)
            elif method == "pymupdf":
                return self._extract_with_pymupdf(pdf_path)
            elif method == "pdfminer":
                return self._extract_with_pdfminer(pdf_path)
            else:
                raise ValueError(f"Unknown extraction method: {method}")
        except Exception as e:
            logger.error(f"Text extraction failed with {method}: {e}")
            # Try fallback methods
            if method != "pdfplumber":
                return self._extract_with_pdfplumber(pdf_path)
            elif method != "pymupdf":
                return self._extract_with_pymupdf(pdf_path)
            else:
                return self._extract_with_pdfminer(pdf_path)
    
    def _extract_with_pdfplumber(self, pdf_path: Path) -> str:
        """Extract text using pdfplumber"""
        text_parts = []
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(f"--- Page {page_num} ---\n{page_text}")
                except Exception as e:
                    logger.warning(f"Failed to extract text from page {page_num}: {e}")
        return "\n\n".join(text_parts)
    
    def _extract_with_pymupdf(self, pdf_path: Path) -> str:
        """Extract text using PyMuPDF"""
        text_parts = []
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            try:
                page = doc.load_page(page_num)
                page_text = page.get_text()
                if page_text:
                    text_parts.append(f"--- Page {page_num + 1} ---\n{page_text}")
            except Exception as e:
                logger.warning(f"Failed to extract text from page {page_num + 1}: {e}")
        doc.close()
        return "\n\n".join(text_parts)
    
    def _extract_with_pdfminer(self, pdf_path: Path) -> str:
        """Extract text using pdfminer"""
        try:
            return extract_text(pdf_path)
        except Exception as e:
            logger.error(f"PDFMiner extraction failed: {e}")
            return ""
    
    def extract_tables_from_pdf(self, pdf_path: Path) -> List[Dict]:
        """Extract tables from PDF"""
        tables = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    page_tables = page.extract_tables()
                    for table_num, table in enumerate(page_tables, 1):
                        if table and len(table) > 1:  # Ensure table has data
                            tables.append({
                                "page": page_num,
                                "table_number": table_num,
                                "data": table,
                                "title": f"Table {table_num} from Page {page_num}"
                            })
        except Exception as e:
            logger.error(f"Table extraction failed: {e}")
        return tables
    
    def detect_language(self, text: str) -> str:
        """Detect language of text"""
        try:
            # Use first 1000 characters for language detection
            sample_text = text[:1000].strip()
            if not sample_text:
                return "en"
            
            detected_lang = detect(sample_text)
            if detected_lang in self.supported_languages:
                return detected_lang
            else:
                logger.warning(f"Unsupported language detected: {detected_lang}, defaulting to English")
                return "en"
        except LangDetectException:
            logger.warning("Could not detect language, defaulting to English")
            return "en"
        except Exception as e:
            logger.error(f"Language detection error: {e}")
            return "en"
    
    def extract_metadata(self, text: str, file_path: Path) -> Dict:
        """Extract metadata from text and file path"""
        metadata = {
            "file_name": file_path.name,
            "file_path": str(file_path),
            "file_size": file_path.stat().st_size if file_path.exists() else 0,
            "language": self.detect_language(text),
            "categories": [],
            "keywords": [],
            "standard_type": "Unknown",
            "standard_number": "Unknown"
        }
        
        # Extract standard information from text
        text_lower = text.lower()
        
        # Detect standard types
        if "en 12464" in text_lower or "european standard" in text_lower:
            metadata["standard_type"] = "European Standard"
            metadata["categories"].append("european_standard")
        elif "breeam" in text_lower:
            metadata["standard_type"] = "BREEAM Guidance"
            metadata["categories"].append("breeam")
        elif "iso" in text_lower:
            metadata["standard_type"] = "ISO Standard"
            metadata["categories"].append("iso_standard")
        elif "ansi" in text_lower or "american national standard" in text_lower:
            metadata["standard_type"] = "ANSI Standard"
            metadata["categories"].append("ansi_standard")
        
        # Extract standard numbers
        standard_patterns = [
            r"en\s+\d+[-\w]*",
            r"iso\s+\d+[-\w]*",
            r"ansi\s+\d+[-\w]*",
            r"bs\s+\d+[-\w]*",
            r"din\s+\d+[-\w]*"
        ]
        
        for pattern in standard_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                metadata["standard_number"] = matches[0].upper()
                break
        
        # Extract keywords
        lighting_keywords = [
            "illuminance", "lux", "luminance", "color rendering", "cri", "ugr", "glare",
            "lighting", "luminaire", "lamp", "led", "fluorescent", "halogen",
            "daylight", "artificial light", "task lighting", "ambient lighting",
            "energy efficiency", "power density", "lighting controls"
        ]
        
        for keyword in lighting_keywords:
            if keyword in text_lower:
                metadata["keywords"].append(keyword)
        
        # Add general categories
        if "illuminance" in text_lower or "lux" in text_lower:
            metadata["categories"].append("illuminance")
        if "color" in text_lower or "cri" in text_lower:
            metadata["categories"].append("color_rendering")
        if "glare" in text_lower or "ugr" in text_lower:
            metadata["categories"].append("glare_control")
        if "energy" in text_lower or "efficiency" in text_lower:
            metadata["categories"].append("energy_efficiency")
        if "daylight" in text_lower:
            metadata["categories"].append("daylight")
        
        return metadata
    
    def process_pdf(self, pdf_path: Path, target_language: str = "en") -> Optional[Dict]:
        """
        Process a PDF file and extract all relevant information
        
        Args:
            pdf_path: Path to PDF file
            target_language: Target language for processing
            
        Returns:
            Dictionary containing processed document data
        """
        try:
            logger.info(f"Processing PDF: {pdf_path.name}")
            
            # Extract text
            text_content = self.extract_text_from_pdf(pdf_path)
            if not text_content.strip():
                logger.error(f"No text extracted from {pdf_path.name}")
                return None
            
            # Extract tables
            tables = self.extract_tables_from_pdf(pdf_path)
            
            # Extract metadata
            metadata = self.extract_metadata(text_content, pdf_path)
            
            # Create processed document
            processed_doc = {
                "file_path": str(pdf_path),
                "file_name": pdf_path.name,
                "language": metadata["language"],
                "text_content": text_content,
                "tables": tables,
                "metadata": metadata,
                "processing_info": {
                    "processed_at": datetime.now().isoformat(),
                    "processing_method": "simple_pdf_processor",
                    "confidence_score": 0.8
                }
            }
            
            logger.info(f"Successfully processed {pdf_path.name}")
            return processed_doc
            
        except Exception as e:
            logger.error(f"Failed to process {pdf_path.name}: {e}")
            import traceback
            traceback.print_exc()
            return None
