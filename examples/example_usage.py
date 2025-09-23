"""
Example usage of the AI Standards Training System
"""
import sys
from pathlib import Path
import json

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ai_standards.core.config import config
from ai_standards.core.pdf_processor import PDFProcessor
from ai_standards.models.ai_trainer import AIStandardsTrainer
from ai_standards.models.comparison_model import StandardsComparisonModel

def example_pdf_processing():
    """Example of processing PDF standards"""
    print("📄 Example: PDF Processing")
    print("-" * 40)
    
    # Initialize PDF processor
    processor = PDFProcessor()
    
    # Find PDF files in base directory
    pdf_files = list(config.BASE_PDFS_DIR.glob("*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in {config.BASE_PDFS_DIR}")
        return []
    
    print(f"Found {len(pdf_files)} PDF files:")
    for pdf_file in pdf_files:
        print(f"  - {pdf_file.name}")
    
    # Process first PDF as example
    pdf_file = pdf_files[0]
    print(f"\nProcessing: {pdf_file.name}")
    
    try:
        # Process PDF
        result = processor.process_pdf(pdf_file, target_language="en")
        
        print(f"✅ Processing successful!")
        print(f"  - Detected language: {result['detected_language']}")
        print(f"  - Text length: {len(result['processed_text']):,} characters")
        print(f"  - Number of chunks: {len(result['chunks'])}")
        print(f"  - Extraction method: {result['extraction_method']}")
        
        # Show structured data
        structured_data = result['structured_data']
        print(f"\n📊 Extracted structured data:")
        for key, values in structured_data.items():
            if values:
                print(f"  - {key.replace('_', ' ').title()}: {len(values)} items")
                if len(values) <= 3:  # Show first few values
                    print(f"    Values: {values}")
        
        return [result]
        
    except Exception as e:
        print(f"❌ Processing failed: {e}")
        return []

def example_model_training(processed_documents):
    """Example of training AI models"""
    print("\n🧠 Example: AI Model Training")
    print("-" * 40)
    
    if not processed_documents:
        print("No processed documents available for training")
        return None
    
    # Initialize AI trainer
    trainer = AIStandardsTrainer()
    
    try:
        # Create training data
        print("Creating training data...")
        training_data = trainer.create_training_data(processed_documents)
        
        print(f"✅ Training data created:")
        print(f"  - Total samples: {len(training_data['texts'])}")
        print(f"  - Categories: {len(set(training_data['labels']))}")
        
        # Train classification model
        print("\nTraining classification model...")
        classification_results = trainer.train_classification_model(training_data)
        
        print(f"✅ Classification model trained:")
        print(f"  - Accuracy: {classification_results['accuracy']:.4f}")
        print(f"  - Training samples: {classification_results['training_samples']}")
        print(f"  - Test samples: {classification_results['test_samples']}")
        
        # Store embeddings
        print("\nStoring embeddings...")
        storage_results = trainer.store_embeddings(training_data)
        
        if storage_results['status'] == 'completed':
            print(f"✅ Embeddings stored: {storage_results['stored_count']} embeddings")
        else:
            print(f"⚠️  Embedding storage: {storage_results['status']}")
        
        return classification_results
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        return None

def example_standards_comparison():
    """Example of comparing standards"""
    print("\n🔍 Example: Standards Comparison")
    print("-" * 40)
    
    # Find PDF files
    pdf_files = list(config.BASE_PDFS_DIR.glob("*.pdf"))
    
    if len(pdf_files) < 2:
        print("Need at least 2 PDF files for comparison")
        return None
    
    # Initialize comparison model
    comparison_model = StandardsComparisonModel()
    
    try:
        # Compare first two PDFs
        standard_a = pdf_files[0]
        standard_b = pdf_files[1]
        
        print(f"Comparing: {standard_a.name} vs {standard_b.name}")
        
        comparison_result = comparison_model.compare_standards(standard_a, standard_b)
        
        print(f"✅ Comparison completed!")
        print(f"  - Overall similarity: {comparison_result.similarity_score:.3f}")
        print(f"  - Compliance status: {comparison_result.compliance_status}")
        
        print(f"\n📊 Category scores:")
        for category, score in comparison_result.category_scores.items():
            print(f"  - {category.replace('_', ' ').title()}: {score:.3f}")
        
        if comparison_result.differences:
            print(f"\n⚠️  Key differences:")
            for diff in comparison_result.differences[:3]:  # Show first 3
                print(f"  - {diff}")
        
        if comparison_result.recommendations:
            print(f"\n💡 Recommendations:")
            for rec in comparison_result.recommendations[:3]:  # Show first 3
                print(f"  - {rec}")
        
        return comparison_result
        
    except Exception as e:
        print(f"❌ Comparison failed: {e}")
        return None

def example_similar_standards_search():
    """Example of finding similar standards"""
    print("\n🔎 Example: Similar Standards Search")
    print("-" * 40)
    
    # Find PDF files
    pdf_files = list(config.BASE_PDFS_DIR.glob("*.pdf"))
    
    if len(pdf_files) < 2:
        print("Need at least 2 PDF files for similarity search")
        return
    
    comparison_model = StandardsComparisonModel()
    
    try:
        # Use first PDF as query
        query_standard = pdf_files[0]
        print(f"Finding standards similar to: {query_standard.name}")
        
        similar_standards = comparison_model.find_similar_standards(query_standard, top_k=3)
        
        if similar_standards:
            print(f"✅ Found {len(similar_standards)} similar standards:")
            for result in similar_standards:
                print(f"  - {result['file_path']} (similarity: {result['similarity_score']:.3f})")
        else:
            print("No similar standards found")
        
    except Exception as e:
        print(f"❌ Similarity search failed: {e}")

def main():
    """Run all examples"""
    print("🚀 AI Standards Training System - Example Usage")
    print("=" * 60)
    
    # Example 1: PDF Processing
    processed_docs = example_pdf_processing()
    
    # Example 2: Model Training (if we have processed documents)
    if processed_docs:
        training_results = example_model_training(processed_docs)
    
    # Example 3: Standards Comparison
    comparison_result = example_standards_comparison()
    
    # Example 4: Similar Standards Search
    example_similar_standards_search()
    
    print("\n" + "=" * 60)
    print("✅ Example usage completed!")
    print("\nTo run the full system:")
    print("1. python main.py process  # Process all PDFs")
    print("2. python main.py train    # Train models")
    print("3. python main.py web      # Start web interface")
    print("4. python main.py demo     # Run complete demo")

if __name__ == "__main__":
    main()
