"""
Quick Batch PDF Evaluator
Simple version that processes all PDFs in a folder
"""
import sys
from pathlib import Path

def quick_evaluate_folder(folder_path: str):
    """Quickly evaluate all PDFs in a folder"""
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"❌ Folder not found: {folder}")
        return
    
    pdf_files = list(folder.glob("*.pdf"))
    if not pdf_files:
        print(f"❌ No PDF files found in {folder}")
        return
    
    print(f"🚀 Quick Batch PDF Evaluator")
    print(f"📁 Folder: {folder}")
    print(f"📄 Found {len(pdf_files)} PDF files")
    print("=" * 50)
    
    # Import the batch evaluator
    try:
        from batch_pdf_evaluator import process_folder, generate_summary_report
        
        # Process all PDFs
        results = process_folder(folder)
        
        if not results:
            print("❌ No results to report")
            return
        
        # Generate and print summary
        summary = generate_summary_report(results)
        
        print("\n" + "=" * 50)
        print("📊 QUICK SUMMARY")
        print("=" * 50)
        print(f"Total PDFs: {summary['total_files']}")
        print(f"Successfully processed: {summary['successful_files']}")
        print(f"Failed: {summary['failed_files']}")
        
        if summary['successful_files'] > 0:
            print(f"Average compliance: {summary['average_compliance']:.1f}%")
            print()
            print("Status breakdown:")
            print(f"  🎉 Excellent: {summary['status_breakdown']['excellent']}")
            print(f"  ✅ Good: {summary['status_breakdown']['good']}")
            print(f"  ⚠️ Acceptable: {summary['status_breakdown']['acceptable']}")
            print(f"  ❌ Poor: {summary['status_breakdown']['poor']}")
            print(f"  💥 Fail: {summary['status_breakdown']['fail']}")
        
        # Show individual results
        print(f"\n📋 INDIVIDUAL RESULTS:")
        for result in results:
            if result['status'] == 'SUCCESS':
                status_icon = "🎉" if result['overall_status'] == 'EXCELLENT' else \
                             "✅" if result['overall_status'] == 'GOOD' else \
                             "⚠️" if result['overall_status'] == 'ACCEPTABLE' else \
                             "❌" if result['overall_status'] == 'POOR' else "💥"
                print(f"  {status_icon} {result['file_name']}: {result['overall_status']} ({result['compliance_score']:.1f}%)")
            else:
                print(f"  ❌ {result['file_name']}: FAILED - {result.get('error', 'Unknown error')}")
        
    except ImportError:
        print("❌ Could not import batch evaluator")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main function"""
    if len(sys.argv) > 1:
        # Use command line argument
        folder_path = sys.argv[1]
        quick_evaluate_folder(folder_path)
    else:
        # Interactive mode
        folder_path = input("Enter path to folder containing PDFs: ").strip()
        if folder_path:
            quick_evaluate_folder(folder_path)
        else:
            print("❌ No folder path provided")

if __name__ == "__main__":
    main()
