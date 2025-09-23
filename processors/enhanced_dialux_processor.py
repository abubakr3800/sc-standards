"""
Enhanced Dialux PDF Processor
More robust processor that can handle different Dialux PDF formats
"""
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class DialuxRoom:
    """Represents a room in Dialux report"""
    name: str
    area: float
    illuminance_avg: float
    illuminance_min: float
    illuminance_max: float
    uniformity: float
    ugr: float
    power_density: float

class EnhancedDialuxProcessor:
    """Enhanced processor that can handle various Dialux PDF formats"""
    
    def __init__(self):
        # More flexible patterns for different Dialux formats
        self.patterns = {
            'illuminance': [
                r'(\d+(?:\.\d+)?)\s*lux',
                r'illuminance[:\s]*(\d+(?:\.\d+)?)',
                r'illumination[:\s]*(\d+(?:\.\d+)?)',
                r'avg[:\s]*(\d+(?:\.\d+)?)',
                r'average[:\s]*(\d+(?:\.\d+)?)',
                r'mean[:\s]*(\d+(?:\.\d+)?)'
            ],
            'area': [
                r'(\d+(?:\.\d+)?)\s*m²',
                r'(\d+(?:\.\d+)?)\s*m2',
                r'area[:\s]*(\d+(?:\.\d+)?)',
                r'size[:\s]*(\d+(?:\.\d+)?)'
            ],
            'ugr': [
                r'UGR[:\s]*(\d+(?:\.\d+)?)',
                r'ugr[:\s]*(\d+(?:\.\d+)?)',
                r'glare[:\s]*(\d+(?:\.\d+)?)',
                r'unified\s+glare[:\s]*(\d+(?:\.\d+)?)'
            ],
            'uniformity': [
                r'uniformity[:\s]*(\d+(?:\.\d+)?)',
                r'uniform[:\s]*(\d+(?:\.\d+)?)',
                r'U[o0][:\s]*(\d+(?:\.\d+)?)',
                r'min/max[:\s]*(\d+(?:\.\d+)?)'
            ],
            'power': [
                r'power[:\s]*(\d+(?:\.\d+)?)\s*W/m²',
                r'power[:\s]*(\d+(?:\.\d+)?)\s*W/m2',
                r'LPD[:\s]*(\d+(?:\.\d+)?)',
                r'lighting\s+power[:\s]*(\d+(?:\.\d+)?)'
            ]
        }
    
    def extract_text_from_pdf(self, pdf_path: Path) -> str:
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
            print(f"✅ Extracted {len(text)} characters using pdfplumber")
        except Exception as e:
            print(f"pdfplumber failed: {e}")
        
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
                print(f"✅ Extracted {len(text)} characters using PyMuPDF")
            except Exception as e:
                print(f"PyMuPDF failed: {e}")
        
        return text
    
    def extract_all_lighting_data(self, text: str) -> List[Dict]:
        """Extract all lighting data from text using flexible patterns"""
        lighting_data = []
        
        # Split text into lines for analysis
        lines = text.split('\n')
        
        # Look for numerical values that could be lighting parameters
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            # Skip empty lines
            if not line.strip():
                continue
            
            # Look for lines that might contain lighting data
            if any(keyword in line_lower for keyword in ['lux', 'ugr', 'uniformity', 'power', 'area', 'illuminance']):
                data = self._extract_data_from_line(line, i)
                if data:
                    lighting_data.append(data)
        
        # Also try to extract data from the entire text
        global_data = self._extract_global_data(text)
        if global_data:
            lighting_data.extend(global_data)
        
        return lighting_data
    
    def _extract_data_from_line(self, line: str, line_num: int) -> Optional[Dict]:
        """Extract data from a single line"""
        data = {}
        
        # Extract illuminance values
        illuminance_matches = re.findall(r'(\d+(?:\.\d+)?)\s*lux', line, re.IGNORECASE)
        if illuminance_matches:
            data['illuminance'] = [float(x) for x in illuminance_matches]
        
        # Extract UGR values
        ugr_matches = re.findall(r'UGR[:\s]*(\d+(?:\.\d+)?)', line, re.IGNORECASE)
        if ugr_matches:
            data['ugr'] = float(ugr_matches[0])
        
        # Extract area values
        area_matches = re.findall(r'(\d+(?:\.\d+)?)\s*m²', line, re.IGNORECASE)
        if area_matches:
            data['area'] = float(area_matches[0])
        
        # Extract power density
        power_matches = re.findall(r'(\d+(?:\.\d+)?)\s*W/m²', line, re.IGNORECASE)
        if power_matches:
            data['power_density'] = float(power_matches[0])
        
        # Extract uniformity
        uniformity_matches = re.findall(r'uniformity[:\s]*(\d+(?:\.\d+)?)', line, re.IGNORECASE)
        if uniformity_matches:
            data['uniformity'] = float(uniformity_matches[0])
        
        if data:
            data['line_number'] = line_num
            data['source_line'] = line.strip()
            return data
        
        return None
    
    def _extract_global_data(self, text: str) -> List[Dict]:
        """Extract data from the entire text using global patterns"""
        data = []
        
        # Find all illuminance values
        illuminance_matches = re.findall(r'(\d+(?:\.\d+)?)\s*lux', text, re.IGNORECASE)
        if illuminance_matches:
            for i, value in enumerate(illuminance_matches):
                data.append({
                    'illuminance': float(value),
                    'type': 'illuminance',
                    'source': f'Global pattern match {i+1}'
                })
        
        # Find all UGR values
        ugr_matches = re.findall(r'UGR[:\s]*(\d+(?:\.\d+)?)', text, re.IGNORECASE)
        if ugr_matches:
            for i, value in enumerate(ugr_matches):
                data.append({
                    'ugr': float(value),
                    'type': 'ugr',
                    'source': f'Global pattern match {i+1}'
                })
        
        return data
    
    def create_rooms_from_data(self, lighting_data: List[Dict]) -> List[DialuxRoom]:
        """Create room objects from extracted data"""
        rooms = []
        
        # Group data by proximity (lines close together might be from the same room)
        grouped_data = self._group_data_by_proximity(lighting_data)
        
        for i, group in enumerate(grouped_data):
            room_data = {
                'name': f'Room {i+1}',
                'area': 0.0,
                'illuminance_avg': 0.0,
                'illuminance_min': 0.0,
                'illuminance_max': 0.0,
                'uniformity': 0.0,
                'ugr': 0.0,
                'power_density': 0.0
            }
            
            # Extract values from the group
            for item in group:
                if 'illuminance' in item:
                    if isinstance(item['illuminance'], list):
                        room_data['illuminance_avg'] = sum(item['illuminance']) / len(item['illuminance'])
                        room_data['illuminance_min'] = min(item['illuminance'])
                        room_data['illuminance_max'] = max(item['illuminance'])
                    else:
                        room_data['illuminance_avg'] = item['illuminance']
                
                if 'ugr' in item:
                    room_data['ugr'] = item['ugr']
                
                if 'area' in item:
                    room_data['area'] = item['area']
                
                if 'power_density' in item:
                    room_data['power_density'] = item['power_density']
                
                if 'uniformity' in item:
                    room_data['uniformity'] = item['uniformity']
            
            # Only create room if it has meaningful data
            if room_data['illuminance_avg'] > 0 or room_data['area'] > 0:
                room = DialuxRoom(
                    name=room_data['name'],
                    area=room_data['area'],
                    illuminance_avg=room_data['illuminance_avg'],
                    illuminance_min=room_data['illuminance_min'],
                    illuminance_max=room_data['illuminance_max'],
                    uniformity=room_data['uniformity'],
                    ugr=room_data['ugr'],
                    power_density=room_data['power_density']
                )
                rooms.append(room)
        
        return rooms
    
    def _group_data_by_proximity(self, data: List[Dict], max_distance: int = 5) -> List[List[Dict]]:
        """Group data items that are close together in the document"""
        if not data:
            return []
        
        # Sort by line number if available
        data_with_lines = [item for item in data if 'line_number' in item]
        data_without_lines = [item for item in data if 'line_number' not in item]
        
        if not data_with_lines:
            return [data_without_lines] if data_without_lines else []
        
        data_with_lines.sort(key=lambda x: x['line_number'])
        
        groups = []
        current_group = [data_with_lines[0]]
        
        for i in range(1, len(data_with_lines)):
            if data_with_lines[i]['line_number'] - data_with_lines[i-1]['line_number'] <= max_distance:
                current_group.append(data_with_lines[i])
            else:
                groups.append(current_group)
                current_group = [data_with_lines[i]]
        
        groups.append(current_group)
        
        # Add data without line numbers to the first group
        if data_without_lines and groups:
            groups[0].extend(data_without_lines)
        elif data_without_lines:
            groups.append(data_without_lines)
        
        return groups
    
    def process_dialux_pdf(self, pdf_path: Path) -> Optional[List[DialuxRoom]]:
        """Process a Dialux PDF and extract lighting data"""
        try:
            print(f"Processing Dialux PDF: {pdf_path.name}")
            
            # Extract text
            text = self.extract_text_from_pdf(pdf_path)
            if not text.strip():
                print("No text extracted from PDF")
                return None
            
            print(f"Extracted text length: {len(text)} characters")
            
            # Extract lighting data
            lighting_data = self.extract_all_lighting_data(text)
            print(f"Found {len(lighting_data)} data items")
            
            if not lighting_data:
                print("No lighting data found")
                return None
            
            # Create rooms from data
            rooms = self.create_rooms_from_data(lighting_data)
            print(f"Created {len(rooms)} rooms")
            
            return rooms
            
        except Exception as e:
            print(f"Error processing PDF: {e}")
            return None

