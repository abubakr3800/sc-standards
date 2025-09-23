"""
Test and Evaluate the AI Standards System
Demonstrates how to use the trained system and test its accuracy
"""
import sys
import json
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_system_accuracy():
    """Test the accuracy of the trained system"""
    print("🧪 Testing AI Standards System Accuracy")
    print("=" * 50)
    
    try:
        from ai_standards.models.comparison_model import StandardsComparisonModel
        from ai_standards.core.config import config
        
        # Initialize the comparison model
        print("🔧 Initializing comparison model...")
        comparison_model = StandardsComparisonModel()
        print("✅ Comparison model loaded")
        
        # Load processed documents for testing
        processed_files = list(config.UPLOADS_DIR.glob("*_processed.json"))
        print(f"📄 Found {len(processed_files)} processed documents")
        
        if len(processed_files) < 2:
            print("❌ Need at least 2 processed documents for comparison testing")
            return
        
        # Test 1: Compare two standards
        print("\n🔍 Test 1: Standards Comparison")
        print("-" * 30)
        
        doc1_path = processed_files[0]
        doc2_path = processed_files[1]
        
        print(f"Comparing:")
        print(f"  📄 Document 1: {doc1_path.stem}")
        print(f"  📄 Document 2: {doc2_path.stem}")
        
        # Load documents
        with open(doc1_path, 'r', encoding='utf-8') as f:
            doc1 = json.load(f)
        
        with open(doc2_path, 'r', encoding='utf-8') as f:
            doc2 = json.load(f)
        
        # Perform comparison
        comparison_result = comparison_model.compare_standards(doc1, doc2)
        
        print(f"\n📊 Comparison Results:")
        print(f"  🎯 Overall Similarity: {comparison_result.overall_similarity:.2%}")
        print(f"  📋 Category Matches: {len(comparison_result.matching_categories)}")
        print(f"  ⚠️  Differences: {len(comparison_result.differences)}")
        print(f"  💡 Recommendations: {len(comparison_result.recommendations)}")
        
        # Show detailed results
        print(f"\n📋 Matching Categories:")
        for category in comparison_result.matching_categories:
            print(f"  ✅ {category}")
        
        print(f"\n⚠️  Key Differences:")
        for diff in comparison_result.differences[:3]:  # Show first 3
            print(f"  • {diff}")
        
        print(f"\n💡 Recommendations:")
        for rec in comparison_result.recommendations[:3]:  # Show first 3
            print(f"  • {rec}")
        
        return comparison_result
        
    except Exception as e:
        print(f"❌ Error testing system: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_semantic_search():
    """Test semantic search functionality"""
    print("\n🔍 Test 2: Semantic Search")
    print("-" * 30)
    
    try:
        from ai_standards.models.comparison_model import StandardsComparisonModel
        
        comparison_model = StandardsComparisonModel()
        
        # Test queries
        test_queries = [
            "illuminance requirements for office work",
            "color rendering index standards",
            "energy efficiency lighting",
            "glare control measures"
        ]
        
        for query in test_queries:
            print(f"\n🔎 Query: '{query}'")
            results = comparison_model.search_standards(query, top_k=3)
            
            if results:
                print(f"  📄 Found {len(results)} relevant documents:")
                for i, (doc, score) in enumerate(results, 1):
                    print(f"    {i}. {doc.get('file_name', 'Unknown')} (Score: {score:.3f})")
            else:
                print("  ❌ No relevant documents found")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing semantic search: {e}")
        return False

def test_category_classification():
    """Test category classification accuracy"""
    print("\n🏷️  Test 3: Category Classification")
    print("-" * 30)
    
    try:
        from ai_standards.models.comparison_model import StandardsComparisonModel
        
        comparison_model = StandardsComparisonModel()
        
        # Test category detection
        test_texts = [
            ("General office work requires 500 lux illuminance", ["illuminance"]),
            ("Color rendering index should be at least 80", ["color_rendering"]),
            ("UGR limit for computer work is 16", ["glare_control"]),
            ("LED lighting reduces energy consumption", ["energy_efficiency"]),
            ("Daylight integration improves sustainability", ["daylight", "energy_efficiency"])
        ]
        
        correct_predictions = 0
        total_predictions = len(test_texts)
        
        for text, expected_categories in test_texts:
            predicted_categories = comparison_model.classify_categories(text)
            
            # Check if any expected category is predicted
            matches = any(cat in predicted_categories for cat in expected_categories)
            if matches:
                correct_predictions += 1
                status = "✅"
            else:
                status = "❌"
            
            print(f"  {status} Text: '{text[:50]}...'")
            print(f"    Expected: {expected_categories}")
            print(f"    Predicted: {predicted_categories}")
        
        accuracy = correct_predictions / total_predictions
        print(f"\n📊 Classification Accuracy: {accuracy:.2%} ({correct_predictions}/{total_predictions})")
        
        return accuracy
        
    except Exception as e:
        print(f"❌ Error testing classification: {e}")
        return 0.0

def demonstrate_usage():
    """Demonstrate how to use the system"""
    print("\n🚀 System Usage Demonstration")
    print("=" * 50)
    
    print("📋 How to Use the AI Standards System:")
    print()
    
    print("1️⃣  Web Interface (Recommended):")
    print("   Command: make web")
    print("   URL: http://localhost:8501")
    print("   Features: Upload PDFs, compare standards, view results")
    print()
    
    print("2️⃣  API Interface:")
    print("   Command: make run-api")
    print("   URL: http://localhost:8000")
    print("   Features: REST API for integration with other systems")
    print()
    
    print("3️⃣  Command Line Interface:")
    print("   Compare standards: make compare --standard-a 'doc1' --standard-b 'doc2'")
    print("   Process new PDFs: make auto-process")
    print("   Train models: make train")
    print()
    
    print("4️⃣  Programmatic Usage:")
    print("   ```python")
    print("   from ai_standards.models.comparison_model import StandardsComparisonModel")
    print("   model = StandardsComparisonModel()")
    print("   result = model.compare_standards(doc1, doc2)")
    print("   ```")

def main():
    """Main testing function"""
    print("🧪 AI Standards System - Testing & Evaluation")
    print("=" * 60)
    
    # Test system accuracy
    comparison_result = test_system_accuracy()
    
    # Test semantic search
    search_success = test_semantic_search()
    
    # Test classification
    classification_accuracy = test_category_classification()
    
    # Demonstrate usage
    demonstrate_usage()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TESTING SUMMARY")
    print("=" * 60)
    
    if comparison_result:
        print(f"✅ Standards Comparison: Working")
        print(f"   Overall Similarity: {comparison_result.overall_similarity:.2%}")
    else:
        print("❌ Standards Comparison: Failed")
    
    if search_success:
        print("✅ Semantic Search: Working")
    else:
        print("❌ Semantic Search: Failed")
    
    print(f"✅ Category Classification: {classification_accuracy:.2%} accuracy")
    
    print(f"\n🎯 System Status: {'Ready for Use' if comparison_result and search_success else 'Needs Attention'}")
    
    print(f"\n💡 Next Steps:")
    print(f"   1. Start web interface: make web")
    print(f"   2. Upload new PDFs to base/ folder")
    print(f"   3. Process new PDFs: make auto-process")
    print(f"   4. Retrain models: make train")

if __name__ == "__main__":
    main()
