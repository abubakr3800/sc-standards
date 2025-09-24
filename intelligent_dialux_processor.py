#!/usr/bin/env python3
"""
Intelligent Dialux PDF Processor
Smart extraction that consolidates data and focuses on actual rooms/spaces
"""
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class IntelligentRoom:
    """Intelligent room data with consolidated parameters"""
    name: str
    area: float
    
    # Core lighting parameters
    illuminance_avg: float
    illuminance_min: float
    illuminance_max: float
    uniformity: float
    ugr: float
    power_density: float
    
    # Additional parameters (if available)
    color_temperature: float
    color_rendering_index: float
    luminous_efficacy: float
    mounting_height: float
    
    # Data quality indicators
    data_completeness: float  # 0-1 score
    confidence_score: float   # 0-1 score
    
    # Compliance flags
    illuminance_compliant: bool
    uniformity_compliant: bool
    glare_compliant: bool
    power_compliant: bool

@dataclass
class IntelligentReport:
    """Intelligent Dialux report with consolidated analysis"""
    project_name: str
    project_type: str
    total_rooms: int
    total_area: float
    
    # Overall statistics
    overall_illuminance_avg: float
    overall_uniformity_avg: float
    overall_ugr_avg: float
    overall_power_density_avg: float
    
    # Compliance statistics
    overall_compliance_rate: float
    data_quality_score: float
    
    # Detailed room data
    rooms: List[IntelligentRoom]
    
    # Standards analysis
    applicable_standards: List[str]
    best_matching_standard: str
    standards_compliance: Dict[str, float]

