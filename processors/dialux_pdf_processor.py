"""
Dialux PDF Report Processor
Processes Dialux PDF reports and evaluates them against lighting standards
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

@dataclass
class DialuxReport:
    """Complete Dialux report data"""
    project_name: str
    rooms: List[DialuxRoom]
    total_area: float
    total_power: float
    average_power_density: float
    overall_uniformity: float
    worst_ugr: float

class DialuxPDFProcessor:
    """Processes Dialux PDF reports and extracts lighting data"""
    
    def __init__(self):
        self.room_patterns = {
            'name': r'Room[:\s]*([^\n\r]+)',
            'area': r'Area[:\s]*(\d+(?:\.\d+)?)\s*m²',
            'illuminance_avg': r'Average[:\s]*(\d+(?:\.\d+)?)\s*lux',
            'illuminance_min': r'Minimum[:\s]*(\d+(?:\.\d+)?)\s*lux',
            'illuminance_max': r'Maximum[:\s]*(\d+(?:\.\d+)?)\s*lux',
            'uniformity': r'Uniformity[:\s]*(\d+(?:\.\d+)?)',
            'ugr': r'UGR[:\s]*(\d+(?:\.\d+)?)',
            'power_density': r'Power\s+Density[:\s]*(\d+(?:\.\d+)?)\s*W/m²'
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
            except Exception as e:
                print(f"PyMuPDF failed: {e}")
        
        # Try pdfminer as last resort
        if not text:
            try:
                from pdfminer.high_level import extract_text
                text = extract_text(pdf_path)
            except Exception as e:
                print(f"pdfminer failed: {e}")
        
        return text
    
    def extract_project_name(self, text: str) -> str:
        """Extract project name from Dialux report"""
        patterns = [
            r'Project[:\s]*([^\n\r]+)',
            r'Title[:\s]*([^\n\r]+)',
            r'Name[:\s]*([^\n\r]+)',
            r'Building[:\s]*([^\n\r]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return "Unknown Project"
    
    def extract_room_data(self, text: str) -> List[DialuxRoom]:
        """Extract room data from Dialux report text"""
        rooms = []
        
        # Look for room sections in the text
        # Dialux reports typically have sections like "Room: Office 1" or "Space: Conference Room"
        room_sections = re.split(r'(?i)(?:room|space|area)[:\s]*', text)
        
        for i, section in enumerate(room_sections[1:], 1):  # Skip first empty section
            try:
                room_data = {}
                
                # Extract room name (first line or from context)
                name_match = re.search(r'^([^\n\r]+)', section.strip())
                room_data['name'] = name_match.group(1).strip() if name_match else f"Room {i}"
                
                # Extract numerical data using patterns
                for param, pattern in self.room_patterns.items():
                    if param == 'name':
                        continue
                    
                    match = re.search(pattern, section, re.IGNORECASE)
                    if match:
                        try:
                            room_data[param] = float(match.group(1))
                        except ValueError:
                            room_data[param] = 0.0
                    else:
                        room_data[param] = 0.0
                
                # Create room object
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
                
                # Only add room if it has meaningful data
                if room.area > 0 or room.illuminance_avg > 0:
                    rooms.append(room)
                    
            except Exception as e:
                print(f"Failed to parse room section {i}: {e}")
                continue
        
        return rooms
    
    def calculate_summary_stats(self, rooms: List[DialuxRoom]) -> Dict:
        """Calculate summary statistics for all rooms"""
        if not rooms:
            return {
                'total_area': 0,
                'total_power': 0,
                'average_power_density': 0,
                'overall_uniformity': 0,
                'worst_ugr': 0
            }
        
        total_area = sum(room.area for room in rooms)
        total_power = sum(room.area * room.power_density for room in rooms)
        
        # Weighted average power density
        if total_area > 0:
            average_power_density = total_power / total_area
        else:
            average_power_density = 0
        
        # Average uniformity
        uniformities = [room.uniformity for room in rooms if room.uniformity > 0]
        overall_uniformity = sum(uniformities) / len(uniformities) if uniformities else 0
        
        # Worst UGR
        ugrs = [room.ugr for room in rooms if room.ugr > 0]
        worst_ugr = max(ugrs) if ugrs else 0
        
        return {
            'total_area': total_area,
            'total_power': total_power,
            'average_power_density': average_power_density,
            'overall_uniformity': overall_uniformity,
            'worst_ugr': worst_ugr
        }
    
    def process_dialux_pdf(self, pdf_path: Path) -> Optional[DialuxReport]:
        """Process a Dialux PDF report file"""
        try:
            print(f"Processing Dialux PDF: {pdf_path.name}")
            
            # Extract text from PDF
            text = self.extract_text_from_pdf(pdf_path)
            if not text.strip():
                print("No text extracted from PDF")
                return None
            
            # Extract project name
            project_name = self.extract_project_name(text)
            
            # Extract room data
            rooms = self.extract_room_data(text)
            
            if not rooms:
                print("No room data found in Dialux report")
                return None
            
            # Calculate summary statistics
            stats = self.calculate_summary_stats(rooms)
            
            # Create Dialux report
            report = DialuxReport(
                project_name=project_name,
                rooms=rooms,
                total_area=stats['total_area'],
                total_power=stats['total_power'],
                average_power_density=stats['average_power_density'],
                overall_uniformity=stats['overall_uniformity'],
                worst_ugr=stats['worst_ugr']
            )
            
            print(f"Successfully processed Dialux report with {len(rooms)} rooms")
            return report
            
        except Exception as e:
            print(f"Failed to process Dialux PDF {pdf_path.name}: {e}")
            return None

def evaluate_dialux_pdf():
    """Evaluate a Dialux PDF report against standards"""
    print("📊 Dialux PDF Report Evaluator")
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
    
    # Process Dialux PDF
    processor = DialuxPDFProcessor()
    dialux_report = processor.process_dialux_pdf(file_path)
    
    if not dialux_report:
        print("❌ Failed to process Dialux PDF report")
        return
    
    print(f"✅ Processed report: {dialux_report.project_name}")
    print(f"   Rooms: {len(dialux_report.rooms)}")
    print(f"   Total Area: {dialux_report.total_area:.1f} m²")
    print(f"   Average Power Density: {dialux_report.average_power_density:.2f} W/m²")
    
    # Import the simple evaluator for compliance checking
    from simple_lighting_evaluator import SimpleLightingEvaluator, LightingParameter
    
    evaluator = SimpleLightingEvaluator()
    
    print(f"\n🔍 Evaluating each room against standards...")
    print("=" * 50)
    
    total_rooms = len(dialux_report.rooms)
    passed_rooms = 0
    
    for room in dialux_report.rooms:
        print(f"\n🏠 Room: {room.name}")
        print(f"   Area: {room.area:.1f} m²")
        print(f"   Illuminance: {room.illuminance_avg:.0f} lux (min: {room.illuminance_min:.0f}, max: {room.illuminance_max:.0f})")
        print(f"   Uniformity: {room.uniformity:.2f}")
        print(f"   UGR: {room.ugr:.1f}")
        print(f"   Power Density: {room.power_density:.2f} W/m²")
        
        # Check compliance for key parameters
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
            print("   ✅ Room PASSES compliance")
        else:
            print("   ❌ Room FAILS compliance")
        
        # Show recommendations
        if illuminance_result.compliance_status != "PASS":
            print(f"   💡 Illuminance: {illuminance_result.recommendation}")
        if ugr_result.compliance_status != "PASS":
            print(f"   💡 UGR: {ugr_result.recommendation}")
        if power_result.compliance_status != "PASS":
            print(f"   💡 Power: {power_result.recommendation}")
    
    # Overall summary
    overall_compliance = (passed_rooms / total_rooms * 100) if total_rooms > 0 else 0
    
    print(f"\n" + "=" * 50)
    print("📊 DIALUX PDF REPORT SUMMARY")
    print("=" * 50)
    print(f"Project: {dialux_report.project_name}")
    print(f"Total Rooms: {total_rooms}")
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
    
    # Save evaluation results
    output_file = file_path.parent / f"{file_path.stem}_evaluation.json"
    evaluation_data = {
        "project_name": dialux_report.project_name,
        "evaluation_date": datetime.now().isoformat(),
        "overall_compliance": overall_compliance,
        "total_rooms": total_rooms,
        "compliant_rooms": passed_rooms,
        "rooms": [
            {
                "name": room.name,
                "area": room.area,
                "illuminance_avg": room.illuminance_avg,
                "uniformity": room.uniformity,
                "ugr": room.ugr,
                "power_density": room.power_density
            }
            for room in dialux_report.rooms
        ]
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(evaluation_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Evaluation saved to: {output_file}")

def main():
    """Main function"""
    print("🚀 Dialux PDF Report Processor")
    print("=" * 40)
    print("This tool processes Dialux PDF reports and evaluates them against lighting standards")
    print()
    
    evaluate_dialux_pdf()

if __name__ == "__main__":
    main()
