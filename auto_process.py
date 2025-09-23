"""
Automated PDF Processing for Standards
Simple, reliable processing that works every time
"""
import sys
import json
from pathlib import Path
from datetime import datetime

def extract_text_simple(pdf_path):
    """Simple text extraction using pdfplumber"""
    try:
        import pdfplumber
        text_parts = []
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(f"--- Page {page_num} ---\n{page_text}")
                except:
                    continue
        return "\n\n".join(text_parts)
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""

def extract_tables_simple(pdf_path):
    """Simple table extraction"""
    try:
        import pdfplumber
        tables = []
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                try:
                    page_tables = page.extract_tables()
                    for table_num, table in enumerate(page_tables, 1):
                        if table and len(table) > 1:
                            tables.append({
                                "page": page_num,
                                "table_number": table_num,
                                "data": table,
                                "title": f"Table {table_num} from Page {page_num}"
                            })
                except:
                    continue
        return tables
    except Exception as e:
        print(f"Error extracting tables: {e}")
        return []

def detect_language_simple(text):
    """Simple language detection"""
    try:
        from langdetect import detect
        sample = text[:1000].strip()
        if sample:
            return detect(sample)
    except:
        pass
    return "en"

def extract_metadata_simple(text, file_path):
    """Extract basic metadata"""
    text_lower = text.lower()
    
    metadata = {
        "file_name": file_path.name,
        "file_path": str(file_path),
        "language": detect_language_simple(text),
        "categories": [],
        "keywords": [],
        "standard_type": "Unknown",
        "standard_number": "Unknown"
    }
    
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
    
    # Extract keywords
    keywords = ["illuminance", "lux", "color rendering", "cri", "ugr", "glare", 
                "lighting", "led", "daylight", "energy efficiency"]
    for keyword in keywords:
        if keyword in text_lower:
            metadata["keywords"].append(keyword)
    
    # Add categories
    if "illuminance" in text_lower or "lux" in text_lower:
        metadata["categories"].append("illuminance")
    if "color" in text_lower or "cri" in text_lower:
        metadata["categories"].append("color_rendering")
    if "glare" in text_lower or "ugr" in text_lower:
        metadata["categories"].append("glare_control")
    if "energy" in text_lower:
        metadata["categories"].append("energy_efficiency")
    
    return metadata

def process_pdf_simple(pdf_path):
    """Process a single PDF file"""
    print(f"📄 Processing: {pdf_path.name}")
    
    try:
        # Extract text
        text_content = extract_text_simple(pdf_path)
        if not text_content.strip():
            print(f"❌ No text extracted from {pdf_path.name}")
            return None
        
        # Extract tables
        tables = extract_tables_simple(pdf_path)
        
        # Extract metadata
        metadata = extract_metadata_simple(text_content, pdf_path)
        
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
                "processing_method": "auto_process_simple",
                "confidence_score": 0.9
            }
        }
        
        print(f"✅ Successfully processed {pdf_path.name}")
        print(f"   📊 Text length: {len(text_content)} characters")
        print(f"   📋 Tables: {len(tables)}")
        print(f"   🏷️  Categories: {', '.join(metadata['categories'])}")
        
        return processed_doc
        
    except Exception as e:
        print(f"❌ Error processing {pdf_path.name}: {e}")
        return None

def main():
    """Main processing function"""
    print("🚀 Automated Standards Processing")
    print("=" * 40)
    
    # Set up paths
    base_dir = Path("base")
    uploads_dir = Path("uploads")
    
    print(f"📁 Base directory: {base_dir}")
    print(f"📁 Uploads directory: {uploads_dir}")
    
    # Check base directory
    if not base_dir.exists():
        print(f"❌ Base directory does not exist: {base_dir}")
        return
    
    # Create uploads directory
    uploads_dir.mkdir(exist_ok=True)
    
    # Find PDF files
    pdf_files = list(base_dir.glob("*.pdf"))
    print(f"📄 Found {len(pdf_files)} PDF files")
    
    if not pdf_files:
        print("❌ No PDF files found in base/ directory")
        return
    
    # Process each PDF
    processed_count = 0
    for pdf_file in pdf_files:
        result = process_pdf_simple(pdf_file)
        if result:
            # Save processed document
            output_filename = f"{pdf_file.stem}_processed.json"
            output_path = uploads_dir / output_filename
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"💾 Saved: {output_filename}")
            processed_count += 1
        print()
    
    # Summary
    print("=" * 40)
    print(f"✅ Successfully processed: {processed_count}/{len(pdf_files)} files")
    
    if processed_count > 0:
        print(f"📁 Processed files saved to: {uploads_dir}")
        print(f"💡 You can now run: py main.py train")
    else:
        print("❌ No files were processed successfully")

if __name__ == "__main__":
    main()