class IntelligentDialuxProcessor:
    """Intelligent processor that consolidates data and focuses on actual rooms"""
    
    def __init__(self):
        # Core patterns for essential lighting parameters
        self.core_patterns = {
            'illuminance_avg': [
                r'(?:average|avg|mean|e\s*avg|em)[:\s]*(\d+(?:\.\d+)?)\s*(?:lux|lx)',
                r'(\d+(?:\.\d+)?)\s*(?:lux|lx)\s*(?:average|avg|mean)',
                r'illuminance[:\s]*(\d+(?:\.\d+)?)\s*(?:lux|lx)',
                r'e[:\s]*(\d+(?:\.\d+)?)\s*(?:lux|lx)',
                r'(\d+(?:\.\d+)?)\s*(?:lux|lx)(?:\s*\(avg\))?'
            ],
            
            'illuminance_min': [
                r'(?:minimum|min|e\s*min)[:\s]*(\d+(?:\.\d+)?)\s*(?:lux|lx)',
                r'(\d+(?:\.\d+)?)\s*(?:lux|lx)\s*(?:minimum|min)',
                r'(\d+(?:\.\d+)?)\s*(?:lux|lx)\s*\(min\)'
            ],
            
            'illuminance_max': [
                r'(?:maximum|max|e\s*max)[:\s]*(\d+(?:\.\d+)?)\s*(?:lux|lx)',
                r'(\d+(?:\.\d+)?)\s*(?:lux|lx)\s*(?:maximum|max)',
                r'(\d+(?:\.\d+)?)\s*(?:lux|lx)\s*\(max\)'
            ],
            
            'uniformity': [
                r'(?:uniformity|uniform|u0)[:\s]*(\d+(?:\.\d+)?)',
                r'(\d+(?:\.\d+)?)\s*(?:uniformity|uniform)',
                r'(\d+(?:\.\d+)?)\s*\(uniformity\)',
                r'u0[:\s]*(\d+(?:\.\d+)?)'
            ],
            
            'ugr': [
                r'(?:ugr|glare)[:\s]*(\d+(?:\.\d+)?)',
                r'(\d+(?:\.\d+)?)\s*(?:ugr|glare)',
                r'(\d+(?:\.\d+)?)\s*\(ugr\)',
                r'ugr[:\s]*(\d+(?:\.\d+)?)'
            ],
            
            'power_density': [
                r'(?:power\s+density|density)[:\s]*(\d+(?:\.\d+)?)\s*(?:w/m²|w/m2|watt/m²)',
                r'(\d+(?:\.\d+)?)\s*(?:w/m²|w/m2|watt/m²)',
                r'(\d+(?:\.\d+)?)\s*(?:w/m²|w/m2|watt/m²)\s*(?:power|density)'
            ],
            
            'area': [
                r'(?:area|size|surface)[:\s]*(\d+(?:\.\d+)?)\s*(?:m²|m2|sqm)',
                r'(\d+(?:\.\d+)?)\s*(?:m²|m2|sqm)',
                r'(\d+(?:\.\d+)?)\s*(?:m²|m2|sqm)\s*(?:area|size)'
            ],
            
            'color_temperature': [
                r'(?:color\s+temperature|temperature|ct)[:\s]*(\d+(?:\.\d+)?)\s*(?:k|kelvin)',
                r'(\d+(?:\.\d+)?)\s*(?:k|kelvin)',
                r'(\d+(?:\.\d+)?)\s*(?:k|kelvin)\s*(?:temperature)'
            ],
            
            'color_rendering_index': [
                r'(?:color\s+rendering\s+index|cri|ra)[:\s]*(\d+(?:\.\d+)?)',
                r'(\d+(?:\.\d+)?)\s*(?:cri|ra)',
                r'(\d+(?:\.\d+)?)\s*(?:cri|ra)\s*(?:index)'
            ],
            
            'luminous_efficacy': [
                r'(?:luminous\s+efficacy|efficacy)[:\s]*(\d+(?:\.\d+)?)\s*(?:lm/w|lumen/watt)',
                r'(\d+(?:\.\d+)?)\s*(?:lm/w|lumen/watt)',
                r'(\d+(?:\.\d+)?)\s*(?:lm/w|lumen/watt)\s*(?:efficacy)'
            ],
            
            'mounting_height': [
                r'(?:mounting\s+height|height)[:\s]*(\d+(?:\.\d+)?)\s*(?:m|meter)',
                r'(\d+(?:\.\d+)?)\s*(?:m|meter)\s*(?:height)',
                r'h[:\s]*(\d+(?:\.\d+)?)\s*(?:m|meter)'
            ]
        }
        
        # Room identification patterns
        self.room_patterns = [
            r'(?:room|space|area|zone|office|meeting|conference|reception|corridor|hall|kitchen|toilet|storage|workshop|factory|retail|shop|display|classroom|laboratory|library|gym|restaurant|cafeteria|auditorium|theater|museum|gallery|warehouse|garage|parking)[:\s]*([^\n\r\d]+?)(?:\s*\d|\s*\(|\s*$)',
            r'([A-Za-z\s]+?)(?:\s*\d+(?:\.\d+)?\s*(?:m²|m2|lux|lx|w/m²))',
            r'([A-Za-z\s]+?)(?:\s*\([^)]*\))?\s*(?:\d+(?:\.\d+)?)',
            r'^([A-Za-z\s]+?)(?:\s*\d)',
            r'([A-Za-z\s]+?)(?:\s*:|\s*$)'
        ]
        
        # Standards database
        self.standards_database = {
            "EN_12464_1_Office": {
                "illuminance_avg": 500,
                "illuminance_min": 300,
                "uniformity": 0.6,
                "ugr": 19,
                "power_density": 10,
                "color_rendering_index": 80
            },
            "EN_12464_1_Meeting": {
                "illuminance_avg": 500,
                "illuminance_min": 300,
                "uniformity": 0.6,
                "ugr": 19,
                "power_density": 10,
                "color_rendering_index": 80
            },
            "EN_12464_1_Corridor": {
                "illuminance_avg": 150,
                "illuminance_min": 100,
                "uniformity": 0.4,
                "ugr": 22,
                "power_density": 5,
                "color_rendering_index": 80
            },
            "EN_12464_1_Storage": {
                "illuminance_avg": 200,
                "illuminance_min": 150,
                "uniformity": 0.4,
                "ugr": 22,
                "power_density": 5,
                "color_rendering_index": 80
            },
            "BREEAM_Office": {
                "illuminance_avg": 500,
                "illuminance_min": 300,
                "uniformity": 0.6,
                "ugr": 19,
                "power_density": 8,
                "color_rendering_index": 80
            }
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
    
    def extract_project_name(self, text: str) -> str:
        """Extract project name from text"""
        lines = text.split('\n')[:20]
        
        for line in lines:
            line = line.strip()
            if len(line) > 5 and not line.isdigit():
                skip_words = ['page', 'date', 'time', 'version', 'dialux', 'report', 'calculation']
                if not any(word in line.lower() for word in skip_words):
                    return line
        
        return "Unknown Project"
    
    def extract_intelligent_data(self, text: str) -> List[Dict[str, Any]]:
        """Extract and consolidate lighting data intelligently"""
        print("🧠 Starting intelligent data extraction...")
        
        # Find all potential room sections
        room_sections = self._find_room_sections(text)
        print(f"🏠 Found {len(room_sections)} potential room sections")
        
        # Extract data from each section
        all_data = []
        for i, section in enumerate(room_sections):
            print(f"🔍 Analyzing room section {i+1}/{len(room_sections)}")
            
            # Extract room name
            room_name = self._extract_room_name(section)
            
            # Extract all parameters from this section
            section_data = self._extract_section_parameters(section, room_name)
            
            if section_data:
                all_data.extend(section_data)
                print(f"   ✅ Found {len(section_data)} parameters for {room_name}")
            else:
                print(f"   ⚠️  No parameters found for {room_name}")
        
        print(f"📊 Total parameters extracted: {len(all_data)}")
        return all_data
    
    def _find_room_sections(self, text: str) -> List[str]:
        """Find sections that likely contain room data"""
        sections = []
        
        # Split by common section delimiters
        potential_sections = re.split(r'\n\s*\n|\f|(?:room|space|area|zone|office|meeting|conference|corridor|hall|storage|workshop|retail|shop|display|classroom|laboratory|library|gym|restaurant|cafeteria|auditorium|theater|museum|gallery|warehouse|garage|parking)', text, flags=re.IGNORECASE)
        
        for section in potential_sections:
            section = section.strip()
            
            # Filter sections that are likely to contain room data
            if self._is_likely_room_section(section):
                sections.append(section)
        
        return sections
    
    def _is_likely_room_section(self, section: str) -> bool:
        """Check if a section is likely to contain room data"""
        if len(section) < 30:  # Too short
            return False
        
        # Look for lighting-related keywords
        lighting_keywords = [
            'illuminance', 'lux', 'lx', 'uniformity', 'ugr', 'glare',
            'power', 'density', 'area', 'room', 'space', 'zone',
            'color', 'temperature', 'cri', 'efficacy', 'height'
        ]
        
        section_lower = section.lower()
        keyword_count = sum(1 for keyword in lighting_keywords if keyword in section_lower)
        
        # Look for numbers (likely lighting values)
        numbers = re.findall(r'\d+(?:\.\d+)?', section)
        
        # Section is likely if it has lighting keywords and numbers
        return keyword_count >= 2 and len(numbers) >= 2
    
    def _extract_room_name(self, section: str) -> str:
        """Extract room name from section"""
        for pattern in self.room_patterns:
            match = re.search(pattern, section, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                if len(name) > 2 and not name.isdigit():
                    # Clean up the name
                    name = re.sub(r'[^\w\s-]', '', name).strip()
                    if len(name) > 2:
                        return name
        
        return "General Space"
    
    def _extract_section_parameters(self, section: str, room_name: str) -> List[Dict[str, Any]]:
        """Extract parameters from a section"""
        data_points = []
        
        for param_name, patterns in self.core_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, section, re.IGNORECASE)
                if match:
                    try:
                        if param_name in ['color_temperature', 'color_rendering_index', 'luminous_efficacy', 'mounting_height']:
                            value = float(match.group(1))
                        else:
                            value = float(match.group(1))
                        
                        if self._is_reasonable_value(param_name, value):
                            data_point = {
                                'parameter': param_name,
                                'value': value,
                                'room_name': room_name,
                                'context': match.group(0),
                                'position': match.start()
                            }
                            data_points.append(data_point)
                            break  # Take first valid match
                    except (ValueError, IndexError):
                        continue
        
        return data_points
    
    def _is_reasonable_value(self, param_name: str, value: float) -> bool:
        """Check if a value is reasonable for a given parameter"""
        reasonable_ranges = {
            'area': (1, 10000),
            'illuminance_avg': (50, 2000),
            'illuminance_min': (10, 1500),
            'illuminance_max': (100, 3000),
            'uniformity': (0.1, 1.0),
            'ugr': (5, 30),
            'power_density': (1, 50),
            'color_temperature': (2000, 6500),
            'color_rendering_index': (50, 100),
            'luminous_efficacy': (50, 200),
            'mounting_height': (1, 10)
        }
        
        if param_name in reasonable_ranges:
            min_val, max_val = reasonable_ranges[param_name]
            return min_val <= value <= max_val
        
        return True
    
    def create_intelligent_rooms(self, lighting_data: List[Dict[str, Any]]) -> List[IntelligentRoom]:
        """Create intelligent room objects with consolidated data"""
        rooms = []
        
        # Group data by room name
        room_groups = {}
        for data_point in lighting_data:
            room_name = data_point.get('room_name', 'General Space')
            if room_name not in room_groups:
                room_groups[room_name] = {}
            
            param_name = data_point.get('parameter')
            value = data_point.get('value')
            if param_name and value is not None:
                room_groups[room_name][param_name] = value
        
        print(f"🏠 Creating intelligent rooms from {len(room_groups)} room groups")
        
        # Create intelligent room objects
        for room_name, room_data in room_groups.items():
            try:
                # Calculate data completeness
                core_params = ['illuminance_avg', 'uniformity', 'ugr', 'power_density', 'area']
                available_params = [p for p in core_params if p in room_data]
                data_completeness = len(available_params) / len(core_params)
                
                # Calculate confidence score based on data quality
                confidence_score = self._calculate_confidence_score(room_data)
                
                # Create room with consolidated data
                room = IntelligentRoom(
                    name=room_name,
                    area=room_data.get('area', 0.0),
                    illuminance_avg=room_data.get('illuminance_avg', 0.0),
                    illuminance_min=room_data.get('illuminance_min', 0.0),
                    illuminance_max=room_data.get('illuminance_max', 0.0),
                    uniformity=room_data.get('uniformity', 0.0),
                    ugr=room_data.get('ugr', 0.0),
                    power_density=room_data.get('power_density', 0.0),
                    color_temperature=room_data.get('color_temperature', 0.0),
                    color_rendering_index=room_data.get('color_rendering_index', 0.0),
                    luminous_efficacy=room_data.get('luminous_efficacy', 0.0),
                    mounting_height=room_data.get('mounting_height', 0.0),
                    data_completeness=data_completeness,
                    confidence_score=confidence_score,
                    illuminance_compliant=False,
                    uniformity_compliant=False,
                    glare_compliant=False,
                    power_compliant=False
                )
                
                # Calculate compliance
                room = self._calculate_compliance(room)
                
                # Only include rooms with meaningful data
                if data_completeness > 0.2:  # At least 20% of core parameters
                    rooms.append(room)
                    print(f"✅ Created intelligent room: {room_name}")
                    print(f"   📊 Data completeness: {data_completeness:.1%}")
                    print(f"   🎯 Confidence score: {confidence_score:.1%}")
                    print(f"   💡 Illuminance: {room.illuminance_avg} lux")
                    print(f"   📐 Area: {room.area} m²")
                    print(f"   ⚡ Power: {room.power_density} W/m²")
                    print(f"   🎨 CRI: {room.color_rendering_index}")
                    print(f"   🌡️  Color Temp: {room.color_temperature}K")
                
            except Exception as e:
                print(f"❌ Error creating room {room_name}: {e}")
        
        return rooms
    
    def _calculate_confidence_score(self, room_data: Dict[str, float]) -> float:
        """Calculate confidence score based on data quality"""
        score = 0.0
        
        # Base score for having data
        if room_data:
            score += 0.3
        
        # Bonus for core parameters
        core_params = ['illuminance_avg', 'uniformity', 'ugr', 'power_density', 'area']
        for param in core_params:
            if param in room_data and room_data[param] > 0:
                score += 0.1
        
        # Bonus for additional parameters
        additional_params = ['color_temperature', 'color_rendering_index', 'luminous_efficacy', 'mounting_height']
        for param in additional_params:
            if param in room_data and room_data[param] > 0:
                score += 0.05
        
        return min(score, 1.0)
    
    def _calculate_compliance(self, room: IntelligentRoom) -> IntelligentRoom:
        """Calculate compliance for a room"""
        # Determine applicable standard based on room type
        standard = self._get_applicable_standard(room.name)
        
        if standard:
            # Check illuminance compliance
            if room.illuminance_avg >= standard.get('illuminance_avg', 0):
                room.illuminance_compliant = True
            
            # Check uniformity compliance
            if room.uniformity >= standard.get('uniformity', 0):
                room.uniformity_compliant = True
            
            # Check glare compliance (lower is better)
            if room.ugr <= standard.get('ugr', 30):
                room.glare_compliant = True
            
            # Check power compliance (lower is better)
            if room.power_density <= standard.get('power_density', 50):
                room.power_compliant = True
        
        return room
    
    def _get_applicable_standard(self, room_name: str) -> Optional[Dict]:
        """Get applicable standard for room type"""
        room_lower = room_name.lower()
        
        if any(word in room_lower for word in ['office', 'workplace', 'desk']):
            return self.standards_database.get('EN_12464_1_Office')
        elif any(word in room_lower for word in ['meeting', 'conference', 'presentation']):
            return self.standards_database.get('EN_12464_1_Meeting')
        elif any(word in room_lower for word in ['corridor', 'hallway', 'passage']):
            return self.standards_database.get('EN_12464_1_Corridor')
        elif any(word in room_lower for word in ['storage', 'warehouse', 'archive']):
            return self.standards_database.get('EN_12464_1_Storage')
        else:
            return self.standards_database.get('EN_12464_1_Office')  # Default
    
    def process_intelligent_dialux_pdf(self, pdf_path: Path) -> Optional[IntelligentReport]:
        """Process a Dialux PDF with intelligent analysis"""
        try:
            print(f"🧠 Intelligent processing of Dialux PDF: {pdf_path.name}")
            
            # Extract text
            text = self.extract_text_from_pdf(pdf_path)
            if not text.strip():
                print("❌ No text extracted from PDF")
                return None
            
            print(f"📄 Extracted {len(text)} characters of text")
            
            # Extract project name
            project_name = self.extract_project_name(text)
            print(f"🏢 Project: {project_name}")
            
            # Extract intelligent data
            lighting_data = self.extract_intelligent_data(text)
            print(f"📊 Found {len(lighting_data)} data points")
            
            if not lighting_data:
                print("❌ No lighting data found")
                return None
            
            # Create intelligent rooms
            rooms = self.create_intelligent_rooms(lighting_data)
            print(f"🏠 Created {len(rooms)} intelligent rooms")
            
            if not rooms:
                print("❌ No rooms could be created from data")
                return None
            
            # Calculate overall statistics
            total_area = sum(room.area for room in rooms)
            overall_illuminance_avg = sum(room.illuminance_avg for room in rooms) / len(rooms) if rooms else 0
            overall_uniformity_avg = sum(room.uniformity for room in rooms) / len(rooms) if rooms else 0
            overall_ugr_avg = sum(room.ugr for room in rooms) / len(rooms) if rooms else 0
            overall_power_density_avg = sum(room.power_density for room in rooms) / len(rooms) if rooms else 0
            
            # Calculate compliance rates
            illuminance_compliant = sum(1 for room in rooms if room.illuminance_compliant)
            uniformity_compliant = sum(1 for room in rooms if room.uniformity_compliant)
            glare_compliant = sum(1 for room in rooms if room.glare_compliant)
            power_compliant = sum(1 for room in rooms if room.power_compliant)
            
            illuminance_compliance_rate = illuminance_compliant / len(rooms) if rooms else 0
            uniformity_compliance_rate = uniformity_compliant / len(rooms) if rooms else 0
            glare_compliance_rate = glare_compliant / len(rooms) if rooms else 0
            power_compliance_rate = power_compliant / len(rooms) if rooms else 0
            overall_compliance_rate = (illuminance_compliance_rate + uniformity_compliance_rate + 
                                     glare_compliance_rate + power_compliance_rate) / 4
            
            # Calculate data quality score
            data_quality_score = sum(room.data_completeness for room in rooms) / len(rooms) if rooms else 0
            
            # Determine project type
            project_type = self._determine_project_type(rooms)
            
            # Get applicable standards
            applicable_standards = list(self.standards_database.keys())
            standards_compliance = {
                standard: self._calculate_standard_compliance(rooms, standard) 
                for standard in applicable_standards
            }
            
            # Find best matching standard
            best_matching_standard = max(standards_compliance.items(), key=lambda x: x[1])[0] if standards_compliance else "Unknown"
            
            # Create intelligent report
            report = IntelligentReport(
                project_name=project_name,
                project_type=project_type,
                total_rooms=len(rooms),
                total_area=total_area,
                overall_illuminance_avg=overall_illuminance_avg,
                overall_uniformity_avg=overall_uniformity_avg,
                overall_ugr_avg=overall_ugr_avg,
                overall_power_density_avg=overall_power_density_avg,
                overall_compliance_rate=overall_compliance_rate,
                data_quality_score=data_quality_score,
                rooms=rooms,
                applicable_standards=applicable_standards,
                best_matching_standard=best_matching_standard,
                standards_compliance=standards_compliance
            )
            
            print(f"✅ Successfully created intelligent report with {len(rooms)} rooms")
            return report
            
        except Exception as e:
            print(f"❌ Error processing PDF: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _determine_project_type(self, rooms: List[IntelligentRoom]) -> str:
        """Determine overall project type"""
        room_types = []
        for room in rooms:
            room_lower = room.name.lower()
            if any(word in room_lower for word in ['office', 'workplace']):
                room_types.append('Office')
            elif any(word in room_lower for word in ['meeting', 'conference']):
                room_types.append('Meeting')
            elif any(word in room_lower for word in ['retail', 'shop', 'store']):
                room_types.append('Retail')
            elif any(word in room_lower for word in ['industrial', 'factory', 'workshop']):
                room_types.append('Industrial')
            else:
                room_types.append('General')
        
        # Return most common type
        if room_types:
            return max(set(room_types), key=room_types.count)
        return 'General'
    
    def _calculate_standard_compliance(self, rooms: List[IntelligentRoom], standard_name: str) -> float:
        """Calculate compliance rate for a specific standard"""
        standard = self.standards_database.get(standard_name)
        if not standard:
            return 0.0
        
        compliant_rooms = 0
        for room in rooms:
            if (room.illuminance_avg >= standard.get('illuminance_avg', 0) and
                room.uniformity >= standard.get('uniformity', 0) and
                room.ugr <= standard.get('ugr', 30) and
                room.power_density <= standard.get('power_density', 50)):
                compliant_rooms += 1
        
        return compliant_rooms / len(rooms) if rooms else 0.0

def test_intelligent_processor():
    """Test the intelligent processor"""
    processor = IntelligentDialuxProcessor()
    
    # Test with existing PDFs
    test_files = [
        "src/base/EN_12464-1.pdf",
        "src/base/prEN 12464-1.pdf"
    ]
    
    for test_file in test_files:
        pdf_path = Path(test_file)
        if pdf_path.exists():
            print(f"\n🧪 Testing intelligent processor with: {pdf_path.name}")
            result = processor.process_intelligent_dialux_pdf(pdf_path)
            if result:
                print(f"✅ Success: {result.total_rooms} rooms, {result.total_area:.1f} m²")
                print(f"📊 Project Type: {result.project_type}")
                print(f"✅ Overall Compliance: {result.overall_compliance_rate:.1%}")
                print(f"📈 Data Quality: {result.data_quality_score:.1%}")
                print(f"💡 Average Illuminance: {result.overall_illuminance_avg:.1f} lux")
                print(f"⚡ Average Power Density: {result.overall_power_density_avg:.1f} W/m²")
                print(f"🎯 Best Matching Standard: {result.best_matching_standard}")
                
                print(f"\n🏠 Room Details:")
                for room in result.rooms[:3]:  # Show first 3 rooms
                    print(f"   {room.name}:")
                    print(f"     💡 Illuminance: {room.illuminance_avg} lux")
                    print(f"     📐 Area: {room.area} m²")
                    print(f"     ⚡ Power: {room.power_density} W/m²")
                    print(f"     🎨 CRI: {room.color_rendering_index}")
                    print(f"     🌡️  Color Temp: {room.color_temperature}K")
                    print(f"     📊 Data Quality: {room.data_completeness:.1%}")
                    print(f"     🎯 Confidence: {room.confidence_score:.1%}")
                    print(f"     ✅ Compliant: I:{room.illuminance_compliant} U:{room.uniformity_compliant} G:{room.glare_compliant} P:{room.power_compliant}")
            else:
                print("❌ Failed to process")

if __name__ == "__main__":
    test_intelligent_processor()
