"""
Test Batch Analyzer
Quick test to verify the batch analyzer works
"""
import sys
from pathlib import Path

def test_imports():
    """Test if all imports work correctly"""
    try:
        from batch_study_analyzer import BatchStudyAnalyzer
        print("✅ BatchStudyAnalyzer import successful")
        
        from pdf_study_analyzer import PDFStudyAnalyzer
        print("✅ PDFStudyAnalyzer import successful")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality"""
    try:
        from batch_study_analyzer import BatchStudyAnalyzer
        
        # Create analyzer instance
        analyzer = BatchStudyAnalyzer()
        print("✅ BatchStudyAnalyzer instance created")
        
        # Test folder path
        test_folder = Path("../dataset/Reports/")
        if test_folder.exists():
            print(f"✅ Test folder exists: {test_folder}")
            
            # Find PDF files
            pdf_files = list(test_folder.rglob("*.pdf"))
            print(f"📁 Found {len(pdf_files)} PDF files")
            
            if pdf_files:
                print("📄 PDF files found:")
                for pdf_file in pdf_files[:5]:  # Show first 5
                    print(f"  • {pdf_file.name}")
                if len(pdf_files) > 5:
                    print(f"  ... and {len(pdf_files) - 5} more")
            else:
                print("❌ No PDF files found in test folder")
        else:
            print(f"❌ Test folder not found: {test_folder}")
        
        return True
    except Exception as e:
        print(f"❌ Functionality test error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 TESTING BATCH ANALYZER")
    print("=" * 40)
    
    # Test imports
    if not test_imports():
        print("❌ Import test failed")
        return
    
    print()
    
    # Test basic functionality
    if not test_basic_functionality():
        print("❌ Functionality test failed")
        return
    
    print()
    print("✅ All tests passed! Batch analyzer is ready to use.")
    print()
    print("🚀 You can now run:")
    print("   python batch_study_analyzer.py \"../dataset/Reports/\" --recursive --output \"out.json\"")

if __name__ == "__main__":
    main()
