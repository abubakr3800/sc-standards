"""
Demo: How to Use the AI Standards System
Shows practical examples of using the trained system
"""
import sys
import json
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

def demo_web_interface():
    """Show how to start the web interface"""
    print("🌐 Web Interface Demo")
    print("=" * 30)
    print("To start the web interface:")
    print("1. Run: make web")
    print("2. Open browser to: http://localhost:8501")
    print("3. Features available:")
    print("   📄 Upload new PDF standards")
    print("   🔍 Search existing standards")
    print("   📊 Compare two standards")
    print("   📈 View similarity scores")
    print("   📋 Export results")
    print()

def demo_api_usage():
    """Show how to use the API"""
    print("🔌 API Usage Demo")
    print("=" * 30)
    print("To start the API:")
    print("1. Run: make run-api")
    print("2. API available at: http://localhost:8000")
    print("3. Example API calls:")
    print()
    print("   # Compare standards")
    print("   curl -X POST http://localhost:8000/compare \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"doc1\": \"prEN 12464-1\", \"doc2\": \"BREEAM\"}'")
    print()
    print("   # Search standards")
    print("   curl http://localhost:8000/search?query=illuminance")
    print()

def demo_cli_usage():
    """Show command line usage"""
    print("💻 Command Line Demo")
    print("=" * 30)
    print("Available commands:")
    print()
    print("  # Process new PDFs")
    print("  make auto-process")
    print()
    print("  # Train models")
    print("  make train")
    print()
    print("  # Compare standards")
    print("  make compare --standard-a 'prEN 12464-1' --standard-b 'BREEAM'")
    print()
    print("  # Start web interface")
    print("  make web")
    print()
    print("  # Start API")
    print("  make run-api")
    print()

def demo_programmatic_usage():
    """Show programmatic usage examples"""
    print("🐍 Programmatic Usage Demo")
    print("=" * 30)
    
    try:
        # Check if we can import the modules
        from ai_standards.models.comparison_model import StandardsComparisonModel
        from ai_standards.core.config import config
        
        print("✅ Modules imported successfully")
        print()
        print("Example code:")
        print()
        print("```python")
        print("from ai_standards.models.comparison_model import StandardsComparisonModel")
        print()
        print("# Initialize model")
        print("model = StandardsComparisonModel()")
        print()
        print("# Load documents")
        print("with open('uploads/prEN 12464-1_processed.json', 'r') as f:")
        print("    doc1 = json.load(f)")
        print()
        print("with open('uploads/BREEAM_processed.json', 'r') as f:")
        print("    doc2 = json.load(f)")
        print()
        print("# Compare standards")
        print("result = model.compare_standards(doc1, doc2)")
        print("print(f'Similarity: {result.overall_similarity:.2%}')")
        print("```")
        print()
        
        # Try to demonstrate actual usage
        print("🧪 Testing actual functionality...")
        
        # Check if processed documents exist
        processed_files = list(config.UPLOADS_DIR.glob("*_processed.json"))
        if len(processed_files) >= 2:
            print(f"✅ Found {len(processed_files)} processed documents")
            
            # Try to load and compare
            with open(processed_files[0], 'r', encoding='utf-8') as f:
                doc1 = json.load(f)
            
            with open(processed_files[1], 'r', encoding='utf-8') as f:
                doc2 = json.load(f)
            
            print(f"📄 Document 1: {doc1.get('file_name', 'Unknown')}")
            print(f"📄 Document 2: {doc2.get('file_name', 'Unknown')}")
            
            # Try to initialize model and compare
            try:
                model = StandardsComparisonModel()
                result = model.compare_standards(doc1, doc2)
                
                print(f"🎯 Comparison successful!")
                print(f"   Similarity: {result.overall_similarity:.2%}")
                print(f"   Matching categories: {len(result.matching_categories)}")
                print(f"   Differences: {len(result.differences)}")
                
            except Exception as e:
                print(f"⚠️  Model comparison failed: {e}")
                print("   This might mean models need to be trained first")
                print("   Run: make train")
        else:
            print("❌ Not enough processed documents found")
            print("   Run: make auto-process")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure all dependencies are installed")
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_accuracy_testing():
    """Show how to test accuracy"""
    print("\n🧪 Accuracy Testing Demo")
    print("=" * 30)
    print("To test system accuracy:")
    print()
    print("1. Run basic accuracy test:")
    print("   python accuracy_test.py")
    print()
    print("2. Run comprehensive test:")
    print("   python test_system.py")
    print()
    print("3. Manual testing:")
    print("   - Compare known similar standards")
    print("   - Search for specific terms")
    print("   - Check category detection")
    print()

def main():
    """Main demo function"""
    print("🚀 AI Standards System - Usage Demo")
    print("=" * 50)
    
    demo_web_interface()
    demo_api_usage()
    demo_cli_usage()
    demo_programmatic_usage()
    demo_accuracy_testing()
    
    print("\n" + "=" * 50)
    print("🎯 QUICK START GUIDE")
    print("=" * 50)
    print("1. Start web interface: make web")
    print("2. Open browser to: http://localhost:8501")
    print("3. Upload PDFs or compare existing standards")
    print("4. Test accuracy: python accuracy_test.py")
    print()
    print("📚 For detailed usage, see: USAGE_GUIDE.md")

if __name__ == "__main__":
    main()
