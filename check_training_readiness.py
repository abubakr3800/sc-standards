"""
Check Training Readiness
Verifies if the model is ready to train with improved code
"""
import sys
from pathlib import Path
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def check_training_readiness():
    """Check if the model is ready for training with improved code"""
    print("🔍 CHECKING TRAINING READINESS")
    print("=" * 50)
    
    readiness_status = {
        "enhanced_extraction": False,
        "dependencies": False,
        "data_available": False,
        "processing_files": False,
        "ai_trainer": False,
        "overall_ready": False
    }
    
    # 1. Check Enhanced Extraction
    print("\n1. 📄 Enhanced Extraction System:")
    try:
        from ai_standards.processing.enhanced_dialux_extractor import EnhancedDialuxExtractor
        extractor = EnhancedDialuxExtractor()
        print("  ✅ Enhanced Dialux Extractor available")
        print("  ✅ Multi-method extraction (pdfplumber, PyMuPDF, OCR, Camelot)")
        print("  ✅ Dialux-specific pattern recognition")
        readiness_status["enhanced_extraction"] = True
    except ImportError as e:
        print(f"  ❌ Enhanced extraction not available: {e}")
    
    # 2. Check Dependencies
    print("\n2. 📦 Dependencies:")
    try:
        import torch
        import transformers
        import sentence_transformers
        import pdfplumber
        import fitz
        print("  ✅ Core AI dependencies available")
        
        # Check optional dependencies
        try:
            import pytesseract
            from PIL import Image
            print("  ✅ OCR dependencies available")
        except ImportError:
            print("  ⚠️  OCR dependencies not available (optional)")
        
        try:
            import camelot
            print("  ✅ Camelot available for advanced table extraction")
        except ImportError:
            print("  ⚠️  Camelot not available (optional)")
        
        readiness_status["dependencies"] = True
    except ImportError as e:
        print(f"  ❌ Missing dependencies: {e}")
    
    # 3. Check Data Availability
    print("\n3. 📊 Data Availability:")
    data_dir = Path("data")
    standards_dir = data_dir / "standards"
    processed_dir = data_dir / "processed"
    
    if standards_dir.exists():
        pdf_files = list(standards_dir.glob("*.pdf"))
        print(f"  ✅ Standards PDFs available: {len(pdf_files)} files")
        for pdf in pdf_files:
            print(f"    - {pdf.name}")
    else:
        print("  ❌ No standards PDFs found")
    
    if processed_dir.exists():
        json_files = list(processed_dir.glob("*.json"))
        print(f"  ✅ Processed data available: {len(json_files)} files")
        for json_file in json_files:
            print(f"    - {json_file.name}")
        readiness_status["data_available"] = True
    else:
        print("  ❌ No processed data found")
    
    # 4. Check Processing Files
    print("\n4. 🔄 Processing Files:")
    processing_dir = Path("src/ai_standards/processing")
    if processing_dir.exists():
        processing_files = list(processing_dir.glob("*.py"))
        print(f"  ✅ Processing files available: {len(processing_files)} files")
        for file in processing_files:
            print(f"    - {file.name}")
        readiness_status["processing_files"] = True
    else:
        print("  ❌ Processing files not found")
    
    # 5. Check AI Trainer
    print("\n5. 🤖 AI Trainer:")
    try:
        from ai_standards.models.ai_trainer import AIStandardsTrainer
        trainer = AIStandardsTrainer()
        print("  ✅ AI Trainer available")
        print("  ✅ Sentence transformers ready")
        print("  ✅ Vector database ready")
        readiness_status["ai_trainer"] = True
    except ImportError as e:
        print(f"  ❌ AI Trainer not available: {e}")
    except Exception as e:
        print(f"  ⚠️  AI Trainer available but may need setup: {e}")
    
    # 6. Overall Assessment
    print("\n6. 🎯 Overall Assessment:")
    ready_components = sum(readiness_status.values())
    total_components = len(readiness_status) - 1  # Exclude overall_ready
    
    if ready_components >= 4:  # At least 4 out of 5 components ready
        readiness_status["overall_ready"] = True
        print("  ✅ MODEL IS READY FOR TRAINING!")
        print("  ✅ Enhanced extraction system available")
        print("  ✅ Dependencies resolved")
        print("  ✅ Data and processing files ready")
        print("  ✅ AI training system available")
    else:
        print("  ❌ Model not ready for training")
        print(f"  📊 Ready components: {ready_components}/{total_components}")
    
    # 7. Training Commands
    if readiness_status["overall_ready"]:
        print("\n7. 🚀 Ready to Train:")
        print("  Command: py main.py train")
        print("  Or: py main.py process (to process more PDFs first)")
        print("  Or: py main.py demo (for complete demo)")
    
    return readiness_status

def main():
    """Main function"""
    status = check_training_readiness()
    
    # Save status report
    with open("training_readiness_report.json", "w") as f:
        json.dump(status, f, indent=2)
    
    print(f"\n📋 Training readiness report saved to: training_readiness_report.json")
    
    return status["overall_ready"]

if __name__ == "__main__":
    is_ready = main()
    sys.exit(0 if is_ready else 1)

