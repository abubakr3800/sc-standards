"""
Analyze Study - Command Line Interface
Quick command-line tool to analyze PDF lighting studies
"""
import argparse
import json
from pathlib import Path
from pdf_study_analyzer import PDFStudyAnalyzer
import sys

def main():
    """Main function for command-line analysis"""
    parser = argparse.ArgumentParser(description="Analyze PDF lighting studies")
    parser.add_argument("pdf_file", help="Path to PDF file to analyze")
    parser.add_argument("--output", "-o", help="Output file path (optional)")
    parser.add_argument("--format", "-f", choices=["json", "summary"], default="summary", 
                       help="Output format (default: summary)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Check if file exists
    pdf_path = Path(args.pdf_file)
    if not pdf_path.exists():
        print(f"❌ Error: File not found: {pdf_path}")
        sys.exit(1)
    
    if not pdf_path.suffix.lower() == '.pdf':
        print(f"❌ Error: File must be a PDF: {pdf_path}")
        sys.exit(1)
    
    print(f"🔍 Analyzing PDF study: {pdf_path.name}")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = PDFStudyAnalyzer()
    
    try:
        # Analyze the PDF
        result = analyzer.analyze_pdf_study(pdf_path)
        
        if args.format == "summary":
            # Print summary
            print_summary(result)
        else:
            # Print full JSON
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Save to output file if specified
        if args.output:
            output_path = Path(args.output)
            with open(output_path, 'w', encoding='utf-8') as f:
                if args.format == "summary":
                    summary_text = generate_summary_text(result)
                    f.write(summary_text)
                else:
                    json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Results saved to: {output_path}")
        
        print("\n✅ Analysis completed successfully!")
        
    except Exception as e:
        print(f"❌ Error analyzing PDF: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

def print_summary(result):
    """Print a formatted summary of the analysis"""
    print(f"📊 ANALYSIS SUMMARY")
    print(f"File: {result['file_name']}")
    print(f"Date: {result['analysis_date'][:10]}")
    print()
    
    # Summary metrics
    summary = result['summary']
    print(f"🏢 Rooms Analyzed: {summary['total_rooms_analyzed']}")
    print(f"📊 Parameters Found: {sum(summary['parameters_found'].values())}")
    print(f"✅ Overall Compliance: {summary['overall_compliance'].upper()}")
    print()
    
    # Key findings
    if summary['key_findings']:
        print("🔍 KEY FINDINGS:")
        for finding in summary['key_findings']:
            print(f"  • {finding}")
        print()
    
    # Recommendations
    if summary['recommendations']:
        print("💡 RECOMMENDATIONS:")
        for rec in summary['recommendations']:
            print(f"  • {rec}")
        print()
    
    # Room analysis
    if result['room_data']:
        print("🏢 ROOM ANALYSIS:")
        for room in result['room_data']:
            print(f"  📋 {room['name']}")
            if room.get('illuminance'):
                print(f"     Illuminance: {room['illuminance']['value']} lux")
            if room.get('ugr'):
                print(f"     UGR: {room['ugr']['value']}")
            if room.get('cri'):
                print(f"     CRI: {room['cri']['value']}")
            if room.get('uniformity'):
                print(f"     Uniformity: {room['uniformity']['value']}")
        print()
    
    # Compliance analysis
    if result['compliance_analysis']['room_compliance']:
        print("✅ COMPLIANCE ANALYSIS:")
        for room_comp in result['compliance_analysis']['room_compliance']:
            status_emoji = "🟢" if room_comp['status'] == 'compliant' else "🔴" if room_comp['status'] == 'non_compliant' else "🟡"
            print(f"  {status_emoji} {room_comp['room_name']}: {room_comp['status'].upper()}")
            
            if room_comp['issues']:
                for issue in room_comp['issues']:
                    print(f"     ❌ {issue}")
            
            if room_comp['recommendations']:
                for rec in room_comp['recommendations']:
                    print(f"     ✅ {rec}")
        print()
    
    # Extracted data summary
    print("📊 EXTRACTED DATA:")
    for param_type, values in result['extracted_data'].items():
        if values:
            print(f"  {param_type.title()}: {len(values)} values found")
            for i, value in enumerate(values[:3]):  # Show first 3 values
                print(f"    {i+1}. {value['value']} (confidence: {value['confidence']:.2f})")
            if len(values) > 3:
                print(f"    ... and {len(values) - 3} more")
    print()

def generate_summary_text(result):
    """Generate markdown summary text"""
    summary = result['summary']
    
    text = f"""# Lighting Study Analysis Report

## File: {result['file_name']}
## Analysis Date: {result['analysis_date']}

## Summary
- **Rooms Analyzed:** {summary['total_rooms_analyzed']}
- **Overall Compliance:** {summary['overall_compliance']}
- **Parameters Found:** {sum(summary['parameters_found'].values())}

## Key Findings
"""
    
    for finding in summary['key_findings']:
        text += f"- {finding}\n"
    
    text += "\n## Recommendations\n"
    for rec in summary['recommendations']:
        text += f"- {rec}\n"
    
    if result['room_data']:
        text += "\n## Room Analysis\n"
        for room in result['room_data']:
            text += f"\n### {room['name']}\n"
            if room.get('illuminance'):
                text += f"- Illuminance: {room['illuminance']['value']} lux\n"
            if room.get('ugr'):
                text += f"- UGR: {room['ugr']['value']}\n"
            if room.get('cri'):
                text += f"- CRI: {room['cri']['value']}\n"
            if room.get('uniformity'):
                text += f"- Uniformity: {room['uniformity']['value']}\n"
    
    if result['compliance_analysis']['room_compliance']:
        text += "\n## Compliance Analysis\n"
        for room_comp in result['compliance_analysis']['room_compliance']:
            text += f"\n### {room_comp['room_name']} - {room_comp['status'].title()}\n"
            
            if room_comp['issues']:
                text += "**Issues:**\n"
                for issue in room_comp['issues']:
                    text += f"- {issue}\n"
            
            if room_comp['recommendations']:
                text += "**Recommendations:**\n"
                for rec in room_comp['recommendations']:
                    text += f"- {rec}\n"
    
    return text

if __name__ == "__main__":
    main()
