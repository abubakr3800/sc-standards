"""
Reliable Standards Processing Script
Automatically processes all PDFs in base/ folder and creates processed documents
"""
import sys
import json
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

def process_all_standards():
    """Process all PDF standards in the base/ folder"""
    print("🚀 AI Standards Processing System")
    print("=" * 50)
    
    try:
        from ai_standards.core.config import config
        from ai_standards.core.simple_pdf_processor import SimplePDFProcessor
        
        # Check directories
        print(f"📁 Base PDFs directory: {config.BASE_PDFS_DIR}")
        print(f"📁 Uploads directory: {config.UPLOADS_DIR}")
        
        if not config.BASE_PDFS_DIR.exists():
            print(f"❌ Base directory does not exist: {config.BASE_PDFS_DIR}")
            return False
        
        if not config.UPLOADS_DIR.exists():
            print(f"📁 Creating uploads directory: {config.UPLOADS_DIR}")
            config.UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Find PDF files
        pdf_files = list(config.BASE_PDFS_DIR.glob("*.pdf"))
        print(f"📄 Found {len(pdf_files)} PDF files to process")
        
        if not pdf_files:
            print("❌ No PDF files found in base/ directory")
            print("Please add PDF files to the base/ folder and try again")
            return False
        
        # List PDF files
        for i, pdf_file in enumerate(pdf_files, 1):
            print(f"  {i}. {pdf_file.name}")
        
        # Create processor
        print("\n🔧 Initializing PDF processor...")
        processor = SimplePDFProcessor()
        print("✅ PDF processor ready")
        
        # Process each PDF
        processed_count = 0
        failed_count = 0
        
        for pdf_file in pdf_files:
            try:
                print(f"\n📄 Processing: {pdf_file.name}")
                print("-" * 40)
                
                # Process the PDF
                result = processor.process_pdf(pdf_file)
                
                if result:
                    # Save processed document
                    output_filename = f"{pdf_file.stem}_processed.json"
                    output_path = config.UPLOADS_DIR / output_filename
                    
                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(result, f, indent=2, ensure_ascii=False, default=str)
                    
                    print(f"✅ Successfully processed and saved: {output_filename}")
                    print(f"   📊 Text length: {len(result.get('text_content', ''))} characters")
                    print(f"   📋 Tables found: {len(result.get('tables', []))}")
                    print(f"   🏷️  Categories: {', '.join(result.get('metadata', {}).get('categories', []))}")
                    print(f"   🔤 Language: {result.get('language', 'unknown')}")
                    
                    processed_count += 1
                else:
                    print(f"❌ Failed to process: {pdf_file.name}")
                    failed_count += 1
                    
            except Exception as e:
                print(f"❌ Error processing {pdf_file.name}: {e}")
                failed_count += 1
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 PROCESSING SUMMARY")
        print("=" * 50)
        print(f"✅ Successfully processed: {processed_count} files")
        print(f"❌ Failed to process: {failed_count} files")
        print(f"📁 Total files: {len(pdf_files)} files")
        
        if processed_count > 0:
            print(f"\n📁 Processed files saved to: {config.UPLOADS_DIR}")
            processed_files = list(config.UPLOADS_DIR.glob("*_processed.json"))
            print(f"📄 Created {len(processed_files)} processed documents:")
            for file in processed_files:
                print(f"   - {file.name}")
            
            print(f"\n🎉 Processing completed successfully!")
            print(f"💡 You can now run: py main.py train")
            return True
        else:
            print(f"\n❌ No files were processed successfully")
            return False
            
    except Exception as e:
        print(f"❌ Critical error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    success = process_all_standards()
    
    if success:
        print(f"\n🚀 Next steps:")
        print(f"   1. Train AI models: py main.py train")
        print(f"   2. Start web interface: py main.py web")
        print(f"   3. Compare standards: py main.py compare")
    else:
        print(f"\n❌ Processing failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
