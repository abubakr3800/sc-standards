"""
PDF Processing Module for Standards Documents
Handles text extraction, language detection, and preprocessing
"""
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re
import pandas as pd

import pdfplumber
import fitz  # PyMuPDF
from pdfminer.high_level import extract_text
from langdetect import detect, LangDetectException
from googletrans import Translator
import spacy
from loguru import logger

from .config import config

class PDFProcessor:
    """Handles PDF text extraction and preprocessing"""
    
    def __init__(self):
        self.translator = Translator()
        self.nlp_models = {}
        self._load_nlp_models()
        
    def _load_nlp_models(self):
        """Load spaCy models for different languages"""
        languages = config.PDF_PROCESSING["supported_languages"]
        for lang in languages:
            try:
                if lang == "en":
                    self.nlp_models[lang] = spacy.load("en_core_web_sm")
                else:
                    # Try to load language model, fallback to English if not available
                    try:
                        self.nlp_models[lang] = spacy.load(f"{lang}_core_news_sm")
                    except OSError:
                        logger.warning(f"Language model for {lang} not found, using English")
                        self.nlp_models[lang] = spacy.load("en_core_web_sm")
            except OSError:
                logger.error(f"Could not load spaCy model for {lang}")
                
    def extract_text_from_pdf(self, pdf_path: Path, method: str = "pdfplumber") -> str:
        """
        Extract text from PDF using specified method
        
        Args:
            pdf_path: Path to PDF file
            method: Extraction method ('pdfplumber', 'pymupdf', 'pdfminer')
            
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
            logger.error(f"Error extracting text from {pdf_path}: {e}")
            return ""
    
    def _extract_with_pdfplumber(self, pdf_path: Path) -> str:
        """Extract text using pdfplumber"""
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages[:config.PDF_PROCESSING["max_pages"]]:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    
    def _extract_with_pymupdf(self, pdf_path: Path) -> str:
        """Extract text using PyMuPDF"""
        text = ""
        doc = fitz.open(pdf_path)
        for page_num in range(min(len(doc), config.PDF_PROCESSING["max_pages"])):
            page = doc[page_num]
            text += page.get_text() + "\n"
        doc.close()
        return text
    
    def _extract_with_pdfminer(self, pdf_path: Path) -> str:
        """Extract text using pdfminer"""
        return extract_text(pdf_path)
    
    def detect_language(self, text: str) -> str:
        """
        Detect language of the text
        
        Args:
            text: Input text
            
        Returns:
            Language code (e.g., 'en', 'de', 'fr')
        """
        try:
            # Use first 1000 characters for language detection
            sample_text = text[:1000]
            detected_lang = detect(sample_text)
            return detected_lang
        except LangDetectException:
            logger.warning("Could not detect language, defaulting to English")
            return "en"
    
    def translate_text(self, text: str, target_language: str = "en") -> str:
        """
        Translate text to target language
        
        Args:
            text: Input text
            target_language: Target language code
            
        Returns:
            Translated text
        """
        try:
            # Split text into chunks for translation
            chunks = self._split_text_into_chunks(text, 4000)
            translated_chunks = []
            
            for chunk in chunks:
                if chunk.strip():
                    result = self.translator.translate(chunk, dest=target_language)
                    translated_chunks.append(result.text)
            
            return " ".join(translated_chunks)
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return text
    
    def _split_text_into_chunks(self, text: str, max_length: int) -> List[str]:
        """Split text into chunks of specified maximum length"""
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 > max_length:
                if current_chunk:
                    chunks.append(" ".join(current_chunk))
                    current_chunk = [word]
                    current_length = len(word)
                else:
                    chunks.append(word)
                    current_length = 0
            else:
                current_chunk.append(word)
                current_length += len(word) + 1
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks
    
    def preprocess_text(self, text: str, language: str = "en") -> str:
        """
        Preprocess text for better AI processing
        
        Args:
            text: Input text
            language: Language code
            
        Returns:
            Preprocessed text
        """
        # Clean text
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)\[\]\"\']', '', text)  # Remove special chars
        text = text.strip()
        
        # Use spaCy for advanced preprocessing if model is available
        if language in self.nlp_models:
            try:
                doc = self.nlp_models[language](text)
                # Extract sentences and clean them
                sentences = [sent.text.strip() for sent in doc.sents if len(sent.text.strip()) > 10]
                text = " ".join(sentences)
            except Exception as e:
                logger.warning(f"spaCy preprocessing failed: {e}")
        
        return text
    
    def extract_structured_data(self, text: str) -> Dict[str, List[str]]:
        """
        Extract structured data from standards text
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with extracted data categories
        """
        structured_data = {
            "illuminance_values": [],
            "color_rendering_index": [],
            "glare_ratings": [],
            "energy_requirements": [],
            "safety_requirements": [],
            "measurement_methods": [],
            "compliance_standards": []
        }
        
        # Extract illuminance values (lux)
        illuminance_pattern = r'(\d+(?:\.\d+)?)\s*(?:lux|lx|lm/m²)'
        structured_data["illuminance_values"] = re.findall(illuminance_pattern, text, re.IGNORECASE)
        
        # Extract color rendering index values
        cri_pattern = r'CRI\s*[:\-]?\s*(\d+(?:\.\d+)?)|Ra\s*[:\-]?\s*(\d+(?:\.\d+)?)'
        cri_matches = re.findall(cri_pattern, text, re.IGNORECASE)
        structured_data["color_rendering_index"] = [match[0] or match[1] for match in cri_matches]
        
        # Extract glare ratings
        glare_pattern = r'UGR\s*[:\-]?\s*(\d+(?:\.\d+)?)|glare\s*rating\s*[:\-]?\s*(\d+(?:\.\d+)?)'
        glare_matches = re.findall(glare_pattern, text, re.IGNORECASE)
        structured_data["glare_ratings"] = [match[0] or match[1] for match in glare_matches]
        
        # Extract energy requirements
        energy_pattern = r'(\d+(?:\.\d+)?)\s*(?:W/m²|W/m2|watts?/m²|watts?/m2)'
        structured_data["energy_requirements"] = re.findall(energy_pattern, text, re.IGNORECASE)
        
        # Extract safety requirements
        safety_keywords = ['safety', 'emergency', 'evacuation', 'fire', 'hazard']
        for keyword in safety_keywords:
            pattern = rf'{keyword}[^.]*\.'
            matches = re.findall(pattern, text, re.IGNORECASE)
            structured_data["safety_requirements"].extend(matches)
        
        # Extract measurement methods
        method_keywords = ['measurement', 'test', 'procedure', 'method']
        for keyword in method_keywords:
            pattern = rf'{keyword}[^.]*\.'
            matches = re.findall(pattern, text, re.IGNORECASE)
            structured_data["measurement_methods"].extend(matches)
        
        # Extract compliance standards
        standard_pattern = r'(?:EN|ISO|IEC|ANSI|ASHRAE|CIE)\s*\d+(?:[-:]\d+)*(?:[A-Z]\d+)?'
        structured_data["compliance_standards"] = re.findall(standard_pattern, text)
        
        return structured_data
    
    def chunk_text(self, text: str) -> List[Dict[str, any]]:
        """
        Split text into overlapping chunks for processing
        
        Args:
            text: Input text
            
        Returns:
            List of text chunks with metadata
        """
        chunk_size = config.PDF_PROCESSING["chunk_size"]
        overlap = config.PDF_PROCESSING["chunk_overlap"]
        
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk_words = words[i:i + chunk_size]
            chunk_text = " ".join(chunk_words)
            
            chunks.append({
                "text": chunk_text,
                "start_index": i,
                "end_index": min(i + chunk_size, len(words)),
                "length": len(chunk_words)
            })
        
        return chunks
    
    def process_pdf(self, pdf_path: Path, target_language: str = "en") -> Dict[str, any]:
        """
        Complete PDF processing pipeline
        
        Args:
            pdf_path: Path to PDF file
            target_language: Target language for translation
            
        Returns:
            Dictionary with processed data
        """
        logger.info(f"Processing PDF: {pdf_path}")
        
        # Extract text using multiple methods and choose the best result
        extraction_methods = config.PDF_PROCESSING["extraction_methods"]
        best_text = ""
        best_method = ""
        
        for method in extraction_methods:
            try:
                text = self.extract_text_from_pdf(pdf_path, method)
                if len(text) > len(best_text):
                    best_text = text
                    best_method = method
            except Exception as e:
                logger.warning(f"Method {method} failed: {e}")
        
        if not best_text:
            raise ValueError(f"Could not extract text from {pdf_path}")
        
        # Detect language
        detected_language = self.detect_language(best_text)
        logger.info(f"Detected language: {detected_language}")
        
        # Translate if necessary
        if detected_language != target_language:
            logger.info(f"Translating from {detected_language} to {target_language}")
            translated_text = self.translate_text(best_text, target_language)
        else:
            translated_text = best_text
        
        # Preprocess text
        processed_text = self.preprocess_text(translated_text, target_language)
        
        # Extract structured data
        structured_data = self.extract_structured_data(processed_text)
        
        # Create chunks
        chunks = self.chunk_text(processed_text)
        
        return {
            "file_path": str(pdf_path),
            "original_text": best_text,
            "processed_text": processed_text,
            "translated_text": translated_text,
            "detected_language": detected_language,
            "target_language": target_language,
            "extraction_method": best_method,
            "structured_data": structured_data,
            "chunks": chunks,
            "metadata": {
                "file_size": pdf_path.stat().st_size,
                "text_length": len(processed_text),
                "num_chunks": len(chunks),
                "processing_timestamp": str(pd.Timestamp.now())
            }
        }
