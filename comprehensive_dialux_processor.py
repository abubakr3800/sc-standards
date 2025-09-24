#!/usr/bin/env python3
"""
Comprehensive Dialux PDF Processor
Extracts ALL lighting parameters for EVERY room/space with detailed analysis
"""
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ComprehensiveRoom:
    """Comprehensive room data with ALL possible lighting parameters"""
    name: str
    area: float
    
    # Illuminance parameters
    illuminance_avg: float
    illuminance_min: float
    illuminance_max: float
    illuminance_maintained: float
    illuminance_initial: float
    
    # Uniformity parameters
    uniformity: float
    uniformity_ratio: float
    uniformity_min_max: float
    
    # Glare parameters
    ugr: float
    glare_index: float
    glare_rating: float
    
    # Power and efficiency
    power_density: float
    power_total: float
    luminous_efficacy: float
    energy_efficiency: float
    
    # Color parameters
    color_temperature: float
    color_rendering_index: float
    color_quality: str
    
    # Additional parameters
    daylight_factor: float
    daylight_autonomy: float
    light_distribution: str
    luminaire_type: str
    mounting_height: float
    
    # Compliance flags
    illuminance_compliant: bool
    uniformity_compliant: bool
    glare_compliant: bool
    power_compliant: bool

@dataclass
class ComprehensiveReport:
    """Comprehensive Dialux report with detailed analysis"""
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
    illuminance_compliance_rate: float
    uniformity_compliance_rate: float
    glare_compliance_rate: float
    power_compliance_rate: float
    overall_compliance_rate: float
    
    # Detailed room data
    rooms: List[ComprehensiveRoom]
    
    # Standards comparison
    applicable_standards: List[str]
    standards_compliance: Dict[str, float]

