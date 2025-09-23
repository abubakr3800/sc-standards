"""
Test script to verify AI Standards Training System installation
"""
import sys
from pathlib import Path

def test_imports():
    """Test if all required packages can be imported"""
    print("🔍 Testing package imports...")
    
    test_packages = [
        ("torch", "PyTorch"),
        ("transformers", "Transformers"),
        ("sentence_transformers", "Sentence Transformers"),
        ("sklearn", "Scikit-learn"),
        ("numpy", "NumPy"),
        ("pandas", "Pandas"),
        ("pdfplumber", "PDF Plumber"),
        ("fitz", "PyMuPDF"),
        ("spacy", "spaCy"),
        ("streamlit", "Streamlit"),
        ("fastapi", "FastAPI"),
        ("chromadb", "ChromaDB"),
        ("matplotlib", "Matplotlib"),
        ("plotly", "Plotly")
    ]
    
    failed_imports = []
    
    for module, name in test_packages:
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError as e:
            print(f"❌ {name}: {e}")
            failed_imports.append(name)
    
    return len(failed_imports) == 0, failed_imports

def test_directories():
    """Test if required directories exist"""
    print("\n📁 Testing directory structure...")
    
    required_dirs = [
        "data",
        "models",
        "uploads", 
        "outputs",
        "logs",
        "base"
    ]
    
    missing_dirs = []
    
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"✅ {dir_name}/")
        else:
            print(f"❌ {dir_name}/ (missing)")
            missing_dirs.append(dir_name)
    
    return len(missing_dirs) == 0, missing_dirs

def test_pdf_files():
    """Test if PDF files are available"""
    print("\n📄 Testing PDF files...")
    
    base_dir = Path("base")
    if not base_dir.exists():
        print("❌ base/ directory not found")
        return False, []
    
    pdf_files = list(base_dir.glob("*.pdf"))
    
    if pdf_files:
        print(f"✅ Found {len(pdf_files)} PDF files:")
        for pdf_file in pdf_files:
            print(f"   - {pdf_file.name}")
        return True, pdf_files
    else:
        print("⚠️  No PDF files found in base/ directory")
        print("   Place your PDF standards files in the base/ folder")
        return False, []

def test_config():
    """Test if configuration can be loaded"""
    print("\n⚙️  Testing configuration...")
    
    try:
        from config import config
        print("✅ Configuration loaded successfully")
        print(f"   - Base directory: {config.BASE_DIR}")
        print(f"   - PDFs directory: {config.BASE_PDFS_DIR}")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_basic_functionality():
    """Test basic system functionality"""
    print("\n🧪 Testing basic functionality...")
    
    try:
        # Test PDF processor
        from pdf_processor import PDFProcessor
        processor = PDFProcessor()
        print("✅ PDF Processor initialized")
        
        # Test AI trainer
        from ai_trainer import AIStandardsTrainer
        trainer = AIStandardsTrainer()
        print("✅ AI Trainer initialized")
        
        # Test comparison model
        from comparison_model import StandardsComparisonModel
        comparison_model = StandardsComparisonModel()
        print("✅ Comparison Model initialized")
        
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 AI Standards Training System - Installation Test")
    print("=" * 60)
    
    # Test imports
    imports_ok, failed_imports = test_imports()
    
    # Test directories
    dirs_ok, missing_dirs = test_directories()
    
    # Test PDF files
    pdfs_ok, pdf_files = test_pdf_files()
    
    # Test configuration
    config_ok = test_config()
    
    # Test basic functionality
    functionality_ok = test_basic_functionality()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary:")
    
    all_tests_passed = all([imports_ok, dirs_ok, config_ok, functionality_ok])
    
    if all_tests_passed:
        print("✅ All tests passed! System is ready to use.")
        
        if pdfs_ok:
            print(f"\n🎯 Ready to process {len(pdf_files)} PDF files")
            print("Next steps:")
            print("1. python main.py process")
            print("2. python main.py train")
            print("3. python main.py web")
        else:
            print("\n📄 Add PDF files to base/ folder to get started")
            
    else:
        print("❌ Some tests failed. Please check the issues above.")
        
        if failed_imports:
            print(f"\n📦 Missing packages: {', '.join(failed_imports)}")
            print("   Run: python install.py")
        
        if missing_dirs:
            print(f"\n📁 Missing directories: {', '.join(missing_dirs)}")
            print("   Run: python install.py")
    
    return all_tests_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
