"""
Improve Standards Data Extraction
Extracts more accurate data from standards documents
"""
import json
import re
from pathlib import Path
from typing import Dict, List, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StandardsDataImprover:
    """Improves extraction of lighting parameters from standards"""
    
    def __init__(self):
        self.uploads_dir = Path("uploads")
        self.improved_data = {}
    
    def improve_extraction(self):
        """Improve data extraction from all processed standards"""
        logger.info("Starting improved standards data extraction...")
        
        processed_files = list(self.uploads_dir.glob("*_processed.json"))
        logger.info(f"Found {len(processed_files)} processed files")
        
        for file_path in processed_files:
            logger.info(f"Processing: {file_path.name}")
            improved_data = self._improve_single_file(file_path)
            self.improved_data[file_path.stem] = improved_data
        
        # Save improved data
        self._save_improved_data()
        logger.info("Improved extraction completed!")
    
    def _improve_single_file(self, file_path: Path) -> Dict:
        """Improve extraction for a single file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        text_content = data.get('text_content', '')
        
        # Extract lighting parameters with improved patterns
        extracted_params = {
            'illuminance': self._extract_illuminance_values(text_content),
            'ugr': self._extract_ugr_values(text_content),
            'cri': self._extract_cri_values(text_content),
            'power_density': self._extract_power_density_values(text_content),
            'uniformity': self._extract_uniformity_values(text_content),
            'applications': self._extract_applications(text_content),
            'tables': self._extract_structured_tables(text_content)
        }
        
        return {
            'original_data': data,
            'extracted_parameters': extracted_params,
            'improvement_notes': self._generate_improvement_notes(extracted_params)
        }
    
    def _extract_illuminance_values(self, text: str) -> List[Dict]:
        """Extract illuminance values with improved patterns"""
        illuminance_data = []
        
        # More comprehensive patterns
        patterns = [
            # Standard patterns
            r'(\d+)\s*lux\s*(?:minimum|min|≥|>=)',
            r'(?:minimum|min|≥|>=)\s*(\d+)\s*lux',
            r'illuminance[:\s]*(\d+)\s*lux',
            r'(\d+)\s*lx\s*(?:minimum|min|≥|>=)',
            r'(?:minimum|min|≥|>=)\s*(\d+)\s*lx',
            
            # Table patterns
            r'(\d+)\s*lux\s*(?:to|-)\s*(\d+)\s*lux',
            r'(\d+)\s*-\s*(\d+)\s*lux',
            r'(\d+)\s*to\s*(\d+)\s*lux',
            
            # Application-specific patterns
            r'office[:\s]*(\d+)\s*lux',
            r'conference[:\s]*(\d+)\s*lux',
            r'corridor[:\s]*(\d+)\s*lux',
            r'reception[:\s]*(\d+)\s*lux',
            r'staircase[:\s]*(\d+)\s*lux',
            
            # Range patterns
            r'(\d+)\s*lux\s*(?:to|-)\s*(\d+)\s*lux',
            r'(\d+)\s*-\s*(\d+)\s*lux',
            r'(\d+)\s*to\s*(\d+)\s*lux'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                groups = match.groups()
                if len(groups) == 1:
                    value = int(groups[0])
                    illuminance_data.append({
                        'value': value,
                        'type': 'single',
                        'context': self._extract_context(text, match.start(), match.end()),
                        'pattern': pattern
                    })
                elif len(groups) == 2:
                    min_val = int(groups[0])
                    max_val = int(groups[1])
                    illuminance_data.append({
                        'min_value': min_val,
                        'max_value': max_val,
                        'type': 'range',
                        'context': self._extract_context(text, match.start(), match.end()),
                        'pattern': pattern
                    })
        
        return illuminance_data
    
    def _extract_ugr_values(self, text: str) -> List[Dict]:
        """Extract UGR values with improved patterns"""
        ugr_data = []
        
        patterns = [
            r'UGR[:\s]*(?:≤|<=|maximum|max)\s*(\d+)',
            r'(?:≤|<=|maximum|max)\s*(\d+)\s*UGR',
            r'glare[:\s]*(?:≤|<=|maximum|max)\s*(\d+)',
            r'UGR[:\s]*(\d+)',
            r'glare rating[:\s]*(\d+)',
            r'unified glare[:\s]*(\d+)'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                value = int(match.groups()[0])
                ugr_data.append({
                    'value': value,
                    'context': self._extract_context(text, match.start(), match.end()),
                    'pattern': pattern
                })
        
        return ugr_data
    
    def _extract_cri_values(self, text: str) -> List[Dict]:
        """Extract CRI values with improved patterns"""
        cri_data = []
        
        patterns = [
            r'CRI[:\s]*(?:≥|>=|minimum|min)\s*(\d+)',
            r'(?:≥|>=|minimum|min)\s*(\d+)\s*CRI',
            r'color rendering[:\s]*(?:≥|>=|minimum|min)\s*(\d+)',
            r'CRI[:\s]*(\d+)',
            r'color rendering index[:\s]*(\d+)',
            r'Ra[:\s]*(?:≥|>=|minimum|min)\s*(\d+)',
            r'(?:≥|>=|minimum|min)\s*(\d+)\s*Ra'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                value = int(match.groups()[0])
                cri_data.append({
                    'value': value,
                    'context': self._extract_context(text, match.start(), match.end()),
                    'pattern': pattern
                })
        
        return cri_data
    
    def _extract_power_density_values(self, text: str) -> List[Dict]:
        """Extract power density values"""
        power_data = []
        
        patterns = [
            r'(\d+(?:\.\d+)?)\s*W/m²',
            r'(\d+(?:\.\d+)?)\s*W/m2',
            r'(\d+(?:\.\d+)?)\s*W/m\^2',
            r'power density[:\s]*(\d+(?:\.\d+)?)\s*W/m²',
            r'lighting power density[:\s]*(\d+(?:\.\d+)?)\s*W/m²'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                value = float(match.groups()[0])
                power_data.append({
                    'value': value,
                    'unit': 'W/m²',
                    'context': self._extract_context(text, match.start(), match.end()),
                    'pattern': pattern
                })
        
        return power_data
    
    def _extract_uniformity_values(self, text: str) -> List[Dict]:
        """Extract uniformity values"""
        uniformity_data = []
        
        patterns = [
            r'uniformity[:\s]*(?:≥|>=|minimum|min)\s*(\d+(?:\.\d+)?)',
            r'(?:≥|>=|minimum|min)\s*(\d+(?:\.\d+)?)\s*uniformity',
            r'uniformity ratio[:\s]*(\d+(?:\.\d+)?)',
            r'Uo[:\s]*(?:≥|>=|minimum|min)\s*(\d+(?:\.\d+)?)'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                value = float(match.groups()[0])
                uniformity_data.append({
                    'value': value,
                    'context': self._extract_context(text, match.start(), match.end()),
                    'pattern': pattern
                })
        
        return uniformity_data
    
    def _extract_applications(self, text: str) -> List[Dict]:
        """Extract application types and their requirements"""
        applications = []
        
        app_patterns = [
            r'office\s*work[:\s]*(\d+)\s*lux',
            r'conference\s*room[:\s]*(\d+)\s*lux',
            r'corridor[:\s]*(\d+)\s*lux',
            r'reception[:\s]*(\d+)\s*lux',
            r'staircase[:\s]*(\d+)\s*lux',
            r'detailed\s*work[:\s]*(\d+)\s*lux',
            r'general\s*work[:\s]*(\d+)\s*lux'
        ]
        
        for pattern in app_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                app_type = pattern.split('[')[0].strip()
                illuminance = int(match.groups()[0])
                applications.append({
                    'application': app_type,
                    'illuminance': illuminance,
                    'context': self._extract_context(text, match.start(), match.end())
                })
        
        return applications
    
    def _extract_structured_tables(self, text: str) -> List[Dict]:
        """Extract structured table data"""
        tables = []
        
        # Look for table-like structures
        table_patterns = [
            r'(\w+)\s+(\d+)\s+lux\s+(\d+)\s+UGR\s+(\d+)\s+CRI',
            r'(\w+)\s+(\d+)\s*lux\s+(\d+)\s*UGR\s+(\d+)\s*CRI'
        ]
        
        for pattern in table_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                groups = match.groups()
                if len(groups) >= 4:
                    tables.append({
                        'application': groups[0],
                        'illuminance': int(groups[1]),
                        'ugr': int(groups[2]),
                        'cri': int(groups[3]),
                        'context': self._extract_context(text, match.start(), match.end())
                    })
        
        return tables
    
    def _extract_context(self, text: str, start: int, end: int, context_length: int = 150) -> str:
        """Extract context around a match"""
        try:
            context_start = max(0, start - context_length)
            context_end = min(len(text), end + context_length)
            return text[context_start:context_end].strip()
        except:
            return ""
    
    def _generate_improvement_notes(self, extracted_params: Dict) -> List[str]:
        """Generate notes about the extraction improvements"""
        notes = []
        
        total_params = sum(len(v) for v in extracted_params.values() if isinstance(v, list))
        notes.append(f"Extracted {total_params} total parameters")
        
        for param_type, values in extracted_params.items():
            if isinstance(values, list) and values:
                notes.append(f"Found {len(values)} {param_type} values")
        
        if extracted_params.get('tables'):
            notes.append(f"Extracted {len(extracted_params['tables'])} structured tables")
        
        return notes
    
    def _save_improved_data(self):
        """Save improved data to file"""
        output_file = Path("uploads/improved_standards_data.json")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.improved_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved improved data to {output_file}")
        
        # Also save a summary
        summary = self._generate_summary()
        summary_file = Path("uploads/extraction_summary.json")
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved extraction summary to {summary_file}")
    
    def _generate_summary(self) -> Dict:
        """Generate summary of extracted data"""
        summary = {
            'total_documents': len(self.improved_data),
            'total_parameters': {},
            'applications_found': set(),
            'extraction_quality': {}
        }
        
        for doc_name, doc_data in self.improved_data.items():
            params = doc_data.get('extracted_parameters', {})
            
            for param_type, values in params.items():
                if isinstance(values, list):
                    if param_type not in summary['total_parameters']:
                        summary['total_parameters'][param_type] = 0
                    summary['total_parameters'][param_type] += len(values)
                    
                    # Collect applications
                    if param_type == 'applications':
                        for app in values:
                            if 'application' in app:
                                summary['applications_found'].add(app['application'])
        
        summary['applications_found'] = list(summary['applications_found'])
        
        return summary

def main():
    """Main function"""
    print("🔧 IMPROVING STANDARDS DATA EXTRACTION")
    print("=" * 50)
    
    improver = StandardsDataImprover()
    improver.improve_extraction()
    
    print("\n✅ IMPROVEMENT COMPLETED!")
    print("=" * 50)
    print("📁 Check uploads/improved_standards_data.json for detailed results")
    print("📊 Check uploads/extraction_summary.json for summary")
    print("\n🚀 Now you can use the enhanced chat API for better accuracy!")

if __name__ == "__main__":
    main()