def evaluate_dialux_pdf_enhanced():
    """Enhanced evaluation of Dialux PDF"""
    print("📊 Enhanced Dialux PDF Report Evaluator")
    print("=" * 40)
    
    # Get file path
    file_path = input("Enter path to Dialux PDF report: ").strip()
    if not file_path:
        print("❌ No file path provided")
        return
    
    file_path = Path(file_path)
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return
    
    # Process PDF
    processor = EnhancedDialuxProcessor()
    rooms = processor.process_dialux_pdf(file_path)
    
    if not rooms:
        print("❌ No lighting data could be extracted from the PDF")
        print("\n💡 This might be because:")
        print("   • The PDF is scanned (not text-based)")
        print("   • The format is different from expected")
        print("   • The PDF is password protected")
        print("   • The text extraction failed")
        return
    
    print(f"✅ Successfully extracted data from {len(rooms)} rooms")
    
    # Import evaluator
    from simple_lighting_evaluator import SimpleLightingEvaluator, LightingParameter
    
    evaluator = SimpleLightingEvaluator()
    
    print(f"\n🔍 Evaluating rooms against standards...")
    print("=" * 50)
    
    passed_rooms = 0
    
    for room in rooms:
        print(f"\n🏠 {room.name}:")
        print(f"   Area: {room.area:.1f} m²")
        print(f"   Illuminance: {room.illuminance_avg:.0f} lux")
        print(f"   UGR: {room.ugr:.1f}")
        print(f"   Power Density: {room.power_density:.2f} W/m²")
        
        # Check compliance
        illuminance_param = LightingParameter("illuminance", room.illuminance_avg, "lux", room.name)
        illuminance_result = evaluator.check_compliance(illuminance_param, "office")
        
        ugr_param = LightingParameter("ugr", room.ugr, "", room.name)
        ugr_result = evaluator.check_compliance(ugr_param, "office")
        
        power_param = LightingParameter("power_density", room.power_density, "W/m²", room.name)
        power_result = evaluator.check_compliance(power_param, "office")
        
        # Room compliance
        room_passed = all([
            illuminance_result.compliance_status == "PASS",
            ugr_result.compliance_status == "PASS",
            power_result.compliance_status == "PASS"
        ])
        
        if room_passed:
            passed_rooms += 1
            print("   ✅ PASSES compliance")
        else:
            print("   ❌ FAILS compliance")
        
        # Show recommendations
        if illuminance_result.compliance_status != "PASS":
            print(f"   💡 Illuminance: {illuminance_result.recommendation}")
        if ugr_result.compliance_status != "PASS":
            print(f"   💡 UGR: {ugr_result.recommendation}")
        if power_result.compliance_status != "PASS":
            print(f"   💡 Power: {power_result.recommendation}")
    
    # Summary
    overall_compliance = (passed_rooms / len(rooms) * 100) if rooms else 0
    
    print(f"\n" + "=" * 50)
    print("📊 EVALUATION SUMMARY")
    print("=" * 50)
    print(f"Total Rooms: {len(rooms)}")
    print(f"Compliant Rooms: {passed_rooms}")
    print(f"Overall Compliance: {overall_compliance:.1f}%")
    
    if overall_compliance >= 90:
        print("🎉 EXCELLENT - Report meets standards!")
    elif overall_compliance >= 75:
        print("✅ GOOD - Minor improvements needed")
    elif overall_compliance >= 60:
        print("⚠️ ACCEPTABLE - Some improvements required")
    else:
        print("❌ POOR - Significant improvements needed")

def main():
    """Main function"""
    print("🚀 Enhanced Dialux PDF Processor")
    print("=" * 40)
    print("This enhanced processor can handle various Dialux PDF formats")
    print()
    
    evaluate_dialux_pdf_enhanced()

if __name__ == "__main__":
    main()
