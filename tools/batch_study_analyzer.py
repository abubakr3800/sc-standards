"""
Batch Study Analyzer
Analyze multiple PDF lighting studies at once
"""
import json
from pathlib import Path
from typing import List, Dict
from pdf_study_analyzer import PDFStudyAnalyzer
import pandas as pd
from datetime import datetime
import argparse
import sys

class BatchStudyAnalyzer:
    """Analyze multiple PDF studies in batch"""
    
    def __init__(self):
        self.analyzer = PDFStudyAnalyzer()
        self.results = []
    
    def analyze_folder(self, folder_path: Path, recursive: bool = False) -> List[Dict]:
        """Analyze all PDF files in a folder"""
        print(f"🔍 Analyzing PDFs in folder: {folder_path}")
        print("=" * 60)
        
        # Find PDF files
        if recursive:
            pdf_files = list(folder_path.rglob("*.pdf"))
        else:
            pdf_files = list(folder_path.glob("*.pdf"))
        
        if not pdf_files:
            print(f"❌ No PDF files found in {folder_path}")
            return []
        
        print(f"📁 Found {len(pdf_files)} PDF files")
        print()
        
        # Analyze each PDF
        for i, pdf_file in enumerate(pdf_files, 1):
            print(f"[{i}/{len(pdf_files)}] Analyzing: {pdf_file.name}")
            try:
                result = self.analyzer.analyze_pdf_study(pdf_file)
                self.results.append(result)
                print(f"✅ Completed: {pdf_file.name}")
            except Exception as e:
                print(f"❌ Error analyzing {pdf_file.name}: {e}")
                # Add error result
                error_result = {
                    "file_name": pdf_file.name,
                    "error": str(e),
                    "analysis_date": datetime.now().isoformat()
                }
                self.results.append(error_result)
            print()
        
        return self.results
    
    def generate_batch_report(self) -> Dict:
        """Generate comprehensive batch analysis report"""
        if not self.results:
            return {"error": "No results to report"}
        
        # Separate successful and failed analyses
        successful_results = [r for r in self.results if 'error' not in r]
        failed_results = [r for r in self.results if 'error' in r]
        
        # Calculate overall statistics
        total_files = len(self.results)
        successful_files = len(successful_results)
        failed_files = len(failed_results)
        
        # Calculate compliance statistics
        compliance_stats = {
            'compliant': 0,
            'non_compliant': 0,
            'mixed': 0,
            'no_data': 0
        }
        
        total_rooms = 0
        total_parameters = 0
        
        for result in successful_results:
            if 'summary' in result:
                compliance = result['summary'].get('overall_compliance', 'no_data')
                compliance_stats[compliance] = compliance_stats.get(compliance, 0) + 1
                
                total_rooms += result['summary'].get('total_rooms_analyzed', 0)
                total_parameters += sum(result['summary'].get('parameters_found', {}).values())
        
        # Generate report
        report = {
            "batch_analysis_date": datetime.now().isoformat(),
            "summary": {
                "total_files": total_files,
                "successful_analyses": successful_files,
                "failed_analyses": failed_files,
                "success_rate": f"{(successful_files/total_files)*100:.1f}%" if total_files > 0 else "0%",
                "total_rooms_analyzed": total_rooms,
                "total_parameters_found": total_parameters
            },
            "compliance_statistics": compliance_stats,
            "file_results": self.results,
            "recommendations": self._generate_batch_recommendations(successful_results, compliance_stats)
        }
        
        return report
    
    def _generate_batch_recommendations(self, successful_results: List[Dict], compliance_stats: Dict) -> List[str]:
        """Generate recommendations based on batch analysis"""
        recommendations = []
        
        # Overall compliance recommendations
        if compliance_stats['non_compliant'] > compliance_stats['compliant']:
            recommendations.append("Most studies show non-compliance issues. Review lighting design standards.")
        
        if compliance_stats['no_data'] > 0:
            recommendations.append(f"{compliance_stats['no_data']} studies had insufficient data. Check PDF quality and content.")
        
        # Parameter-specific recommendations
        all_parameters = {}
        for result in successful_results:
            if 'extracted_data' in result:
                for param_type, values in result['extracted_data'].items():
                    if param_type not in all_parameters:
                        all_parameters[param_type] = 0
                    all_parameters[param_type] += len(values)
        
        if all_parameters:
            most_common_param = max(all_parameters, key=all_parameters.get)
            recommendations.append(f"Most commonly found parameter: {most_common_param} ({all_parameters[most_common_param]} values)")
        
        # Room analysis recommendations
        total_rooms = sum(r.get('summary', {}).get('total_rooms_analyzed', 0) for r in successful_results)
        if total_rooms > 0:
            recommendations.append(f"Analyzed {total_rooms} rooms across all studies. Consider room-specific compliance requirements.")
        
        return recommendations
    
    def save_batch_report(self, output_path: Path):
        """Save batch analysis report to file"""
        report = self.generate_batch_report()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Batch report saved to: {output_path}")
    
    def print_batch_summary(self):
        """Print formatted batch analysis summary"""
        report = self.generate_batch_report()
        
        print("📊 BATCH ANALYSIS SUMMARY")
        print("=" * 60)
        
        summary = report['summary']
        print(f"📁 Total Files: {summary['total_files']}")
        print(f"✅ Successful: {summary['successful_analyses']}")
        print(f"❌ Failed: {summary['failed_analyses']}")
        print(f"📈 Success Rate: {summary['success_rate']}")
        print(f"🏢 Total Rooms: {summary['total_rooms_analyzed']}")
        print(f"📊 Total Parameters: {summary['total_parameters_found']}")
        print()
        
        # Compliance statistics
        print("✅ COMPLIANCE STATISTICS:")
        compliance_stats = report['compliance_statistics']
        for status, count in compliance_stats.items():
            if count > 0:
                emoji = "🟢" if status == "compliant" else "🔴" if status == "non_compliant" else "🟡" if status == "mixed" else "⚪"
                print(f"  {emoji} {status.title()}: {count} files")
        print()
        
        # Recommendations
        if report['recommendations']:
            print("💡 RECOMMENDATIONS:")
            for rec in report['recommendations']:
                print(f"  • {rec}")
            print()
        
        # Individual file results
        print("📋 INDIVIDUAL FILE RESULTS:")
        for result in report['file_results']:
            if 'error' in result:
                print(f"  ❌ {result['file_name']}: ERROR - {result['error']}")
            else:
                compliance = result.get('summary', {}).get('overall_compliance', 'unknown')
                emoji = "🟢" if compliance == "compliant" else "🔴" if compliance == "non_compliant" else "🟡"
                rooms = result.get('summary', {}).get('total_rooms_analyzed', 0)
                print(f"  {emoji} {result['file_name']}: {compliance.upper()} ({rooms} rooms)")

