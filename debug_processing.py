"""
Debug script to test PDF processing functionality
"""
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from ai_standards.core.config import config
        print("✅ Config imported")
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from ai_standards.core.pdf_processor import PDFProcessor
        print("✅ PDFProcessor imported")
    except Exception as e:
        print(f"❌ PDFProcessor import failed: {e}")
        return False
    
    return True

def test_config():
    """Test configuration"""
    print("\n🔍 Testing configuration...")
    
    try:
        from ai_standards.core.config import config
        
        print(f"Base PDFs directory: {config.BASE_PDFS_DIR}")
        print(f"Uploads directory: {config.UPLOADS_DIR}")
        print(f"Base PDFs exists: {config.BASE_PDFS_DIR.exists()}")
        print(f"Uploads exists: {config.UPLOADS_DIR.exists()}")
        
        # List PDF files
        pdf_files = list(config.BASE_PDFS_DIR.glob("*.pdf"))
        print(f"PDF files found: {len(pdf_files)}")
        for pdf_file in pdf_files:
            print(f"  - {pdf_file.name}")
        
        return len(pdf_files) > 0
        
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False

def test_pdf_processor():
    """Test PDF processor creation"""
    print("\n🔍 Testing PDF processor...")
    
    try:
        from ai_standards.core.pdf_processor import PDFProcessor
        
        processor = PDFProcessor()
        print("✅ PDFProcessor created successfully")
        return True
        
    except Exception as e:
        print(f"❌ PDFProcessor creation failed: {e}")
        return False

def test_single_pdf():
    """Test processing a single PDF"""
    print("\n🔍 Testing single PDF processing...")
    
    try:
        from ai_standards.core.config import config
        from ai_standards.core.pdf_processor import PDFProcessor
        
        pdf_files = list(config.BASE_PDFS_DIR.glob("*.pdf"))
        if not pdf_files:
            print("❌ No PDF files found")
            return False
        
        # Test with first PDF
        test_pdf = pdf_files[0]
        print(f"Testing with: {test_pdf.name}")
        
        processor = PDFProcessor()
        
        # Try to process the PDF
        print("Processing PDF...")
        result = processor.process_pdf(test_pdf)
        
        if result:
            print("✅ PDF processing successful")
            print(f"Result keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
            return True
        else:
            print("❌ PDF processing returned None")
            return False
            
    except Exception as e:
        print(f"❌ PDF processing failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main debug function"""
    print("🚀 AI Standards - PDF Processing Debug")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed")
        return
    
    # Test config
    if not test_config():
        print("\n❌ Config tests failed")
        return
    
    # Test processor
    if not test_pdf_processor():
        print("\n❌ Processor tests failed")
        return
    
    # Test single PDF
    if not test_single_pdf():
        print("\n❌ PDF processing tests failed")
        return
    
    print("\n✅ All tests passed! PDF processing should work.")

if __name__ == "__main__":
    main()