class ComprehensiveDialuxProcessor:
    """Comprehensive processor that extracts ALL lighting parameters for EVERY space"""
    
    def __init__(self):
        # Comprehensive patterns for ALL lighting parameters
        self.comprehensive_patterns = {
            # Illuminance patterns - very detailed
            'illuminance_avg': [
                r'(?:average|avg|mean|e\s*avg|e\s*average|em)[:\s]*(\d+(?:\.\d+)?)\s*(?:lux|lx)',
                r'(\d+(?:\.\d+)?)\s*(?:lux|lx)\s*(?:average|avg|mean|em)',
                r'illuminance[:\s]*(\d+(?:\.\d+)?)\s*(?:lux|lx)',
                r'e[:\s]*(\d+(?:\.\d+)?)\s*(?:lux|lx)',
                r'(\d+(?:\.\d+)?)\s*(?:lux|lx)(?:\s*\(avg\))?',
                r'(\d+(?:\.\d+)?)\s*(?:lux|lx)\s*\(em\)',
                r'(\d+(?:\.\d+)?)\s*(?:lux|lx)\s*\(mean\)'
            ],
            
            'illuminance_min': [
                r'(?:minimum|min|e\s*min|e\s*minimum)[:\s]*(\d+(?:\.\d+)?)\s*(?:lux|lx)',
                r'(\d+(?:\.\d+)?)\s*(?:lux|lx)\s*(?:minimum|min)',
                r'(\d+(?:\.\d+)?)\s*(?:lux|lx)\s*\(min\)',
                r'(\d+(?:\.\d+)?)\s*(?:lux|lx)\s*\(minimum\)',
                r'emin[:\s]*(\d+(?:\.\d+)?)\s*(?:lux|lx)'
            ],
            
            'illuminance_max': [
                r'(?:maximum|max|e\s*max|e\s*maximum)[:\s]*(\d+(?:\.\d+)?)\s*(?:lux|lx)',
                r'(\d+(?:\.\d+)?)\s*(?:lux|lx)\s*(?:maximum|max)',
                r'(\d+(?:\.\d+)?)\s*(?:lux|lx)\s*\(max\)',
                r'(\d+(?:\.\d+)?)\s*(?:lux|lx)\s*\(maximum\)',
                r'emax[:\s]*(\d+(?:\.\d+)?)\s*(?:lux|lx)'
            ],
            
            'illuminance_maintained': [
                r'(?:maintained|maintenance)[:\s]*(\d+(?:\.\d+)?)\s*(?:lux|lx)',
                r'(\d+(?:\.\d+)?)\s*(?:lux|lx)\s*(?:maintained|maintenance)',
                r'(\d+(?:\.\d+)?)\s*(?:lux|lx)\s*\(maintained\)',
                r'em[:\s]*(\d+(?:\.\d+)?)\s*(?:lux|lx)'
            ],
            
            'illuminance_initial': [
                r'(?:initial|new)[:\s]*(\d+(?:\.\d+)?)\s*(?:lux|lx)',
                r'(\d+(?:\.\d+)?)\s*(?:lux|lx)\s*(?:initial|new)',
                r'(\d+(?:\.\d+)?)\s*(?:lux|lx)\s*\(initial\)',
                r'ei[:\s]*(\d+(?:\.\d+)?)\s*(?:lux|lx)'
            ],
            
            # Uniformity patterns - comprehensive
            'uniformity': [
                r'(?:uniformity|uniform|u0|u\s*0)[:\s]*(\d+(?:\.\d+)?)',
                r'(\d+(?:\.\d+)?)\s*(?:uniformity|uniform)',
                r'(\d+(?:\.\d+)?)\s*\(uniformity\)',
                r'(\d+(?:\.\d+)?)\s*\(uniform\)',
                r'u0[:\s]*(\d+(?:\.\d+)?)',
                r'(\d+(?:\.\d+)?)\s*\(u0\)',
                r'u[:\s]*(\d+(?:\.\d+)?)'
            ],
            
            'uniformity_ratio': [
                r'(?:uniformity\s+ratio|u\s*ratio)[:\s]*(\d+(?:\.\d+)?)',
                r'(\d+(?:\.\d+)?)\s*(?:uniformity\s+ratio|u\s*ratio)',
                r'(\d+(?:\.\d+)?)\s*\(uniformity\s+ratio\)'
            ],
            
            'uniformity_min_max': [
                r'(?:min/max|emin/emax)[:\s]*(\d+(?:\.\d+)?)',
                r'(\d+(?:\.\d+)?)\s*(?:min/max|emin/emax)',
                r'(\d+(?:\.\d+)?)\s*\(min/max\)'
            ],
            
            # Glare patterns - comprehensive
            'ugr': [
                r'(?:ugr|glare|u\s*g\s*r)[:\s]*(\d+(?:\.\d+)?)',
                r'(\d+(?:\.\d+)?)\s*(?:ugr|glare)',
                r'(\d+(?:\.\d+)?)\s*\(ugr\)',
                r'(\d+(?:\.\d+)?)\s*\(glare\)',
                r'ugr[:\s]*(\d+(?:\.\d+)?)',
                r'glare[:\s]*(\d+(?:\.\d+)?)',
                r'u\s*g\s*r[:\s]*(\d+(?:\.\d+)?)'
            ],
            
            'glare_index': [
                r'(?:glare\s+index|gi)[:\s]*(\d+(?:\.\d+)?)',
                r'(\d+(?:\.\d+)?)\s*(?:glare\s+index|gi)',
                r'(\d+(?:\.\d+)?)\s*\(glare\s+index\)'
            ],
            
            'glare_rating': [
                r'(?:glare\s+rating|gr)[:\s]*(\d+(?:\.\d+)?)',
                r'(\d+(?:\.\d+)?)\s*(?:glare\s+rating|gr)',
                r'(\d+(?:\.\d+)?)\s*\(glare\s+rating\)'
            ],
            
            # Power and efficiency patterns
            'power_density': [
                r'(?:power\s+density|density|p\s*density|specific\s+power)[:\s]*(\d+(?:\.\d+)?)\s*(?:w/m²|w/m2|watt/m²|watt/m2|w/m\^2)',
                r'(\d+(?:\.\d+)?)\s*(?:w/m²|w/m2|watt/m²|watt/m2|w/m\^2)',
                r'(\d+(?:\.\d+)?)\s*(?:w/m²|w/m2|watt/m²|watt/m2|w/m\^2)\s*(?:power|density)',
                r'(\d+(?:\.\d+)?)\s*(?:w/m²|w/m2|watt/m²|watt/m2|w/m\^2)\s*\(power\)',
                r'power[:\s]*(\d+(?:\.\d+)?)\s*(?:w/m²|w/m2|watt/m²|watt/m2|w/m\^2)',
                r'ps[:\s]*(\d+(?:\.\d+)?)\s*(?:w/m²|w/m2|watt/m²|watt/m2|w/m\^2)'
            ],
            
            'power_total': [
                r'(?:total\s+power|power\s+total|ptotal)[:\s]*(\d+(?:\.\d+)?)\s*(?:w|watt)',
                r'(\d+(?:\.\d+)?)\s*(?:w|watt)\s*(?:total|ptotal)',
                r'(\d+(?:\.\d+)?)\s*(?:w|watt)\s*\(total\)',
                r'pt[:\s]*(\d+(?:\.\d+)?)\s*(?:w|watt)'
            ],
            
            'luminous_efficacy': [
                r'(?:luminous\s+efficacy|efficacy|lm/w)[:\s]*(\d+(?:\.\d+)?)\s*(?:lm/w|lumen/watt)',
                r'(\d+(?:\.\d+)?)\s*(?:lm/w|lumen/watt)',
                r'(\d+(?:\.\d+)?)\s*(?:lm/w|lumen/watt)\s*(?:efficacy)',
                r'(\d+(?:\.\d+)?)\s*(?:lm/w|lumen/watt)\s*\(efficacy\)'
            ],
            
            'energy_efficiency': [
                r'(?:energy\s+efficiency|efficiency)[:\s]*(\d+(?:\.\d+)?)\s*(?:%)',
                r'(\d+(?:\.\d+)?)\s*(?:%)\s*(?:efficiency)',
                r'(\d+(?:\.\d+)?)\s*(?:%)\s*\(efficiency\)'
            ],
            
            # Color parameters
            'color_temperature': [
                r'(?:color\s+temperature|temperature|ct|k)[:\s]*(\d+(?:\.\d+)?)\s*(?:k|kelvin)',
                r'(\d+(?:\.\d+)?)\s*(?:k|kelvin)',
                r'(\d+(?:\.\d+)?)\s*(?:k|kelvin)\s*(?:temperature)',
                r'(\d+(?:\.\d+)?)\s*(?:k|kelvin)\s*\(temperature\)',
                r'ct[:\s]*(\d+(?:\.\d+)?)\s*(?:k|kelvin)'
            ],
            
            'color_rendering_index': [
                r'(?:color\s+rendering\s+index|cri|ra)[:\s]*(\d+(?:\.\d+)?)',
                r'(\d+(?:\.\d+)?)\s*(?:cri|ra)',
                r'(\d+(?:\.\d+)?)\s*(?:cri|ra)\s*(?:index)',
                r'(\d+(?:\.\d+)?)\s*(?:cri|ra)\s*\(index\)',
                r'cri[:\s]*(\d+(?:\.\d+)?)',
                r'ra[:\s]*(\d+(?:\.\d+)?)'
            ],
            
            'color_quality': [
                r'(?:color\s+quality|quality)[:\s]*([a-zA-Z\s]+)',
                r'([a-zA-Z\s]+)\s*(?:color\s+quality|quality)',
                r'([a-zA-Z\s]+)\s*\(quality\)'
            ],
            
            # Area patterns
            'area': [
                r'(?:area|size|surface|floor\s+area)[:\s]*(\d+(?:\.\d+)?)\s*(?:m²|m2|sqm|m\^2)',
                r'(\d+(?:\.\d+)?)\s*(?:m²|m2|sqm|m\^2)',
                r'(\d+(?:\.\d+)?)\s*(?:m²|m2|sqm|m\^2)\s*(?:area|size)',
                r'(\d+(?:\.\d+)?)\s*(?:m²|m2|sqm|m\^2)\s*\(area\)',
                r'a[:\s]*(\d+(?:\.\d+)?)\s*(?:m²|m2|sqm|m\^2)'
            ],
            
            # Additional parameters
            'daylight_factor': [
                r'(?:daylight\s+factor|df)[:\s]*(\d+(?:\.\d+)?)\s*(?:%)',
                r'(\d+(?:\.\d+)?)\s*(?:%)\s*(?:daylight\s+factor|df)',
                r'(\d+(?:\.\d+)?)\s*(?:%)\s*\(daylight\s+factor\)',
                r'df[:\s]*(\d+(?:\.\d+)?)\s*(?:%)'
            ],
            
            'daylight_autonomy': [
                r'(?:daylight\s+autonomy|da)[:\s]*(\d+(?:\.\d+)?)\s*(?:%)',
                r'(\d+(?:\.\d+)?)\s*(?:%)\s*(?:daylight\s+autonomy|da)',
                r'(\d+(?:\.\d+)?)\s*(?:%)\s*\(daylight\s+autonomy\)',
                r'da[:\s]*(\d+(?:\.\d+)?)\s*(?:%)'
            ],
            
            'mounting_height': [
                r'(?:mounting\s+height|height|h)[:\s]*(\d+(?:\.\d+)?)\s*(?:m|meter)',
                r'(\d+(?:\.\d+)?)\s*(?:m|meter)\s*(?:height)',
                r'(\d+(?:\.\d+)?)\s*(?:m|meter)\s*\(height\)',
                r'h[:\s]*(\d+(?:\.\d+)?)\s*(?:m|meter)'
            ],
            
            # Room/space identification patterns
            'room_name': [
                r'(?:room|space|area|zone|office|meeting|conference|reception|corridor|hall|kitchen|toilet|storage|workshop|factory|retail|shop|display)[:\s]*([^\n\r\d]+?)(?:\s*\d|\s*\(|\s*$)',
                r'([A-Za-z\s]+?)(?:\s*\d+(?:\.\d+)?\s*(?:m²|m2|lux|lx|w/m²))',
                r'([A-Za-z\s]+?)(?:\s*\([^)]*\))?\s*(?:\d+(?:\.\d+)?)',
                r'^([A-Za-z\s]+?)(?:\s*\d)',
                r'([A-Za-z\s]+?)(?:\s*:|\s*$)',
                r'([A-Za-z\s]+?)(?:\s*room|\s*space|\s*area|\s*zone)'
            ]
        }
        
        # Standards database for compliance checking
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
    
    def extract_comprehensive_data(self, text: str) -> List[Dict[str, Any]]:
        """Extract comprehensive lighting data for ALL spaces"""
        print("🔍 Starting comprehensive data extraction...")
        
        # Split text into sections for analysis
        sections = self._split_into_sections(text)
        print(f"📄 Split text into {len(sections)} sections")
        
        all_data = []
        
        for i, section in enumerate(sections):
            if len(section.strip()) < 20:  # Skip very short sections
                continue
            
            print(f"🔍 Analyzing section {i+1}/{len(sections)}")
            
            # Extract all parameters from this section
            section_data = self._extract_section_parameters(section)
            
            if section_data:
                all_data.extend(section_data)
                print(f"   ✅ Found {len(section_data)} data points")
            else:
                print(f"   ⚠️  No data found")
        
        print(f"📊 Total data points extracted: {len(all_data)}")
        return all_data
    
    def _split_into_sections(self, text: str) -> List[str]:
        """Split text into meaningful sections"""
        # Split by double newlines, page breaks, or section headers
        sections = re.split(r'\n\s*\n|\f|(?:room|space|area|zone|office|meeting|conference)', text, flags=re.IGNORECASE)
        
        # Clean up sections
        cleaned_sections = []
        for section in sections:
            section = section.strip()
            if len(section) > 20:  # Only keep substantial sections
                cleaned_sections.append(section)
        
        return cleaned_sections
    
    def _extract_section_parameters(self, section: str) -> List[Dict[str, Any]]:
        """Extract all parameters from a text section"""
        data_points = []
        
        # Extract room name
        room_name = self._extract_room_name(section)
        
        # Extract all parameters
        for param_name, patterns in self.comprehensive_patterns.items():
            if param_name == 'room_name':
                continue
                
            for pattern in patterns:
                matches = re.finditer(pattern, section, re.IGNORECASE)
                for match in matches:
                    try:
                        if param_name in ['color_quality', 'light_distribution', 'luminaire_type']:
                            value = match.group(1).strip()
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
    
    def _extract_room_name(self, text: str) -> str:
        """Extract room name from text"""
        for pattern in self.comprehensive_patterns['room_name']:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                if len(name) > 2 and not name.isdigit():
                    return name
        
        return "General Space"
    
    def _is_reasonable_value(self, param_name: str, value) -> bool:
        """Check if a value is reasonable for a given parameter"""
        if isinstance(value, str):
            return len(value) > 0
        
        reasonable_ranges = {
            'area': (1, 10000),
            'illuminance_avg': (50, 2000),
            'illuminance_min': (10, 1500),
            'illuminance_max': (100, 3000),
            'illuminance_maintained': (50, 2000),
            'illuminance_initial': (50, 2000),
            'uniformity': (0.1, 1.0),
            'uniformity_ratio': (0.1, 1.0),
            'uniformity_min_max': (0.1, 1.0),
            'ugr': (5, 30),
            'glare_index': (5, 30),
            'glare_rating': (5, 30),
            'power_density': (1, 50),
            'power_total': (10, 10000),
            'luminous_efficacy': (50, 200),
            'energy_efficiency': (50, 100),
            'color_temperature': (2000, 6500),
            'color_rendering_index': (50, 100),
            'daylight_factor': (0, 10),
            'daylight_autonomy': (0, 100),
            'mounting_height': (1, 10)
        }
        
        if param_name in reasonable_ranges:
            min_val, max_val = reasonable_ranges[param_name]
            return min_val <= value <= max_val
        
        return True
    
    def create_comprehensive_rooms(self, lighting_data: List[Dict[str, Any]]) -> List[ComprehensiveRoom]:
        """Create comprehensive room objects with ALL parameters"""
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
        
        print(f"🏠 Creating comprehensive rooms from {len(room_groups)} room groups")
        
        # Create comprehensive room objects
        for room_name, room_data in room_groups.items():
            try:
                # Create room with all parameters
                room = ComprehensiveRoom(
                    name=room_name,
                    area=room_data.get('area', 0.0),
                    
                    # Illuminance parameters
                    illuminance_avg=room_data.get('illuminance_avg', 0.0),
                    illuminance_min=room_data.get('illuminance_min', 0.0),
                    illuminance_max=room_data.get('illuminance_max', 0.0),
                    illuminance_maintained=room_data.get('illuminance_maintained', 0.0),
                    illuminance_initial=room_data.get('illuminance_initial', 0.0),
                    
                    # Uniformity parameters
                    uniformity=room_data.get('uniformity', 0.0),
                    uniformity_ratio=room_data.get('uniformity_ratio', 0.0),
                    uniformity_min_max=room_data.get('uniformity_min_max', 0.0),
                    
                    # Glare parameters
                    ugr=room_data.get('ugr', 0.0),
                    glare_index=room_data.get('glare_index', 0.0),
                    glare_rating=room_data.get('glare_rating', 0.0),
                    
                    # Power and efficiency
                    power_density=room_data.get('power_density', 0.0),
                    power_total=room_data.get('power_total', 0.0),
                    luminous_efficacy=room_data.get('luminous_efficacy', 0.0),
                    energy_efficiency=room_data.get('energy_efficiency', 0.0),
                    
                    # Color parameters
                    color_temperature=room_data.get('color_temperature', 0.0),
                    color_rendering_index=room_data.get('color_rendering_index', 0.0),
                    color_quality=room_data.get('color_quality', 'Unknown'),
                    
                    # Additional parameters
                    daylight_factor=room_data.get('daylight_factor', 0.0),
                    daylight_autonomy=room_data.get('daylight_autonomy', 0.0),
                    light_distribution=room_data.get('light_distribution', 'Unknown'),
                    luminaire_type=room_data.get('luminaire_type', 'Unknown'),
                    mounting_height=room_data.get('mounting_height', 0.0),
                    
                    # Compliance flags (will be calculated)
                    illuminance_compliant=False,
                    uniformity_compliant=False,
                    glare_compliant=False,
                    power_compliant=False
                )
                
                # Calculate compliance
                room = self._calculate_compliance(room)
                
                rooms.append(room)
                print(f"✅ Created comprehensive room: {room_name}")
                print(f"   📊 Parameters: {len(room_data)}")
                print(f"   💡 Illuminance: {room.illuminance_avg} lux")
                print(f"   📐 Area: {room.area} m²")
                print(f"   ⚡ Power: {room.power_density} W/m²")
                print(f"   🎨 CRI: {room.color_rendering_index}")
                print(f"   🌡️  Color Temp: {room.color_temperature}K")
                
            except Exception as e:
                print(f"❌ Error creating room {room_name}: {e}")
        
        return rooms
    
    def _calculate_compliance(self, room: ComprehensiveRoom) -> ComprehensiveRoom:
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
    
    def process_comprehensive_dialux_pdf(self, pdf_path: Path) -> Optional[ComprehensiveReport]:
        """Process a Dialux PDF with comprehensive analysis"""
        try:
            print(f"🔍 Comprehensive processing of Dialux PDF: {pdf_path.name}")
            
            # Extract text
            text = self.extract_text_from_pdf(pdf_path)
            if not text.strip():
                print("❌ No text extracted from PDF")
                return None
            
            print(f"📄 Extracted {len(text)} characters of text")
            
            # Extract project name
            project_name = self.extract_project_name(text)
            print(f"🏢 Project: {project_name}")
            
            # Extract comprehensive data
            lighting_data = self.extract_comprehensive_data(text)
            print(f"📊 Found {len(lighting_data)} data points")
            
            if not lighting_data:
                print("❌ No lighting data found")
                return None
            
            # Create comprehensive rooms
            rooms = self.create_comprehensive_rooms(lighting_data)
            print(f"🏠 Created {len(rooms)} comprehensive rooms")
            
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
            
            # Determine project type
            project_type = self._determine_project_type(rooms)
            
            # Get applicable standards
            applicable_standards = list(self.standards_database.keys())
            standards_compliance = {
                standard: self._calculate_standard_compliance(rooms, standard) 
                for standard in applicable_standards
            }
            
            # Create comprehensive report
            report = ComprehensiveReport(
                project_name=project_name,
                project_type=project_type,
                total_rooms=len(rooms),
                total_area=total_area,
                overall_illuminance_avg=overall_illuminance_avg,
                overall_uniformity_avg=overall_uniformity_avg,
                overall_ugr_avg=overall_ugr_avg,
                overall_power_density_avg=overall_power_density_avg,
                illuminance_compliance_rate=illuminance_compliance_rate,
                uniformity_compliance_rate=uniformity_compliance_rate,
                glare_compliance_rate=glare_compliance_rate,
                power_compliance_rate=power_compliance_rate,
                overall_compliance_rate=overall_compliance_rate,
                rooms=rooms,
                applicable_standards=applicable_standards,
                standards_compliance=standards_compliance
            )
            
            print(f"✅ Successfully created comprehensive report with {len(rooms)} rooms")
            return report
            
        except Exception as e:
            print(f"❌ Error processing PDF: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _determine_project_type(self, rooms: List[ComprehensiveRoom]) -> str:
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
    
    def _calculate_standard_compliance(self, rooms: List[ComprehensiveRoom], standard_name: str) -> float:
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

def test_comprehensive_processor():
    """Test the comprehensive processor"""
    processor = ComprehensiveDialuxProcessor()
    
    # Test with existing PDFs
    test_files = [
        "src/base/EN_12464-1.pdf",
        "src/base/prEN 12464-1.pdf"
    ]
    
    for test_file in test_files:
        pdf_path = Path(test_file)
        if pdf_path.exists():
            print(f"\n🧪 Testing comprehensive processor with: {pdf_path.name}")
            result = processor.process_comprehensive_dialux_pdf(pdf_path)
            if result:
                print(f"✅ Success: {result.total_rooms} rooms, {result.total_area:.1f} m²")
                print(f"📊 Project Type: {result.project_type}")
                print(f"✅ Overall Compliance: {result.overall_compliance_rate:.1%}")
                print(f"💡 Average Illuminance: {result.overall_illuminance_avg:.1f} lux")
                print(f"⚡ Average Power Density: {result.overall_power_density_avg:.1f} W/m²")
                
                print(f"\n🏠 Room Details:")
                for room in result.rooms[:3]:  # Show first 3 rooms
                    print(f"   {room.name}:")
                    print(f"     💡 Illuminance: {room.illuminance_avg} lux")
                    print(f"     📐 Area: {room.area} m²")
                    print(f"     ⚡ Power: {room.power_density} W/m²")
                    print(f"     🎨 CRI: {room.color_rendering_index}")
                    print(f"     🌡️  Color Temp: {room.color_temperature}K")
                    print(f"     ✅ Compliant: I:{room.illuminance_compliant} U:{room.uniformity_compliant} G:{room.glare_compliant} P:{room.power_compliant}")
            else:
                print("❌ Failed to process")

if __name__ == "__main__":
    test_comprehensive_processor()
