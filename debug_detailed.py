"""
Detailed debug script with error handling
"""
import sys
import traceback
from pathlib import Path

print("Starting detailed debug...")

try:
    # Add src to path
    sys.path.insert(0, str(Path(__file__).parent / "src"))
    print("✅ Path added")
    
    # Test config import
    print("Testing config import...")
    from ai_standards.core.config import config
    print("✅ Config imported")
    
    # Test PDF processor import
    print("Testing PDF processor import...")
    from ai_standards.core.pdf_processor import PDFProcessor
    print("✅ PDFProcessor imported")
    
    # Test processor creation
    print("Testing processor creation...")
    processor = PDFProcessor()
    print("✅ Processor created")
    
    # Test PDF files
    print("Testing PDF files...")
    pdf_files = list(config.BASE_PDFS_DIR.glob("*.pdf"))
    print(f"Found {len(pdf_files)} PDF files")
    
    if pdf_files:
        test_pdf = pdf_files[0]
        print(f"Testing with: {test_pdf.name}")
        
        # Test PDF processing
        print("Testing PDF processing...")
        result = processor.process_pdf(test_pdf)
        print(f"Processing result: {result is not None}")
        
        if result:
            print(f"Result type: {type(result)}")
            if isinstance(result, dict):
                print(f"Result keys: {list(result.keys())}")
        else:
            print("❌ Processing returned None")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("Full traceback:")
    traceback.print_exc()

print("Debug completed.")
