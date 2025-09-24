"""
Simple PDF processing script to create processed documents
"""
import sys
import json
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    print("🚀 Processing PDFs...")
    
    try:
        from ai_standards.core.config import config
        from ai_standards.core.pdf_processor import PDFProcessor
        
        print(f"Base PDFs directory: {config.BASE_PDFS_DIR}")
        print(f"Uploads directory: {config.UPLOADS_DIR}")
        
        # Find PDF files
        pdf_files = list(config.BASE_PDFS_DIR.glob("*.pdf"))
        print(f"Found {len(pdf_files)} PDF files")
        
        if not pdf_files:
            print("❌ No PDF files found in base/ directory")
            return
        
        # Create processor
        processor = PDFProcessor()
        print("✅ PDFProcessor created")
        
        # Process each PDF
        processed_count = 0
        for pdf_file in pdf_files:
            try:
                print(f"\n📄 Processing: {pdf_file.name}")
                
                # Process the PDF
                result = processor.process_pdf(pdf_file)
                
                if result:
                    # Save processed document
                    output_path = config.UPLOADS_DIR / f"{pdf_file.stem}_processed.json"
                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(result, f, indent=2, default=str)
                    
                    print(f"✅ Saved: {output_path.name}")
                    processed_count += 1
                else:
                    print(f"❌ Failed to process: {pdf_file.name}")
                    
            except Exception as e:
                print(f"❌ Error processing {pdf_file.name}: {e}")
        
        print(f"\n🎉 Processed {processed_count} out of {len(pdf_files)} PDFs")
        
        # List processed files
        processed_files = list(config.UPLOADS_DIR.glob("*_processed.json"))
        print(f"Created {len(processed_files)} processed files:")
        for file in processed_files:
            print(f"  - {file.name}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
