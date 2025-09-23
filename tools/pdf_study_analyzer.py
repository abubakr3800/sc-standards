"""
PDF Study Analyzer
Advanced system for analyzing lighting studies from PDFs with high accuracy
"""
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime
import fitz  # PyMuPDF
import pdfplumber
from pdfminer.high_level import extract_text
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFStudyAnalyzer:
    """Advanced PDF study analyzer for lighting reports"""
    
    def __init__(self):
        self.uploads_dir = Path("uploads")
        self.studies_dir = Path("studies")
        self.studies_dir.mkdir(exist_ok=True)
        
        # Enhanced extraction patterns
        self.patterns = self._initialize_patterns()
        
        # Standards reference data
        self.standards_data = self._load_standards_reference()
    
    def _initialize_patterns(self):
        """Initialize comprehensive extraction patterns"""
        return {
            'illuminance': {
                'patterns': [
                    # Standard illuminance patterns
                    r'illuminance[:\s]*(\d+(?:\.\d+)?)\s*lux',
                    r'(\d+(?:\.\d+)?)\s*lux\s*(?:illuminance|maintained|average|target)',
                    r'(?:maintained|average|target)\s*illuminance[:\s]*(\d+(?:\.\d+)?)\s*lux',
                    r'(\d+(?:\.\d+)?)\s*lx\s*(?:illuminance|maintained|average|target)',
                    
                    # Table patterns
                    r'(\d+(?:\.\d+)?)\s*lux\s*(?:to|-)\s*(\d+(?:\.\d+)?)\s*lux',
                    r'(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*lux',
                    r'(\d+(?:\.\d+)?)\s*to\s*(\d+(?:\.\d+)?)\s*lux',
                    
                    # Room-specific patterns
                    r'(?:office|work|desk|task)[:\s]*(\d+(?:\.\d+)?)\s*lux',
                    r'(?:conference|meeting|room)[:\s]*(\d+(?:\.\d+)?)\s*lux',
                    r'(?:corridor|hallway|passage)[:\s]*(\d+(?:\.\d+)?)\s*lux',
                    r'(?:reception|lobby|entrance)[:\s]*(\d+(?:\.\d+)?)\s*lux',
                    
                    # Minimum/maximum patterns
                    r'(?:minimum|min)[:\s]*(\d+(?:\.\d+)?)\s*lux',
                    r'(?:maximum|max)[:\s]*(\d+(?:\.\d+)?)\s*lux',
                    r'(?:average|avg)[:\s]*(\d+(?:\.\d+)?)\s*lux',
                    
                    # Uniformity patterns
                    r'uniformity[:\s]*(\d+(?:\.\d+)?)',
                    r'(\d+(?:\.\d+)?)\s*uniformity',
                    r'Uo[:\s]*(\d+(?:\.\d+)?)',
                    
                    # Power density patterns
                    r'(\d+(?:\.\d+)?)\s*W/m²',
                    r'(\d+(?:\.\d+)?)\s*W/m2',
                    r'power\s*density[:\s]*(\d+(?:\.\d+)?)\s*W/m²',
                    r'lighting\s*power\s*density[:\s]*(\d+(?:\.\d+)?)\s*W/m²'
                ],
                'context_keywords': ['illuminance', 'lux', 'lx', 'lighting', 'light', 'brightness']
            },
            
            'ugr': {
                'patterns': [
                    r'UGR[:\s]*(?:≤|<=|maximum|max|≤)\s*(\d+(?:\.\d+)?)',
                    r'(?:≤|<=|maximum|max|≤)\s*(\d+(?:\.\d+)?)\s*UGR',
                    r'glare[:\s]*(?:≤|<=|maximum|max|≤)\s*(\d+(?:\.\d+)?)',
                    r'UGR[:\s]*(\d+(?:\.\d+)?)',
                    r'glare\s*rating[:\s]*(\d+(?:\.\d+)?)',
                    r'unified\s*glare[:\s]*(\d+(?:\.\d+)?)',
                    r'(\d+(?:\.\d+)?)\s*UGR'
                ],
                'context_keywords': ['UGR', 'glare', 'unified glare rating', 'glare control']
            },
            
            'cri': {
                'patterns': [
                    r'CRI[:\s]*(?:≥|>=|minimum|min|≥)\s*(\d+(?:\.\d+)?)',
                    r'(?:≥|>=|minimum|min|≥)\s*(\d+(?:\.\d+)?)\s*CRI',
                    r'color\s*rendering[:\s]*(?:≥|>=|minimum|min|≥)\s*(\d+(?:\.\d+)?)',
                    r'CRI[:\s]*(\d+(?:\.\d+)?)',
                    r'color\s*rendering\s*index[:\s]*(\d+(?:\.\d+)?)',
                    r'Ra[:\s]*(?:≥|>=|minimum|min|≥)\s*(\d+(?:\.\d+)?)',
                    r'(?:≥|>=|minimum|min|≥)\s*(\d+(?:\.\d+)?)\s*Ra'
                ],
                'context_keywords': ['CRI', 'color rendering', 'Ra', 'color quality']
            },
            
            'rooms': {
                'patterns': [
                    r'(?:room|space|area)[:\s]*([A-Za-z\s]+?)(?:\s*\d+|\s*lux|\s*UGR|\s*CRI)',
                    r'([A-Za-z\s]+?)\s*(?:office|room|space|area|zone)',
                    r'(?:office|conference|meeting|corridor|reception|lobby|staircase|break|kitchen|toilet|storage)',
                    r'([A-Za-z\s]+?)\s*(?:\d+\s*lux|\d+\s*UGR|\d+\s*CRI)'
                ],
                'context_keywords': ['room', 'space', 'area', 'zone', 'office', 'conference', 'meeting']
            },
            
            'luminaire_data': {
                'patterns': [
                    r'(\d+(?:\.\d+)?)\s*W\s*(?:per|/)\s*(?:luminaire|fitting|fixture)',
                    r'(\d+(?:\.\d+)?)\s*W\s*(?:per|/)\s*(?:m²|m2)',
                    r'(\d+(?:\.\d+)?)\s*lumens\s*(?:per|/)\s*(?:W|watt)',
                    r'efficacy[:\s]*(\d+(?:\.\d+)?)\s*(?:lm/W|lumens/watt)',
                    r'(\d+(?:\.\d+)?)\s*K\s*(?:color|temperature|CCT)',
                    r'color\s*temperature[:\s]*(\d+(?:\.\d+)?)\s*K'
                ],
                'context_keywords': ['luminaire', 'fitting', 'fixture', 'watt', 'efficacy', 'color temperature']
            }
        }
    
    def _load_standards_reference(self):
        """Load standards reference data for comparison"""
        try:
            # Load enhanced standards data if available
            enhanced_file = self.uploads_dir / "enhanced_standards_data.json"
            if enhanced_file.exists():
                with open(enhanced_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            # Fallback to basic standards
            return {
                "en12464_2021": {
                    "applications": {
                        "office_general": {
                            "illuminance": {"maintained": 500, "minimum": 300, "maximum": 1000},
                            "ugr": {"maximum": 19, "recommended": 16},
                            "cri": {"minimum": 80, "recommended": 90},
                            "uniformity": {"minimum": 0.6, "recommended": 0.8},
                            "power_density": {"maximum": 3.5, "recommended": 2.5}
                        }
                    }
                }
            }
        except Exception as e:
            logger.error(f"Could not load standards reference: {e}")
            return {}
    
    def analyze_pdf_study(self, pdf_path: Path) -> Dict:
        """Analyze a PDF lighting study with high accuracy"""
        logger.info(f"Analyzing PDF study: {pdf_path.name}")
        
        # Extract text using multiple methods
        text_content = self._extract_text_comprehensive(pdf_path)
        
        # Extract structured data
        extracted_data = self._extract_structured_data(text_content)
        
        # Extract room-specific data
        room_data = self._extract_room_data(text_content)
        
        # Extract luminaire data
        luminaire_data = self._extract_luminaire_data(text_content)
        
        # Analyze compliance
        compliance_analysis = self._analyze_compliance(extracted_data, room_data)
        
        # Generate summary
        summary = self._generate_study_summary(extracted_data, room_data, compliance_analysis)
        
        # Save analysis results
        analysis_result = {
            "file_name": pdf_path.name,
            "analysis_date": datetime.now().isoformat(),
            "extracted_data": extracted_data,
            "room_data": room_data,
            "luminaire_data": luminaire_data,
            "compliance_analysis": compliance_analysis,
            "summary": summary,
            "text_content": text_content[:5000]  # First 5000 chars for reference
        }
        
        # Save to studies directory
        output_file = self.studies_dir / f"{pdf_path.stem}_analysis.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_result, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Analysis saved to: {output_file}")
        return analysis_result
    
    def _extract_text_comprehensive(self, pdf_path: Path) -> str:
        """Extract text using multiple methods for better accuracy"""
        text_content = ""
        
        try:
            # Method 1: PyMuPDF (best for most PDFs)
            doc = fitz.open(pdf_path)
            for page in doc:
                text_content += page.get_text() + "\n"
            doc.close()
            
            # Method 2: pdfplumber (better for tables)
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text_content += page.extract_text() or ""
            
            # Method 3: pdfminer (fallback)
            if len(text_content) < 100:
                text_content = extract_text(pdf_path)
                
        except Exception as e:
            logger.error(f"Error extracting text: {e}")
        
        return text_content
    
    def _extract_structured_data(self, text: str) -> Dict:
        """Extract structured lighting data from text"""
        extracted = {
            'illuminance': [],
            'ugr': [],
            'cri': [],
            'uniformity': [],
            'power_density': []
        }
        
        for param_type, config in self.patterns.items():
            if param_type in extracted:
                for pattern in config['patterns']:
                    matches = re.finditer(pattern, text, re.IGNORECASE)
                    for match in matches:
                        groups = match.groups()
                        if groups:
                            value = float(groups[0]) if '.' in groups[0] else int(groups[0])
                            extracted[param_type].append({
                                'value': value,
                                'context': self._extract_context(text, match.start(), match.end()),
                                'pattern': pattern,
                                'confidence': self._calculate_extraction_confidence(match, config['context_keywords'])
                            })
        
        return extracted
    
    def _extract_room_data(self, text: str) -> List[Dict]:
        """Extract room-specific lighting data"""
        rooms = []
        
        # Look for room sections
        room_sections = re.finditer(r'(?:room|space|area)[:\s]*([A-Za-z\s]+?)(?:\n|$)', text, re.IGNORECASE)
        
        for section in room_sections:
            room_name = section.group(1).strip()
            if len(room_name) > 2:  # Filter out very short matches
                # Extract data for this room
                room_data = {
                    'name': room_name,
                    'illuminance': self._extract_room_parameter(text, room_name, 'illuminance'),
                    'ugr': self._extract_room_parameter(text, room_name, 'ugr'),
                    'cri': self._extract_room_parameter(text, room_name, 'cri'),
                    'uniformity': self._extract_room_parameter(text, room_name, 'uniformity')
                }
                rooms.append(room_data)
        
        return rooms
    
    def _extract_room_parameter(self, text: str, room_name: str, parameter: str) -> Optional[Dict]:
        """Extract specific parameter for a room"""
        # Look for parameter near room name
        room_context = self._find_room_context(text, room_name)
        if room_context:
            patterns = self.patterns.get(parameter, {}).get('patterns', [])
            for pattern in patterns:
                matches = re.finditer(pattern, room_context, re.IGNORECASE)
                for match in matches:
                    groups = match.groups()
                    if groups:
                        value = float(groups[0]) if '.' in groups[0] else int(groups[0])
                        return {
                            'value': value,
                            'context': room_context,
                            'confidence': 0.8
                        }
        return None
    
    def _find_room_context(self, text: str, room_name: str, context_length: int = 500) -> Optional[str]:
        """Find context around room name"""
        try:
            index = text.lower().find(room_name.lower())
            if index != -1:
                start = max(0, index - context_length)
                end = min(len(text), index + len(room_name) + context_length)
                return text[start:end]
        except:
            pass
        return None
    
    def _extract_luminaire_data(self, text: str) -> List[Dict]:
        """Extract luminaire specifications"""
        luminaires = []
        
        patterns = self.patterns['luminaire_data']['patterns']
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                groups = match.groups()
                if groups:
                    value = float(groups[0]) if '.' in groups[0] else int(groups[0])
                    luminaires.append({
                        'value': value,
                        'parameter': self._identify_luminaire_parameter(pattern),
                        'context': self._extract_context(text, match.start(), match.end()),
                        'confidence': 0.7
                    })
        
        return luminaires
    
    def _identify_luminaire_parameter(self, pattern: str) -> str:
        """Identify what parameter the pattern extracts"""
        if 'watt' in pattern.lower() or 'W' in pattern:
            return 'power'
        elif 'lumen' in pattern.lower() or 'lm' in pattern:
            return 'luminous_flux'
        elif 'efficacy' in pattern.lower():
            return 'efficacy'
        elif 'K' in pattern or 'temperature' in pattern.lower():
            return 'color_temperature'
        else:
            return 'unknown'
    
    def _analyze_compliance(self, extracted_data: Dict, room_data: List[Dict]) -> Dict:
        """Analyze compliance with standards"""
        compliance = {
            'overall_compliance': 'unknown',
            'room_compliance': [],
            'parameter_compliance': {},
            'recommendations': []
        }
        
        # Analyze each room
        for room in room_data:
            room_compliance = self._analyze_room_compliance(room)
            compliance['room_compliance'].append(room_compliance)
        
        # Analyze overall parameters
        for param_type, values in extracted_data.items():
            if values:
                compliance['parameter_compliance'][param_type] = self._analyze_parameter_compliance(param_type, values)
        
        # Generate overall compliance
        compliance['overall_compliance'] = self._calculate_overall_compliance(compliance)
        
        return compliance
    
    def _analyze_room_compliance(self, room: Dict) -> Dict:
        """Analyze compliance for a specific room"""
        room_name = room['name']
        compliance = {
            'room_name': room_name,
            'status': 'unknown',
            'issues': [],
            'recommendations': []
        }
        
        # Check illuminance
        if room.get('illuminance'):
            illuminance = room['illuminance']['value']
            if illuminance < 300:
                compliance['issues'].append(f"Illuminance too low: {illuminance} lux (minimum 300 lux)")
            elif illuminance > 1000:
                compliance['issues'].append(f"Illuminance too high: {illuminance} lux (maximum 1000 lux)")
            else:
                compliance['recommendations'].append(f"Good illuminance: {illuminance} lux")
        
        # Check UGR
        if room.get('ugr'):
            ugr = room['ugr']['value']
            if ugr > 19:
                compliance['issues'].append(f"UGR too high: {ugr} (maximum 19)")
            else:
                compliance['recommendations'].append(f"Good UGR: {ugr}")
        
        # Check CRI
        if room.get('cri'):
            cri = room['cri']['value']
            if cri < 80:
                compliance['issues'].append(f"CRI too low: {cri} (minimum 80)")
            else:
                compliance['recommendations'].append(f"Good CRI: {cri}")
        
        # Determine status
        if compliance['issues']:
            compliance['status'] = 'non_compliant'
        elif compliance['recommendations']:
            compliance['status'] = 'compliant'
        else:
            compliance['status'] = 'unknown'
        
        return compliance
    
    def _analyze_parameter_compliance(self, param_type: str, values: List[Dict]) -> Dict:
        """Analyze compliance for a specific parameter"""
        if not values:
            return {'status': 'no_data', 'confidence': 0.0}
        
        # Get standards reference
        standards_ref = self.standards_data.get('en12464_2021', {}).get('applications', {}).get('office_general', {})
        
        if param_type == 'illuminance':
            min_required = standards_ref.get('illuminance', {}).get('minimum', 300)
            max_required = standards_ref.get('illuminance', {}).get('maximum', 1000)
            
            compliant_values = [v for v in values if min_required <= v['value'] <= max_required]
            compliance_rate = len(compliant_values) / len(values) if values else 0
            
            return {
                'status': 'compliant' if compliance_rate > 0.8 else 'non_compliant',
                'compliance_rate': compliance_rate,
                'values_analyzed': len(values),
                'compliant_values': len(compliant_values)
            }
        
        return {'status': 'analyzed', 'confidence': 0.5}
    
    def _calculate_overall_compliance(self, compliance: Dict) -> str:
        """Calculate overall compliance status"""
        room_statuses = [room['status'] for room in compliance['room_compliance']]
        param_statuses = [param['status'] for param in compliance['parameter_compliance'].values()]
        
        all_statuses = room_statuses + param_statuses
        
        if not all_statuses:
            return 'no_data'
        
        compliant_count = all_statuses.count('compliant')
        non_compliant_count = all_statuses.count('non_compliant')
        
        if non_compliant_count > compliant_count:
            return 'non_compliant'
        elif compliant_count > non_compliant_count:
            return 'compliant'
        else:
            return 'mixed'
    
    def _generate_study_summary(self, extracted_data: Dict, room_data: List[Dict], compliance_analysis: Dict) -> Dict:
        """Generate comprehensive study summary"""
        summary = {
            'total_rooms_analyzed': len(room_data),
            'parameters_found': {k: len(v) for k, v in extracted_data.items() if v},
            'overall_compliance': compliance_analysis['overall_compliance'],
            'key_findings': [],
            'recommendations': []
        }
        
        # Generate key findings
        if extracted_data['illuminance']:
            avg_illuminance = np.mean([v['value'] for v in extracted_data['illuminance']])
            summary['key_findings'].append(f"Average illuminance: {avg_illuminance:.1f} lux")
        
        if extracted_data['ugr']:
            max_ugr = max([v['value'] for v in extracted_data['ugr']])
            summary['key_findings'].append(f"Maximum UGR: {max_ugr}")
        
        if extracted_data['cri']:
            min_cri = min([v['value'] for v in extracted_data['cri']])
            summary['key_findings'].append(f"Minimum CRI: {min_cri}")
        
        # Generate recommendations
        if compliance_analysis['overall_compliance'] == 'non_compliant':
            summary['recommendations'].append("Review lighting design for compliance issues")
        
        if room_data:
            summary['recommendations'].append(f"Analyzed {len(room_data)} rooms for lighting compliance")
        
        return summary
    
    def _extract_context(self, text: str, start: int, end: int, context_length: int = 200) -> str:
        """Extract context around a match"""
        try:
            context_start = max(0, start - context_length)
            context_end = min(len(text), end + context_length)
            return text[context_start:context_end].strip()
        except:
            return ""
    
    def _calculate_extraction_confidence(self, match, context_keywords: List[str]) -> float:
        """Calculate confidence in extraction based on context"""
        base_confidence = 0.5
        
        # Increase confidence if context keywords are nearby
        context = self._extract_context(match.string, match.start(), match.end())
        context_lower = context.lower()
        
        for keyword in context_keywords:
            if keyword.lower() in context_lower:
                base_confidence += 0.1
        
        return min(base_confidence, 0.95)

def main():
    """Main function for testing"""
    analyzer = PDFStudyAnalyzer()
    
    # Test with existing PDFs
    base_dir = Path("base")
    if base_dir.exists():
        pdf_files = list(base_dir.glob("*.pdf"))
        if pdf_files:
            print(f"Found {len(pdf_files)} PDF files to analyze")
            for pdf_file in pdf_files:
                print(f"\nAnalyzing: {pdf_file.name}")
                try:
                    result = analyzer.analyze_pdf_study(pdf_file)
                    print(f"✅ Analysis completed for {pdf_file.name}")
                    print(f"   Rooms analyzed: {result['summary']['total_rooms_analyzed']}")
                    print(f"   Overall compliance: {result['summary']['overall_compliance']}")
                except Exception as e:
                    print(f"❌ Error analyzing {pdf_file.name}: {e}")
        else:
            print("No PDF files found in base/ directory")
    else:
        print("base/ directory not found")

if __name__ == "__main__":
    main()