def main():
    """Main function for batch analysis"""
    parser = argparse.ArgumentParser(description="Batch analyze PDF lighting studies")
    parser.add_argument("folder", help="Folder containing PDF files to analyze")
    parser.add_argument("--output", "-o", help="Output file for batch report (optional)")
    parser.add_argument("--recursive", "-r", action="store_true", help="Search subdirectories recursively")
    parser.add_argument("--format", "-f", choices=["summary", "json"], default="summary", 
                       help="Output format (default: summary)")
    
    args = parser.parse_args()
    
    # Check if folder exists
    folder_path = Path(args.folder)
    if not folder_path.exists():
        print(f"❌ Error: Folder not found: {folder_path}")
        sys.exit(1)
    
    if not folder_path.is_dir():
        print(f"❌ Error: Path is not a directory: {folder_path}")
        sys.exit(1)
    
    # Initialize batch analyzer
    batch_analyzer = BatchStudyAnalyzer()
    
    try:
        # Analyze folder
        results = batch_analyzer.analyze_folder(folder_path, args.recursive)
        
        if not results:
            print("❌ No results to report")
            sys.exit(1)
        
        # Print summary
        if args.format == "summary":
            batch_analyzer.print_batch_summary()
        else:
            # Print full JSON
            report = batch_analyzer.generate_batch_report()
            print(json.dumps(report, indent=2, ensure_ascii=False))
        
        # Save to output file if specified
        if args.output:
            output_path = Path(args.output)
            batch_analyzer.save_batch_report(output_path)
        
        print("\n✅ Batch analysis completed successfully!")
        
    except Exception as e:
        print(f"❌ Error in batch analysis: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
