"""
Realistic Lighting Evaluator
More accurate evaluation criteria based on real-world lighting studies
"""
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import re

def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract text from PDF using multiple methods"""
    text = ""
    
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"pdfplumber failed: {e}")
    
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
            print(f"PyMuPDF failed: {e}")
    
    return text

def extract_lighting_parameters(text: str) -> Dict:
    """Extract lighting parameters from text with better patterns"""
    import re
    
    parameters = {
        'illuminance': [],
        'ugr': [],
        'area': [],
        'power_density': [],
        'uniformity': [],
        'cri': [],
        'color_temperature': []
    }
    
    # More comprehensive patterns for illuminance
    illuminance_patterns = [
        r'(\d+(?:\.\d+)?)\s*lux',
        r'illuminance[:\s]*(\d+(?:\.\d+)?)',
        r'illumination[:\s]*(\d+(?:\.\d+)?)',
        r'avg[:\s]*(\d+(?:\.\d+)?)',
        r'average[:\s]*(\d+(?:\.\d+)?)',
        r'mean[:\s]*(\d+(?:\.\d+)?)',
        r'(\d+(?:\.\d+)?)\s*lx'
    ]
    
    for pattern in illuminance_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        parameters['illuminance'].extend([float(x) for x in matches])
    
    # Remove duplicates and sort
    parameters['illuminance'] = sorted(list(set(parameters['illuminance'])))
    
    # UGR patterns
    ugr_patterns = [
        r'UGR[:\s]*(\d+(?:\.\d+)?)',
        r'ugr[:\s]*(\d+(?:\.\d+)?)',
        r'glare[:\s]*(\d+(?:\.\d+)?)',
        r'unified\s+glare[:\s]*(\d+(?:\.\d+)?)'
    ]
    
    for pattern in ugr_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        parameters['ugr'].extend([float(x) for x in matches])
    
    parameters['ugr'] = sorted(list(set(parameters['ugr'])))
    
    # Area patterns
    area_patterns = [
        r'(\d+(?:\.\d+)?)\s*m²',
        r'(\d+(?:\.\d+)?)\s*m2',
        r'area[:\s]*(\d+(?:\.\d+)?)',
        r'size[:\s]*(\d+(?:\.\d+)?)'
    ]
    
    for pattern in area_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        parameters['area'].extend([float(x) for x in matches])
    
    parameters['area'] = sorted(list(set(parameters['area'])))
    
    # Power density patterns
    power_patterns = [
        r'(\d+(?:\.\d+)?)\s*W/m²',
        r'(\d+(?:\.\d+)?)\s*W/m2',
        r'LPD[:\s]*(\d+(?:\.\d+)?)',
        r'power\s+density[:\s]*(\d+(?:\.\d+)?)',
        r'lighting\s+power[:\s]*(\d+(?:\.\d+)?)'
    ]
    
    for pattern in power_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        parameters['power_density'].extend([float(x) for x in matches])
    
    parameters['power_density'] = sorted(list(set(parameters['power_density'])))
    
    # Uniformity patterns
    uniformity_patterns = [
        r'uniformity[:\s]*(\d+(?:\.\d+)?)',
        r'uniform[:\s]*(\d+(?:\.\d+)?)',
        r'U[o0][:\s]*(\d+(?:\.\d+)?)',
        r'min/max[:\s]*(\d+(?:\.\d+)?)'
    ]
    
    for pattern in uniformity_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        parameters['uniformity'].extend([float(x) for x in matches])
    
    parameters['uniformity'] = sorted(list(set(parameters['uniformity'])))
    
    # CRI patterns
    cri_patterns = [
        r'CRI[:\s]*(\d+(?:\.\d+)?)',
        r'color\s+rendering[:\s]*(\d+(?:\.\d+)?)',
        r'Ra[:\s]*(\d+(?:\.\d+)?)'
    ]
    
    for pattern in cri_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        parameters['cri'].extend([float(x) for x in matches])
    
    parameters['cri'] = sorted(list(set(parameters['cri'])))
    
    # Color temperature patterns
    cct_patterns = [
        r'(\d+(?:\.\d+)?)\s*K',
        r'CCT[:\s]*(\d+(?:\.\d+)?)',
        r'color\s+temperature[:\s]*(\d+(?:\.\d+)?)'
    ]
    
    for pattern in cct_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        parameters['color_temperature'].extend([float(x) for x in matches])
    
    parameters['color_temperature'] = sorted(list(set(parameters['color_temperature'])))
    
    return parameters

def evaluate_parameters_realistic(parameters: Dict) -> Dict:
    """Evaluate parameters with realistic criteria"""
    results = {
        'illuminance': {'status': 'UNKNOWN', 'recommendation': '', 'score': 0},
        'ugr': {'status': 'UNKNOWN', 'recommendation': '', 'score': 0},
        'power_density': {'status': 'UNKNOWN', 'recommendation': '', 'score': 0},
        'uniformity': {'status': 'UNKNOWN', 'recommendation': '', 'score': 0},
        'cri': {'status': 'UNKNOWN', 'recommendation': '', 'score': 0},
        'color_temperature': {'status': 'UNKNOWN', 'recommendation': '', 'score': 0}
    }
    
    # Evaluate illuminance with realistic criteria
    if parameters['illuminance']:
        # Filter out unrealistic values (too high or too low)
        realistic_illuminance = [x for x in parameters['illuminance'] if 10 <= x <= 5000]
        
        if realistic_illuminance:
            avg_illuminance = sum(realistic_illuminance) / len(realistic_illuminance)
            
            # More realistic criteria based on actual lighting studies
            if 200 <= avg_illuminance <= 800:  # Good range for most applications
                if 300 <= avg_illuminance <= 600:  # Optimal range
                    results['illuminance'] = {
                        'status': 'EXCELLENT',
                        'recommendation': f'Excellent illuminance: {avg_illuminance:.0f} lux - Perfect for most applications',
                        'score': 100
                    }
                else:
                    results['illuminance'] = {
                        'status': 'GOOD',
                        'recommendation': f'Good illuminance: {avg_illuminance:.0f} lux - Suitable for most tasks',
                        'score': 85
                    }
            elif 100 <= avg_illuminance < 200:  # Acceptable for some applications
                results['illuminance'] = {
                    'status': 'ACCEPTABLE',
                    'recommendation': f'Acceptable illuminance: {avg_illuminance:.0f} lux - Suitable for general areas',
                    'score': 70
                }
            elif avg_illuminance > 800:  # High but not necessarily bad
                results['illuminance'] = {
                    'status': 'GOOD',
                    'recommendation': f'High illuminance: {avg_illuminance:.0f} lux - Good for detailed work',
                    'score': 80
                }
            else:  # Too low
                results['illuminance'] = {
                    'status': 'POOR',
                    'recommendation': f'Low illuminance: {avg_illuminance:.0f} lux - Consider increasing for better visibility',
                    'score': 40
                }
    
    # Evaluate UGR with realistic criteria
    if parameters['ugr']:
        # Filter realistic UGR values
        realistic_ugr = [x for x in parameters['ugr'] if 0 <= x <= 30]
        
        if realistic_ugr:
            max_ugr = max(realistic_ugr)
            
            if max_ugr <= 13:  # Excellent
                results['ugr'] = {
                    'status': 'EXCELLENT',
                    'recommendation': f'Excellent glare control: UGR {max_ugr:.1f} - Very comfortable',
                    'score': 100
                }
            elif max_ugr <= 16:  # Good
                results['ugr'] = {
                    'status': 'GOOD',
                    'recommendation': f'Good glare control: UGR {max_ugr:.1f} - Comfortable for most users',
                    'score': 90
                }
            elif max_ugr <= 19:  # Acceptable
                results['ugr'] = {
                    'status': 'ACCEPTABLE',
                    'recommendation': f'Acceptable glare control: UGR {max_ugr:.1f} - Generally acceptable',
                    'score': 75
                }
            elif max_ugr <= 22:  # Poor but not terrible
                results['ugr'] = {
                    'status': 'POOR',
                    'recommendation': f'Moderate glare: UGR {max_ugr:.1f} - Consider improving glare control',
                    'score': 60
                }
            else:  # Too high
                results['ugr'] = {
                    'status': 'POOR',
                    'recommendation': f'High glare: UGR {max_ugr:.1f} - Needs improvement',
                    'score': 30
                }
    
    # Evaluate power density with realistic criteria
    if parameters['power_density']:
        # Filter realistic power density values
        realistic_power = [x for x in parameters['power_density'] if 0.5 <= x <= 10]
        
        if realistic_power:
            avg_power = sum(realistic_power) / len(realistic_power)
            
            if avg_power <= 2.0:  # Excellent efficiency
                results['power_density'] = {
                    'status': 'EXCELLENT',
                    'recommendation': f'Excellent energy efficiency: {avg_power:.2f} W/m² - Very efficient',
                    'score': 100
                }
            elif avg_power <= 3.0:  # Good efficiency
                results['power_density'] = {
                    'status': 'GOOD',
                    'recommendation': f'Good energy efficiency: {avg_power:.2f} W/m² - Efficient design',
                    'score': 85
                }
            elif avg_power <= 4.0:  # Acceptable
                results['power_density'] = {
                    'status': 'ACCEPTABLE',
                    'recommendation': f'Acceptable energy efficiency: {avg_power:.2f} W/m² - Within reasonable limits',
                    'score': 70
                }
            elif avg_power <= 5.0:  # Poor but not terrible
                results['power_density'] = {
                    'status': 'POOR',
                    'recommendation': f'Moderate energy efficiency: {avg_power:.2f} W/m² - Consider more efficient lighting',
                    'score': 50
                }
            else:  # Too high
                results['power_density'] = {
                    'status': 'POOR',
                    'recommendation': f'High energy consumption: {avg_power:.2f} W/m² - Needs efficiency improvements',
                    'score': 30
                }
    
    # Evaluate uniformity with realistic criteria
    if parameters['uniformity']:
        # Filter realistic uniformity values
        realistic_uniformity = [x for x in parameters['uniformity'] if 0.1 <= x <= 1.0]
        
        if realistic_uniformity:
            avg_uniformity = sum(realistic_uniformity) / len(realistic_uniformity)
            
            if avg_uniformity >= 0.8:  # Excellent
                results['uniformity'] = {
                    'status': 'EXCELLENT',
                    'recommendation': f'Excellent uniformity: {avg_uniformity:.2f} - Very even lighting',
                    'score': 100
                }
            elif avg_uniformity >= 0.6:  # Good
                results['uniformity'] = {
                    'status': 'GOOD',
                    'recommendation': f'Good uniformity: {avg_uniformity:.2f} - Generally even lighting',
                    'score': 85
                }
            elif avg_uniformity >= 0.4:  # Acceptable
                results['uniformity'] = {
                    'status': 'ACCEPTABLE',
                    'recommendation': f'Acceptable uniformity: {avg_uniformity:.2f} - Adequate lighting distribution',
                    'score': 70
                }
            else:  # Poor
                results['uniformity'] = {
                    'status': 'POOR',
                    'recommendation': f'Poor uniformity: {avg_uniformity:.2f} - Uneven lighting distribution',
                    'score': 40
                }
    
    # Evaluate CRI with realistic criteria
    if parameters['cri']:
        # Filter realistic CRI values
        realistic_cri = [x for x in parameters['cri'] if 50 <= x <= 100]
        
        if realistic_cri:
            min_cri = min(realistic_cri)
            
            if min_cri >= 90:  # Excellent
                results['cri'] = {
                    'status': 'EXCELLENT',
                    'recommendation': f'Excellent color rendering: CRI {min_cri:.0f} - Excellent color quality',
                    'score': 100
                }
            elif min_cri >= 80:  # Good
                results['cri'] = {
                    'status': 'GOOD',
                    'recommendation': f'Good color rendering: CRI {min_cri:.0f} - Good color quality',
                    'score': 85
                }
            elif min_cri >= 70:  # Acceptable
                results['cri'] = {
                    'status': 'ACCEPTABLE',
                    'recommendation': f'Acceptable color rendering: CRI {min_cri:.0f} - Adequate color quality',
                    'score': 70
                }
            else:  # Poor
                results['cri'] = {
                    'status': 'POOR',
                    'recommendation': f'Poor color rendering: CRI {min_cri:.0f} - Consider higher CRI lighting',
                    'score': 40
                }
    
    # Evaluate color temperature with realistic criteria
    if parameters['color_temperature']:
        # Filter realistic CCT values
        realistic_cct = [x for x in parameters['color_temperature'] if 2000 <= x <= 8000]
        
        if realistic_cct:
            avg_cct = sum(realistic_cct) / len(realistic_cct)
            
            if 3000 <= avg_cct <= 4000:  # Excellent for most applications
                results['color_temperature'] = {
                    'status': 'EXCELLENT',
                    'recommendation': f'Excellent color temperature: {avg_cct:.0f}K - Perfect for most applications',
                    'score': 100
                }
            elif 2700 <= avg_cct <= 5000:  # Good range
                results['color_temperature'] = {
                    'status': 'GOOD',
                    'recommendation': f'Good color temperature: {avg_cct:.0f}K - Suitable for most applications',
                    'score': 85
                }
            elif 2000 <= avg_cct <= 6500:  # Acceptable range
                results['color_temperature'] = {
                    'status': 'ACCEPTABLE',
                    'recommendation': f'Acceptable color temperature: {avg_cct:.0f}K - Generally acceptable',
                    'score': 70
                }
            else:  # Outside normal range
                results['color_temperature'] = {
                    'status': 'POOR',
                    'recommendation': f'Unusual color temperature: {avg_cct:.0f}K - Consider standard range (2700-5000K)',
                    'score': 50
                }
    
    return results

def calculate_realistic_compliance_score(results: Dict) -> float:
    """Calculate realistic compliance score"""
    total_params = 0
    total_score = 0
    
    for param, result in results.items():
        if result['status'] != 'UNKNOWN':
            total_params += 1
            total_score += result['score']
    
    return (total_score / total_params) if total_params > 0 else 0

def process_single_pdf_realistic(pdf_path: Path) -> Dict:
    """Process a single PDF with realistic evaluation"""
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
        
        # Evaluate parameters with realistic criteria
        results = evaluate_parameters_realistic(parameters)
        
        # Calculate compliance score
        compliance_score = calculate_realistic_compliance_score(results)
        
        # Determine overall status
        if compliance_score >= 90:
            overall_status = 'EXCELLENT'
        elif compliance_score >= 80:
            overall_status = 'GOOD'
        elif compliance_score >= 70:
            overall_status = 'ACCEPTABLE'
        elif compliance_score >= 60:
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

def process_folder_realistic(folder_path: Path) -> List[Dict]:
    """Process all PDFs in a folder with realistic evaluation"""
    print(f"📁 Processing folder: {folder_path}")
    
    # Find all PDF files
    pdf_files = list(folder_path.glob("*.pdf"))
    if not pdf_files:
        print("❌ No PDF files found in folder")
        return []
    
    print(f"📄 Found {len(pdf_files)} PDF files")
    
    results = []
    for pdf_file in pdf_files:
        result = process_single_pdf_realistic(pdf_file)
        results.append(result)
        
        # Print summary for each file
        if result['status'] == 'SUCCESS':
            print(f"   ✅ {result['overall_status']} - {result['compliance_score']:.1f}% compliance")
        else:
            print(f"   ❌ FAILED - {result.get('error', 'Unknown error')}")
    
    return results

def main():
    """Main function"""
    print("🚀 Realistic Lighting Evaluator")
    print("=" * 40)
    print("More accurate evaluation criteria for real-world lighting studies")
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
    results = process_folder_realistic(folder_path)
    
    if not results:
        print("❌ No results to report")
        return
    
    # Calculate summary
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
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 REALISTIC EVALUATION SUMMARY")
    print("=" * 50)
    print(f"Total PDFs: {total_files}")
    print(f"Successfully processed: {successful_files}")
    print(f"Failed to process: {failed_files}")
    
    if successful_files > 0:
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
    
    # Save results
    output_file = folder_path / f"realistic_evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    report_data = {
        'evaluation_date': datetime.now().isoformat(),
        'folder_path': str(folder_path),
        'evaluation_type': 'realistic',
        'summary': {
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
        },
        'detailed_results': results
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Detailed results saved to: {output_file}")

if __name__ == "__main__":
    main()
