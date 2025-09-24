"""
Enhanced Dialux PDF Extractor
Advanced extraction method for improved accuracy
"""
import os
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import logging

import pdfplumber
import fitz  # PyMuPDF
import pandas as pd
from loguru import logger

# Optional dependencies for enhanced extraction
try:
    import pytesseract
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    logger.warning("OCR dependencies not available. Install pytesseract and Pillow for OCR support.")

try:
    import camelot
    CAMELOT_AVAILABLE = True
except ImportError:
    CAMELOT_AVAILABLE = False
    logger.warning("Camelot not available. Install camelot-py for advanced table extraction.")

class EnhancedDialuxExtractor:
    """Enhanced Dialux PDF extractor with multiple extraction methods"""
    
    def __init__(self):
        self.project_keys = ['project', 'project title', 'title', 'projekt', 'project name']
        self.lum_table_keywords = ['luminaire', 'luminaire list', 'luminaire schedule', 'lamp', 'manufacturer', 'model']
        self.room_keys = ['room', 'area', 'space', 'raum', 'room name']
        self.calc_keys = ['illuminance', 'avg', 'uniformity', 'ugr', 'lux', 'w/m²', 'power density']
        
    def slug(self, text: str) -> str:
        """Convert text to slug format"""
        return re.sub(r'\s+', '_', text.strip().lower())
    
    def contains_any(self, text: str, keywords: List[str]) -> bool:
        """Check if text contains any of the keywords"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in keywords)
    
    def save_image_from_pix(self, pix, out_path: str) -> str:
        """Save PyMuPDF pixmap as image"""
        if not OCR_AVAILABLE:
            return ""
        
        try:
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img.save(out_path)
            return out_path
        except Exception as e:
            logger.error(f"Failed to save image: {e}")
            return ""
    
    def ocr_image(self, image_path: str) -> str:
        """Extract text from image using OCR"""
        if not OCR_AVAILABLE:
            return ""
        
        try:
            text = pytesseract.image_to_string(Image.open(image_path))
            return text.strip()
        except Exception as e:
            logger.error(f"OCR failed for {image_path}: {e}")
            return ""
    
    def extract_with_pdfplumber(self, pdf_path: Path) -> Dict[str, Any]:
        """Extract data using pdfplumber"""
        result = {
            "text_pages": [],
            "tables": [],
            "luminaires": [],
            "project_info": {}
        }
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    page_num = i + 1
                    text = page.extract_text() or ""
                    result["text_pages"].append({"page": page_num, "text": text})
                    
                    # Extract project information
                    if self.contains_any(text, self.project_keys) and not result["project_info"].get("title"):
                        match = re.search(r'project[:\s\-]*([^\n\r]+)', text, re.IGNORECASE)
                        if match:
                            result["project_info"]["title"] = match.group(1).strip()
                    
                    # Extract tables
                    try:
                        tables = page.extract_tables()
                        for table in tables:
                            if any(len(row) > 0 for row in table):
                                result["tables"].append({
                                    "page": page_num,
                                    "raw_table": table
                                })
                                
                                # Check if it's a luminaire table
                                header = " ".join(table[0]).lower() if table and table[0] else ""
                                if self.contains_any(header, self.lum_table_keywords):
                                    # Convert to structured data
                                    keys = [col.strip() for col in table[0]]
                                    for row in table[1:]:
                                        luminaire = {}
                                        for key, value in zip(keys, row):
                                            luminaire[key or 'col'] = value
                                        result["luminaires"].append(luminaire)
                    except Exception as e:
                        logger.warning(f"Table extraction failed on page {page_num}: {e}")
                        
        except Exception as e:
            logger.error(f"PDFPlumber extraction failed: {e}")
            
        return result
    
    def extract_with_pymupdf(self, pdf_path: Path, output_dir: str) -> Dict[str, Any]:
        """Extract data using PyMuPDF with image processing"""
        result = {
            "images": [],
            "ocr_text": [],
            "metadata": {}
        }
        
        try:
            doc = fitz.open(pdf_path)
            
            # Extract metadata
            metadata = doc.metadata
            result["metadata"] = {
                "title": metadata.get("title", ""),
                "author": metadata.get("author", ""),
                "subject": metadata.get("subject", ""),
                "creator": metadata.get("creator", ""),
                "producer": metadata.get("producer", ""),
                "creation_date": metadata.get("creationDate", ""),
                "modification_date": metadata.get("modDate", ""),
                "page_count": len(doc)
            }
            
            # Extract images and run OCR
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                images = page.get_images(full=True)
                
                for img_index, img in enumerate(images):
                    xref = img[0]
                    pix = fitz.Pixmap(doc, xref)
                    
                    img_name = f"page_{page_num+1}_img_{img_index+1}.png"
                    img_path = os.path.join(output_dir, img_name)
                    
                    try:
                        if pix.n < 5:  # GRAY or RGB
                            pix.save(img_path)
                        else:  # CMYK
                            pix0 = fitz.Pixmap(fitz.csRGB, pix)
                            pix0.save(img_path)
                            pix0 = None
                        
                        result["images"].append({
                            "page": page_num + 1,
                            "path": img_path
                        })
                        
                        # Run OCR on image
                        ocr_text = self.ocr_image(img_path)
                        if ocr_text:
                            result["ocr_text"].append({
                                "page": page_num + 1,
                                "text": ocr_text
                            })
                            
                            # Extract illuminance values from OCR
                            lux_matches = re.findall(r'([\d,.]{2,7})\s*(lx|lux)', ocr_text, re.IGNORECASE)
                            for match in lux_matches:
                                result.setdefault("ocr_lux_values", []).append({
                                    "page": page_num + 1,
                                    "value": match[0],
                                    "unit": match[1]
                                })
                                
                    except Exception as e:
                        logger.warning(f"Image processing failed for page {page_num+1}: {e}")
                    finally:
                        pix = None
                        
            doc.close()
            
        except Exception as e:
            logger.error(f"PyMuPDF extraction failed: {e}")
            
        return result
    
    def extract_with_camelot(self, pdf_path: Path) -> Dict[str, Any]:
        """Extract tables using Camelot (if available)"""
        result = {"camelot_tables": []}
        
        if not CAMELOT_AVAILABLE:
            logger.warning("Camelot not available, skipping advanced table extraction")
            return result
        
        try:
            tables = camelot.read_pdf(str(pdf_path), pages='all', flavor='stream')
            
            for table in tables:
                df = table.df
                result["camelot_tables"].append({
                    "page": int(table.page),
                    "raw_table": df.values.tolist(),
                    "accuracy": table.accuracy
                })
                
                # Check if it's a luminaire table
                header = " ".join(df.iloc[0].astype(str).tolist()).lower()
                if self.contains_any(header, self.lum_table_keywords):
                    keys = df.iloc[0].tolist()
                    luminaires = []
                    for i in range(1, len(df)):
                        row = df.iloc[i].tolist()
                        luminaire = {key: value for key, value in zip(keys, row)}
                        luminaires.append(luminaire)
                    
                    result.setdefault("camelot_luminaires", []).extend(luminaires)
                    
        except Exception as e:
            logger.warning(f"Camelot extraction failed: {e}")
            
        return result
    
    def extract_rooms_from_text(self, text: str) -> List[Dict[str, str]]:
        """Extract room information from text"""
        rooms = []
        
        # Pattern for room extraction
        room_patterns = [
            r'(Room|Space|Area)\s*[:\-]\s*([^\n\r]+)',
            r'([^\n\r]+)\s*\(([^\n\r]+)\)',  # Room name (description)
            r'Room\s+(\d+)[:\-]\s*([^\n\r]+)'
        ]
        
        for pattern in room_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                room_name = match.group(2) if len(match.groups()) > 1 else match.group(1)
                rooms.append({"name": room_name.strip()})
        
        return rooms
    
    def extract_report(self, pdf_path: Path, output_dir: str = "output") -> Dict[str, Any]:
        """Main extraction method combining all approaches"""
        os.makedirs(output_dir, exist_ok=True)
        base_name = Path(pdf_path).stem
        
        logger.info(f"Starting enhanced extraction for: {pdf_path}")
        
        # Initialize result structure
        result = {
            "project": {},
            "rooms": [],
            "luminaires": [],
            "tables_extracted": [],
            "images": [],
            "extraction_quality": {},
            "extraction_methods": []
        }
        
        # 1. PDFPlumber extraction
        logger.info("Extracting with PDFPlumber...")
        pdfplumber_result = self.extract_with_pdfplumber(pdf_path)
        result["extraction_methods"].append("pdfplumber")
        
        # Merge results
        result["project"].update(pdfplumber_result["project_info"])
        result["luminaires"].extend(pdfplumber_result["luminaires"])
        result["tables_extracted"].extend(pdfplumber_result["tables"])
        
        # 2. PyMuPDF extraction with OCR
        logger.info("Extracting with PyMuPDF and OCR...")
        pymupdf_result = self.extract_with_pymupdf(pdf_path, output_dir)
        result["extraction_methods"].append("pymupdf")
        
        # Merge results
        result["images"].extend(pymupdf_result["images"])
        result["extraction_quality"]["ocr_pages"] = len(pymupdf_result["ocr_text"])
        
        # 3. Camelot extraction (if available)
        if CAMELOT_AVAILABLE:
            logger.info("Extracting with Camelot...")
            camelot_result = self.extract_with_camelot(pdf_path)
            result["extraction_methods"].append("camelot")
            
            # Merge results
            result["tables_extracted"].extend(camelot_result["camelot_tables"])
            if "camelot_luminaires" in camelot_result:
                result["luminaires"].extend(camelot_result["camelot_luminaires"])
        
        # 4. Extract rooms from all text sources
        all_text = ""
        for page in pdfplumber_result["text_pages"]:
            all_text += page["text"] + "\n"
        for ocr in pymupdf_result["ocr_text"]:
            all_text += ocr["text"] + "\n"
        
        result["rooms"] = self.extract_rooms_from_text(all_text)
        
        # 5. Calculate extraction quality metrics
        result["extraction_quality"] = {
            "text_confidence_estimate": 0.90,  # Higher confidence with multiple methods
            "tables_found": len(result["tables_extracted"]),
            "ocr_images_with_text": len(pymupdf_result["ocr_text"]),
            "luminaires_found": len(result["luminaires"]),
            "rooms_found": len(result["rooms"]),
            "extraction_methods_used": result["extraction_methods"]
        }
        
        # 6. Normalize luminaires data
        normalized_luminaires = []
        for luminaire in result["luminaires"]:
            normalized = {key.strip().lower(): (value or "").strip() 
                         for key, value in luminaire.items()}
            normalized_luminaires.append(normalized)
        result["luminaires"] = normalized_luminaires
        
        # 7. Save results
        output_json = os.path.join(output_dir, f"{base_name}_enhanced.json")
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        # Save CSV files
        if result["luminaires"]:
            df_luminaires = pd.DataFrame(result["luminaires"])
            df_luminaires.to_csv(
                os.path.join(output_dir, f"{base_name}_luminaires.csv"), 
                index=False
            )
        
        # Save tables as CSV
        for idx, table in enumerate(result["tables_extracted"]):
            df_table = pd.DataFrame(table["raw_table"])
            df_table.to_csv(
                os.path.join(output_dir, f"{base_name}_table_{idx+1}_p{table['page']}.csv"),
                index=False
            )
        
        logger.info(f"Enhanced extraction completed. Results saved to: {output_json}")
        return result

def main():
    """Main function for command-line usage"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python enhanced_dialux_extractor.py <pdf_file> [output_dir]")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "output"
    
    extractor = EnhancedDialuxExtractor()
    result = extractor.extract_report(Path(pdf_file), output_dir)
    
    print(f"Extraction completed!")
    print(f"Project: {result['project'].get('title', 'Unknown')}")
    print(f"Rooms found: {len(result['rooms'])}")
    print(f"Luminaires found: {len(result['luminaires'])}")
    print(f"Tables found: {len(result['tables_extracted'])}")
    print(f"Methods used: {', '.join(result['extraction_methods'])}")

if __name__ == "__main__":
    main()
