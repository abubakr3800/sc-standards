"""
Quick Realistic Lighting Evaluator
Simple version with more accurate evaluation criteria
"""
import sys
from pathlib import Path

def quick_realistic_evaluate(folder_path: str):
    """Quickly evaluate all PDFs in a folder with realistic criteria"""
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"❌ Folder not found: {folder}")
        return
    
    pdf_files = list(folder.glob("*.pdf"))
    if not pdf_files:
        print(f"❌ No PDF files found in {folder}")
        return
    
    print(f"🚀 Quick Realistic Lighting Evaluator")
    print(f"📁 Folder: {folder}")
    print(f"📄 Found {len(pdf_files)} PDF files")
    print("=" * 50)
    
    # Import the realistic evaluator
    try:
        from realistic_lighting_evaluator import process_folder_realistic
        
        # Process all PDFs
        results = process_folder_realistic(folder)
        
        if not results:
            print("❌ No results to report")
            return
        
        # Calculate summary
        total_files = len(results)
        successful_files = len([r for r in results if r['status'] == 'SUCCESS'])
        
        if successful_files > 0:
            avg_compliance = sum(r['compliance_score'] for r in results if r['status'] == 'SUCCESS') / successful_files
            
            # Count by status
            excellent = len([r for r in results if r.get('overall_status') == 'EXCELLENT'])
            good = len([r for r in results if r.get('overall_status') == 'GOOD'])
            acceptable = len([r for r in results if r.get('overall_status') == 'ACCEPTABLE'])
            poor = len([r for r in results if r.get('overall_status') == 'POOR'])
            fail = len([r for r in results if r.get('overall_status') == 'FAIL'])
        else:
            avg_compliance = 0
            excellent = good = acceptable = poor = fail = 0
        
        # Print summary
        print("\n" + "=" * 50)
        print("📊 REALISTIC EVALUATION SUMMARY")
        print("=" * 50)
        print(f"Total PDFs: {total_files}")
        print(f"Successfully processed: {successful_files}")
        print(f"Average compliance: {avg_compliance:.1f}%")
        print()
        print("Status breakdown:")
        print(f"  🎉 Excellent: {excellent}")
        print(f"  ✅ Good: {good}")
        print(f"  ⚠️ Acceptable: {acceptable}")
        print(f"  ❌ Poor: {poor}")
        print(f"  💥 Fail: {fail}")
        
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
        
        # Show recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if avg_compliance >= 90:
            print("🎉 Excellent overall compliance! Your lighting studies meet high standards.")
        elif avg_compliance >= 80:
            print("✅ Good overall compliance. Your lighting studies are well-designed.")
        elif avg_compliance >= 70:
            print("⚠️ Acceptable compliance. Some improvements could be made.")
        else:
            print("❌ Poor compliance. Significant improvements are required.")
        
    except ImportError:
        print("❌ Could not import realistic evaluator")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main function"""
    if len(sys.argv) > 1:
        # Use command line argument
        folder_path = sys.argv[1]
        quick_realistic_evaluate(folder_path)
    else:
        # Interactive mode
        folder_path = input("Enter path to folder containing PDFs: ").strip()
        if folder_path:
            quick_realistic_evaluate(folder_path)
        else:
            print("❌ No folder path provided")

if __name__ == "__main__":
    main()
