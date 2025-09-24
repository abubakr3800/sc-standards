"""
Simple test to check basic functionality
"""
print("Starting simple test...")

try:
    import sys
    from pathlib import Path
    print("✅ Basic imports work")
    
    # Add src to path
    sys.path.insert(0, str(Path(__file__).parent / "src"))
    print("✅ Path added")
    
    # Test config
    from ai_standards.core.config import config
    print("✅ Config imported")
    print(f"Base PDFs dir: {config.BASE_PDFS_DIR}")
    print(f"Base PDFs exists: {config.BASE_PDFS_DIR.exists()}")
    
    # List PDFs
    pdf_files = list(config.BASE_PDFS_DIR.glob("*.pdf"))
    print(f"Found {len(pdf_files)} PDF files")
    for pdf in pdf_files:
        print(f"  - {pdf.name}")
    
    # Test PDF processor
    from ai_standards.core.pdf_processor import PDFProcessor
    print("✅ PDFProcessor imported")
    
    processor = PDFProcessor()
    print("✅ PDFProcessor created")
    
    if pdf_files:
        print(f"Testing with: {pdf_files[0].name}")
        result = processor.process_pdf(pdf_files[0])
        if result:
            print("✅ PDF processing successful")
            print(f"Result type: {type(result)}")
            if isinstance(result, dict):
                print(f"Result keys: {list(result.keys())}")
        else:
            print("❌ PDF processing returned None")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("Test completed.")
