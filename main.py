"""
Main entry point for the AI Standards Training System
"""
import sys
import argparse
from pathlib import Path
from loguru import logger

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from ai_standards.core.config import config
from ai_standards.core.simple_pdf_processor import SimplePDFProcessor
from ai_standards.models.ai_trainer import AIStandardsTrainer
from ai_standards.models.comparison_model import StandardsComparisonModel
from ai_standards.web.web_interface import run_streamlit, run_fastapi

def setup_logging():
    """Setup logging configuration"""
    logger.remove()  # Remove default handler
    
    # Add console handler
    logger.add(
        sys.stderr,
        format=config.LOGGING["format"],
        level=config.LOGGING["level"],
        colorize=True
    )
    
    # Add file handler
    logger.add(
        config.LOGGING["file"],
        format=config.LOGGING["format"],
        level=config.LOGGING["level"],
        rotation="10 MB",
        retention="7 days"
    )

def process_pdfs_from_directory(pdf_directory: Path, target_language: str = "en"):
    """Process all PDFs in a directory"""
    logger.info(f"Processing PDFs from directory: {pdf_directory}")
    
    pdf_processor = SimplePDFProcessor()
    pdf_files = list(pdf_directory.glob("*.pdf"))
    
    if not pdf_files:
        logger.warning(f"No PDF files found in {pdf_directory}")
        return []
    
    processed_documents = []
    
    for pdf_file in pdf_files:
        try:
            logger.info(f"Processing {pdf_file.name}")
            processed_doc = pdf_processor.process_pdf(pdf_file, target_language)
            processed_documents.append(processed_doc)
            
            # Save processed document
            output_path = config.UPLOADS_DIR / f"{pdf_file.stem}_processed.json"
            import json
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(processed_doc, f, indent=2, default=str)
            
            logger.info(f"Successfully processed {pdf_file.name}")
            
        except Exception as e:
            logger.error(f"Failed to process {pdf_file.name}: {e}")
    
    logger.info(f"Processed {len(processed_documents)} out of {len(pdf_files)} PDFs")
    return processed_documents

def train_models_from_processed_data():
    """Train models from processed data"""
    logger.info("Training models from processed data")
    
    ai_trainer = AIStandardsTrainer()
    
    # Find processed documents
    processed_files = list(config.UPLOADS_DIR.glob("*_processed.json"))
    
    if not processed_files:
        logger.error("No processed documents found")
        return None
    
    # Load processed documents
    import json
    processed_documents = []
    for file_path in processed_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            doc_data = json.load(f)
            processed_documents.append(doc_data)
    
    # Train models
    results = ai_trainer.train_complete_pipeline([Path(doc['file_path']) for doc in processed_documents])
    
    logger.info("Model training completed")
    return results

def compare_standards_cli(standard_a: Path, standard_b: Path):
    """Compare two standards from command line"""
    logger.info(f"Comparing standards: {standard_a.name} vs {standard_b.name}")
    
    comparison_model = StandardsComparisonModel()
    
    try:
        comparison_result = comparison_model.compare_standards(standard_a, standard_b)
        
        print(f"\n=== Comparison Results ===")
        print(f"Standard A: {comparison_result.standard_a}")
        print(f"Standard B: {comparison_result.standard_b}")
        print(f"Overall Similarity: {comparison_result.similarity_score:.3f}")
        print(f"Compliance Status: {comparison_result.compliance_status}")
        
        print(f"\n=== Category Scores ===")
        for category, score in comparison_result.category_scores.items():
            print(f"{category.replace('_', ' ').title()}: {score:.3f}")
        
        if comparison_result.differences:
            print(f"\n=== Key Differences ===")
            for diff in comparison_result.differences:
                print(f"- {diff}")
        
        if comparison_result.recommendations:
            print(f"\n=== Recommendations ===")
            for rec in comparison_result.recommendations:
                print(f"- {rec}")
        
        return comparison_result
        
    except Exception as e:
        logger.error(f"Comparison failed: {e}")
        return None

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="AI Standards Training System")
    parser.add_argument("command", choices=[
        "process", "train", "compare", "web", "api", "demo", "dialux"
    ], help="Command to execute")
    
    parser.add_argument("--input-dir", type=Path, default=config.BASE_PDFS_DIR,
                       help="Input directory for PDF files")
    parser.add_argument("--target-language", default="en",
                       help="Target language for translation")
    parser.add_argument("--standard-a", type=Path,
                       help="Path to first standard for comparison")
    parser.add_argument("--standard-b", type=Path,
                       help="Path to second standard for comparison")
    parser.add_argument("--host", default="0.0.0.0",
                       help="Host for API server")
    parser.add_argument("--port", type=int, default=8000,
                       help="Port for API server")
    parser.add_argument("--file", type=Path,
                       help="Path to Dialux PDF file for processing")
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging()
    
    logger.info("Starting AI Standards Training System")
    
    if args.command == "process":
        # Process PDFs from directory
        processed_docs = process_pdfs_from_directory(args.input_dir, args.target_language)
        logger.info(f"Processing completed. {len(processed_docs)} documents processed.")
        
    elif args.command == "train":
        # Train models
        results = train_models_from_processed_data()
        if results:
            logger.info("Training completed successfully")
        else:
            logger.error("Training failed")
            
    elif args.command == "compare":
        # Compare two standards
        if not args.standard_a or not args.standard_b:
            logger.error("Both --standard-a and --standard-b are required for comparison")
            return
        
        if not args.standard_a.exists() or not args.standard_b.exists():
            logger.error("One or both standard files do not exist")
            return
        
        comparison_result = compare_standards_cli(args.standard_a, args.standard_b)
        
    elif args.command == "web":
        # Run Streamlit web interface
        logger.info("Starting Streamlit web interface")
        run_streamlit()
        
    elif args.command == "api":
        # Run FastAPI server
        logger.info(f"Starting FastAPI server on {args.host}:{args.port}")
        config.API["host"] = args.host
        config.API["port"] = args.port
        run_fastapi()
        
    elif args.command == "demo":
        # Run demo with existing PDFs
        logger.info("Running demo with existing PDFs")
        
        # Process existing PDFs
        pdf_files = list(config.BASE_PDFS_DIR.glob("*.pdf"))
        
        if not pdf_files:
            logger.error(f"No PDF files found in {config.BASE_PDFS_DIR}")
            return
        
        logger.info(f"Found {len(pdf_files)} PDF files")
        
        # Process PDFs
        processed_docs = process_pdfs_from_directory(config.BASE_PDFS_DIR)
        
        if len(processed_docs) >= 2:
            # Train models
            results = train_models_from_processed_data()
            
            if results and results.get("overall_status") == "completed":
                # Compare first two standards
                comparison_result = compare_standards_cli(pdf_files[0], pdf_files[1])
                
                logger.info("Demo completed successfully!")
            else:
                logger.error("Demo failed during model training")
        else:
            logger.warning("Need at least 2 PDF files for comparison demo")
            
    elif args.command == "dialux":
        # Process Dialux PDF report
        if not args.file:
            logger.error("--file argument is required for Dialux processing")
            return
        
        if not args.file.exists():
            logger.error(f"Dialux PDF file not found: {args.file}")
            return
        
        logger.info(f"Processing Dialux PDF: {args.file}")
        try:
            from dialux_pdf_processor import DialuxPDFProcessor, evaluate_dialux_pdf
            evaluate_dialux_pdf()
        except ImportError:
            logger.error("Dialux processor not available")
        except Exception as e:
            logger.error(f"Failed to process Dialux PDF: {e}")

if __name__ == "__main__":
    main()