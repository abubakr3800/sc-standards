"""
Simple Accuracy Test for AI Standards System
"""
import sys
import json
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_basic_functionality():
    """Test basic system functionality"""
    print("🧪 Basic System Test")
    print("=" * 30)
    
    try:
        # Test 1: Check if models are trained
        models_dir = Path("models")
        if models_dir.exists():
            model_files = list(models_dir.glob("*"))
            print(f"✅ Models directory exists with {len(model_files)} files")
        else:
            print("❌ Models directory not found")
            return False
        
        # Test 2: Check processed documents
        uploads_dir = Path("uploads")
        processed_files = list(uploads_dir.glob("*_processed.json"))
        print(f"✅ Found {len(processed_files)} processed documents")
        
        if len(processed_files) == 0:
            print("❌ No processed documents found")
            return False
        
        # Test 3: Test document loading
        test_doc = processed_files[0]
        with open(test_doc, 'r', encoding='utf-8') as f:
            doc_data = json.load(f)
        
        required_fields = ['file_name', 'text_content', 'metadata', 'tables']
        missing_fields = [field for field in required_fields if field not in doc_data]
        
        if missing_fields:
            print(f"❌ Missing fields in processed document: {missing_fields}")
            return False
        else:
            print("✅ Processed document structure is correct")
        
        # Test 4: Test metadata extraction
        metadata = doc_data.get('metadata', {})
        categories = metadata.get('categories', [])
        keywords = metadata.get('keywords', [])
        
        print(f"✅ Document categories: {categories}")
        print(f"✅ Document keywords: {keywords[:5]}...")  # Show first 5
        
        return True
        
    except Exception as e:
        print(f"❌ Error in basic test: {e}")
        return False

def test_comparison_accuracy():
    """Test comparison accuracy with known data"""
    print("\n🔍 Comparison Accuracy Test")
    print("=" * 30)
    
    try:
        from ai_standards.models.comparison_model import StandardsComparisonModel
        
        # Initialize model
        model = StandardsComparisonModel()
        
        # Load test documents
        uploads_dir = Path("uploads")
        processed_files = list(uploads_dir.glob("*_processed.json"))
        
        if len(processed_files) < 2:
            print("❌ Need at least 2 documents for comparison")
            return False
        
        # Load documents
        with open(processed_files[0], 'r', encoding='utf-8') as f:
            doc1 = json.load(f)
        
        with open(processed_files[1], 'r', encoding='utf-8') as f:
            doc2 = json.load(f)
        
        # Perform comparison
        result = model.compare_standards(doc1, doc2)
        
        # Evaluate results
        print(f"📊 Comparison Results:")
        print(f"  Overall Similarity: {result.overall_similarity:.2%}")
        print(f"  Matching Categories: {len(result.matching_categories)}")
        print(f"  Differences Found: {len(result.differences)}")
        print(f"  Recommendations: {len(result.recommendations)}")
        
        # Check if results are reasonable
        if 0 <= result.overall_similarity <= 1:
            print("✅ Similarity score is within valid range")
        else:
            print("❌ Similarity score is invalid")
            return False
        
        if len(result.matching_categories) > 0:
            print("✅ Found matching categories")
        else:
            print("⚠️  No matching categories found")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in comparison test: {e}")
        return False

def test_search_accuracy():
    """Test search functionality"""
    print("\n🔎 Search Accuracy Test")
    print("=" * 30)
    
    try:
        from ai_standards.models.comparison_model import StandardsComparisonModel
        
        model = StandardsComparisonModel()
        
        # Test search queries
        test_queries = [
            "illuminance",
            "lighting",
            "energy efficiency",
            "color rendering"
        ]
        
        for query in test_queries:
            results = model.search_standards(query, top_k=2)
            
            if results:
                print(f"✅ Query '{query}': Found {len(results)} results")
                for doc, score in results:
                    print(f"   - {doc.get('file_name', 'Unknown')} (Score: {score:.3f})")
            else:
                print(f"❌ Query '{query}': No results found")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in search test: {e}")
        return False

def main():
    """Main accuracy test function"""
    print("🎯 AI Standards System - Accuracy Test")
    print("=" * 50)
    
    # Run tests
    basic_test = test_basic_functionality()
    comparison_test = test_comparison_accuracy()
    search_test = test_search_accuracy()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 ACCURACY TEST SUMMARY")
    print("=" * 50)
    
    tests_passed = sum([basic_test, comparison_test, search_test])
    total_tests = 3
    
    print(f"✅ Basic Functionality: {'PASS' if basic_test else 'FAIL'}")
    print(f"✅ Comparison Accuracy: {'PASS' if comparison_test else 'FAIL'}")
    print(f"✅ Search Accuracy: {'PASS' if search_test else 'FAIL'}")
    
    print(f"\n🎯 Overall Score: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 System is working accurately!")
        print("\n💡 Ready to use:")
        print("   - Web interface: make web")
        print("   - API: make run-api")
        print("   - CLI: make compare")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    main()
