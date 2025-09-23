"""
Batch PDF Evaluator
Processes all PDFs in a folder and evaluates them against lighting standards
"""
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract text from PDF using multiple methods"""
    text = ""
    
    # Try pdfplumber first
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"pdfplumber failed for {pdf_path.name}: {e}")
    
    # Try PyMuPDF as fallback
    if not text:
        try:
            import fitz
            doc = fitz.open(pdf_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                page_text = page.get_text()
                if page_text:
                    text += page_text + "\n"
            doc.close()
        except Exception as e:
            print(f"PyMuPDF failed for {pdf_path.name}: {e}")
    
    return text

def extract_lighting_parameters(text: str) -> Dict:
    """Extract lighting parameters from text"""
    import re
    
    parameters = {
        'illuminance': [],
        'ugr': [],
        'area': [],
        'power_density': [],
        'uniformity': [],
        'cri': []
    }
    
    # Extract illuminance values
    illuminance_matches = re.findall(r'(\d+(?:\.\d+)?)\s*lux', text, re.IGNORECASE)
    parameters['illuminance'] = [float(x) for x in illuminance_matches]
    
    # Extract UGR values
    ugr_matches = re.findall(r'UGR[:\s]*(\d+(?:\.\d+)?)', text, re.IGNORECASE)
    parameters['ugr'] = [float(x) for x in ugr_matches]
    
    # Extract area values
    area_matches = re.findall(r'(\d+(?:\.\d+)?)\s*m²', text, re.IGNORECASE)
    parameters['area'] = [float(x) for x in area_matches]
    
    # Extract power density
    power_matches = re.findall(r'(\d+(?:\.\d+)?)\s*W/m²', text, re.IGNORECASE)
    parameters['power_density'] = [float(x) for x in power_matches]
    
    # Extract uniformity
    uniformity_matches = re.findall(r'uniformity[:\s]*(\d+(?:\.\d+)?)', text, re.IGNORECASE)
    parameters['uniformity'] = [float(x) for x in uniformity_matches]
    
    # Extract CRI
    cri_matches = re.findall(r'CRI[:\s]*(\d+(?:\.\d+)?)', text, re.IGNORECASE)
    parameters['cri'] = [float(x) for x in cri_matches]
    
    return parameters

def evaluate_parameters(parameters: Dict) -> Dict:
    """Evaluate parameters against standards"""
    results = {
        'illuminance': {'status': 'UNKNOWN', 'recommendation': ''},
        'ugr': {'status': 'UNKNOWN', 'recommendation': ''},
        'power_density': {'status': 'UNKNOWN', 'recommendation': ''},
        'uniformity': {'status': 'UNKNOWN', 'recommendation': ''},
        'cri': {'status': 'UNKNOWN', 'recommendation': ''}
    }
    
    # Evaluate illuminance (office standard: 300-1000 lux, recommended 500 lux)
    if parameters['illuminance']:
        avg_illuminance = sum(parameters['illuminance']) / len(parameters['illuminance'])
        if 300 <= avg_illuminance <= 1000:
            if 450 <= avg_illuminance <= 550:
                results['illuminance'] = {'status': 'PASS', 'recommendation': f'Excellent illuminance: {avg_illuminance:.0f} lux'}
            else:
                results['illuminance'] = {'status': 'PASS', 'recommendation': f'Good illuminance: {avg_illuminance:.0f} lux (consider 500 lux for optimal)'}
        else:
            results['illuminance'] = {'status': 'FAIL', 'recommendation': f'Poor illuminance: {avg_illuminance:.0f} lux (should be 300-1000 lux)'}
    
    # Evaluate UGR (office standard: ≤19, recommended ≤16)
    if parameters['ugr']:
        max_ugr = max(parameters['ugr'])
        if max_ugr <= 16:
            results['ugr'] = {'status': 'PASS', 'recommendation': f'Excellent UGR: {max_ugr:.1f}'}
        elif max_ugr <= 19:
            results['ugr'] = {'status': 'PASS', 'recommendation': f'Acceptable UGR: {max_ugr:.1f} (consider reducing to ≤16)'}
        else:
            results['ugr'] = {'status': 'FAIL', 'recommendation': f'Poor UGR: {max_ugr:.1f} (should be ≤19)'}
    
    # Evaluate power density (office standard: ≤3.5 W/m², recommended ≤2.5 W/m²)
    if parameters['power_density']:
        avg_power = sum(parameters['power_density']) / len(parameters['power_density'])
        if avg_power <= 2.5:
            results['power_density'] = {'status': 'PASS', 'recommendation': f'Excellent power density: {avg_power:.2f} W/m²'}
        elif avg_power <= 3.5:
            results['power_density'] = {'status': 'PASS', 'recommendation': f'Good power density: {avg_power:.2f} W/m²'}
        else:
            results['power_density'] = {'status': 'FAIL', 'recommendation': f'Poor power density: {avg_power:.2f} W/m² (should be ≤3.5 W/m²)'}
    
    # Evaluate uniformity (office standard: ≥0.6, recommended ≥0.8)
    if parameters['uniformity']:
        avg_uniformity = sum(parameters['uniformity']) / len(parameters['uniformity'])
        if avg_uniformity >= 0.8:
            results['uniformity'] = {'status': 'PASS', 'recommendation': f'Excellent uniformity: {avg_uniformity:.2f}'}
        elif avg_uniformity >= 0.6:
            results['uniformity'] = {'status': 'PASS', 'recommendation': f'Good uniformity: {avg_uniformity:.2f} (consider improving to ≥0.8)'}
        else:
            results['uniformity'] = {'status': 'FAIL', 'recommendation': f'Poor uniformity: {avg_uniformity:.2f} (should be ≥0.6)'}
    
    # Evaluate CRI (office standard: ≥80, recommended ≥90)
    if parameters['cri']:
        min_cri = min(parameters['cri'])
        if min_cri >= 90:
            results['cri'] = {'status': 'PASS', 'recommendation': f'Excellent CRI: {min_cri:.0f}'}
        elif min_cri >= 80:
            results['cri'] = {'status': 'PASS', 'recommendation': f'Good CRI: {min_cri:.0f} (consider ≥90 for better color rendering)'}
        else:
            results['cri'] = {'status': 'FAIL', 'recommendation': f'Poor CRI: {min_cri:.0f} (should be ≥80)'}
    
    return results

def calculate_compliance_score(results: Dict) -> float:
    """Calculate overall compliance score"""
    total_params = 0
    passed_params = 0
    
    for param, result in results.items():
        if result['status'] != 'UNKNOWN':
            total_params += 1
            if result['status'] == 'PASS':
                passed_params += 1
    
    return (passed_params / total_params * 100) if total_params > 0 else 0

def process_single_pdf(pdf_path: Path) -> Dict:
    """Process a single PDF file"""
    print(f"📄 Processing: {pdf_path.name}")
    
    try:
        # Extract text
        text = extract_text_from_pdf(pdf_path)
        if not text.strip():
            return {
                'file_name': pdf_path.name,
                'status': 'FAILED',
                'error': 'No text extracted',
                'compliance_score': 0,
                'parameters': {},
                'results': {}
            }
        
        # Extract parameters
        parameters = extract_lighting_parameters(text)
        
        # Evaluate parameters
        results = evaluate_parameters(parameters)
        
        # Calculate compliance score
        compliance_score = calculate_compliance_score(results)
        
        # Determine overall status
        if compliance_score >= 90:
            overall_status = 'EXCELLENT'
        elif compliance_score >= 75:
            overall_status = 'GOOD'
        elif compliance_score >= 60:
            overall_status = 'ACCEPTABLE'
        elif compliance_score >= 40:
            overall_status = 'POOR'
        else:
            overall_status = 'FAIL'
        
        return {
            'file_name': pdf_path.name,
            'status': 'SUCCESS',
            'overall_status': overall_status,
            'compliance_score': compliance_score,
            'parameters': parameters,
            'results': results,
            'text_length': len(text)
        }
        
    except Exception as e:
        return {
            'file_name': pdf_path.name,
            'status': 'FAILED',
            'error': str(e),
            'compliance_score': 0,
            'parameters': {},
            'results': {}
        }

def process_folder(folder_path: Path) -> List[Dict]:
    """Process all PDFs in a folder"""
    print(f"📁 Processing folder: {folder_path}")
    
    # Find all PDF files
    pdf_files = list(folder_path.glob("*.pdf"))
    if not pdf_files:
        print("❌ No PDF files found in folder")
        return []
    
    print(f"📄 Found {len(pdf_files)} PDF files")
    
    results = []
    for pdf_file in pdf_files:
        result = process_single_pdf(pdf_file)
        results.append(result)
        
        # Print summary for each file
        if result['status'] == 'SUCCESS':
            print(f"   ✅ {result['overall_status']} - {result['compliance_score']:.1f}% compliance")
        else:
            print(f"   ❌ FAILED - {result.get('error', 'Unknown error')}")
    
    return results

def generate_summary_report(results: List[Dict]) -> Dict:
    """Generate summary report"""
    total_files = len(results)
    successful_files = len([r for r in results if r['status'] == 'SUCCESS'])
    failed_files = total_files - successful_files
    
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
    
    return {
        'total_files': total_files,
        'successful_files': successful_files,
        'failed_files': failed_files,
        'average_compliance': avg_compliance,
        'status_breakdown': {
            'excellent': excellent,
            'good': good,
            'acceptable': acceptable,
            'poor': poor,
            'fail': fail
        }
    }

def main():
    """Main function"""
    print("🚀 Batch PDF Evaluator")
    print("=" * 40)
    print("Processes all PDFs in a folder and evaluates them against lighting standards")
    print()
    
    # Get folder path
    folder_path = input("Enter path to folder containing PDFs: ").strip()
    if not folder_path:
        print("❌ No folder path provided")
        return
    
    folder_path = Path(folder_path)
    if not folder_path.exists():
        print(f"❌ Folder not found: {folder_path}")
        return
    
    if not folder_path.is_dir():
        print(f"❌ Path is not a directory: {folder_path}")
        return
    
    # Process all PDFs
    results = process_folder(folder_path)
    
    if not results:
        print("❌ No results to report")
        return
    
    # Generate summary
    summary = generate_summary_report(results)
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 BATCH EVALUATION SUMMARY")
    print("=" * 50)
    print(f"Total PDFs: {summary['total_files']}")
    print(f"Successfully processed: {summary['successful_files']}")
    print(f"Failed to process: {summary['failed_files']}")
    
    if summary['successful_files'] > 0:
        print(f"Average compliance: {summary['average_compliance']:.1f}%")
        print()
        print("Status breakdown:")
        print(f"  🎉 Excellent: {summary['status_breakdown']['excellent']}")
        print(f"  ✅ Good: {summary['status_breakdown']['good']}")
        print(f"  ⚠️ Acceptable: {summary['status_breakdown']['acceptable']}")
        print(f"  ❌ Poor: {summary['status_breakdown']['poor']}")
        print(f"  💥 Fail: {summary['status_breakdown']['fail']}")
    
    # Save detailed results
    output_file = folder_path / f"batch_evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    report_data = {
        'evaluation_date': datetime.now().isoformat(),
        'folder_path': str(folder_path),
        'summary': summary,
        'detailed_results': results
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Detailed results saved to: {output_file}")
    
    # Show recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    if summary['average_compliance'] >= 90:
        print("🎉 Excellent overall compliance! Your lighting reports meet high standards.")
    elif summary['average_compliance'] >= 75:
        print("✅ Good overall compliance. Minor improvements could be made.")
    elif summary['average_compliance'] >= 60:
        print("⚠️ Acceptable compliance. Some improvements are needed.")
    else:
        print("❌ Poor compliance. Significant improvements are required.")
    
    print(f"\n📋 Check the detailed JSON report for specific recommendations for each file.")

if __name__ == "__main__":
    main()
