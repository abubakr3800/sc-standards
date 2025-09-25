#!/usr/bin/env python3
"""
Focused Dialux PDF Processor
Consolidates data properly and focuses on actual room spaces with complete data
"""
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class FocusedRoom:
    """Focused room data with consolidated parameters"""
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
class FocusedReport:
    """Focused Dialux report with consolidated analysis"""
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
    rooms: List[FocusedRoom]
    
    # Standards analysis
    applicable_standards: List[str]
    best_matching_standard: str
    standards_compliance: Dict[str, float]

class FocusedDialuxProcessor:
    """Focused processor that consolidates data and focuses on actual rooms"""
    
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
    
    def extract_focused_data(self, text: str) -> List[Dict[str, Any]]:
        """Extract and consolidate lighting data focusing on actual rooms"""
        print("🎯 Starting focused data extraction...")
        
        # Look for table-like structures first (most reliable)
        table_data = self._extract_table_data(text)
        print(f"📊 Table extraction found {len(table_data)} data points")
        
        # Look for structured sections
        section_data = self._extract_structured_sections(text)
        print(f"📋 Section extraction found {len(section_data)} data points")
        
        # Combine and consolidate data
        all_data = table_data + section_data
        consolidated_data = self._consolidate_data(all_data)
        print(f"🔄 After consolidation: {len(consolidated_data)} consolidated data points")
        
        return consolidated_data
    
    def _extract_table_data(self, text: str) -> List[Dict[str, Any]]:
        """Extract data from table-like structures"""
        data_points = []
        lines = text.split('\n')
        
        # Look for lines that look like table rows
        for i, line in enumerate(lines):
            line = line.strip()
            if len(line) < 10:
                continue
            
            # Check if line contains multiple numbers (likely a data row)
            numbers = re.findall(r'\d+(?:\.\d+)?', line)
            if len(numbers) >= 3:  # At least 3 numbers suggests a data row
                # Get context from surrounding lines
                context_start = max(0, i-2)
                context_end = min(len(lines), i+3)
                context = '\n'.join(lines[context_start:context_end])
                
                data_point = self._parse_table_row(line, context, numbers)
                if data_point:
                    data_points.append(data_point)
        
        return data_points
    
    def _extract_structured_sections(self, text: str) -> List[Dict[str, Any]]:
        """Extract data from structured sections"""
        data_points = []
        
        # Split text into sections
        sections = re.split(r'\n\s*\n', text)
        
        for section in sections:
            if len(section.strip()) < 50:  # Skip very short sections
                continue
            
            # Check if section contains lighting data
            if self._is_lighting_section(section):
                data_point = self._parse_section(section)
                if data_point:
                    data_points.append(data_point)
        
        return data_points
    
    def _parse_table_row(self, row: str, context: str, numbers: List[str]) -> Optional[Dict[str, Any]]:
        """Parse a table row with context"""
        try:
            data = {}
            
            # Extract room name from context
            room_name = self._extract_room_name_from_context(context)
            if room_name:
                data['room_name'] = room_name
            
            # Map numbers to parameters based on context and position
            param_mapping = self._map_numbers_to_parameters(numbers, context)
            data.update(param_mapping)
            
            # Validate data - must have at least room name and 2 parameters
            if len(data) >= 3:
                return data
        
        except Exception as e:
            print(f"Error parsing table row: {e}")
        
        return None
    
    def _parse_section(self, section: str) -> Optional[Dict[str, Any]]:
        """Parse a text section for lighting data"""
        try:
            data = {}
            
            # Extract room name
            room_name = self._extract_room_name_from_section(section)
            if room_name:
                data['room_name'] = room_name
            
            # Extract parameters using patterns
            for param_name, patterns in self.core_patterns.items():
                for pattern in patterns:
                    match = re.search(pattern, section, re.IGNORECASE)
                    if match:
                        try:
                            value = float(match.group(1))
                            if self._is_reasonable_value(param_name, value):
                                data[param_name] = value
                                break
                        except (ValueError, IndexError):
                            continue
            
            # Validate data - must have at least room name and 2 parameters
            if len(data) >= 3:
                return data
        
        except Exception as e:
            print(f"Error parsing section: {e}")
        
        return None
    
    def _extract_room_name_from_context(self, context: str) -> Optional[str]:
        """Extract room name from context"""
        # Look for room names in the context
        room_patterns = [
            r'(?:room|space|area|zone|office|meeting|conference|reception|corridor|hall|kitchen|toilet|storage|workshop|factory|retail|shop|display|classroom|laboratory|library|gym|restaurant|cafeteria|auditorium|theater|museum|gallery|warehouse|garage|parking)[:\s]*([^\n\r\d]+?)(?:\s*\d|\s*\(|\s*$)',
            r'([A-Za-z\s]+?)(?:\s*\d+(?:\.\d+)?\s*(?:m²|m2|lux|lx|w/m²))',
            r'([A-Za-z\s]+?)(?:\s*:|\s*$)',
            r'^([A-Za-z\s]+?)(?:\s*\d)'
        ]
        
        for pattern in room_patterns:
            match = re.search(pattern, context, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                if len(name) > 2 and not name.isdigit():
                    # Clean up the name
                    name = re.sub(r'[^\w\s-]', '', name).strip()
                    if len(name) > 2:
                        return name
        
        return None
    
    def _extract_room_name_from_section(self, section: str) -> Optional[str]:
        """Extract room name from section"""
        # Look for room names in the section
        room_patterns = [
            r'(?:room|space|area|zone|office|meeting|conference|reception|corridor|hall|kitchen|toilet|storage|workshop|factory|retail|shop|display|classroom|laboratory|library|gym|restaurant|cafeteria|auditorium|theater|museum|gallery|warehouse|garage|parking)[:\s]*([^\n\r\d]+?)(?:\s*\d|\s*\(|\s*$)',
            r'([A-Za-z\s]+?)(?:\s*\d+(?:\.\d+)?\s*(?:m²|m2|lux|lx|w/m²))',
            r'([A-Za-z\s]+?)(?:\s*:|\s*$)',
            r'^([A-Za-z\s]+?)(?:\s*\d)'
        ]
        
        for pattern in room_patterns:
            match = re.search(pattern, section, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                if len(name) > 2 and not name.isdigit():
                    # Clean up the name
                    name = re.sub(r'[^\w\s-]', '', name).strip()
                    if len(name) > 2:
                        return name
        
        return None
    
    def _map_numbers_to_parameters(self, numbers: List[str], context: str) -> Dict[str, float]:
        """Map numbers to parameters based on context"""
        mapping = {}
        
        # Look for parameter indicators in context
        for param_name, patterns in self.core_patterns.items():
            for pattern in patterns:
                if re.search(pattern, context, re.IGNORECASE):
                    # Find the corresponding number
                    for num_str in numbers:
                        try:
                            value = float(num_str)
                            if self._is_reasonable_value(param_name, value):
                                mapping[param_name] = value
                                break
                        except ValueError:
                            continue
        
        return mapping
    
    def _is_lighting_section(self, section: str) -> bool:
        """Check if a section contains lighting data"""
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
    
    def _consolidate_data(self, data_points: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Consolidate data points by room name"""
        consolidated = {}
        
        for data_point in data_points:
            room_name = data_point.get('room_name', 'Unknown Room')
            
            if room_name not in consolidated:
                consolidated[room_name] = {}
            
            # Add parameters to the room
            for key, value in data_point.items():
                if key != 'room_name' and value is not None:
                    consolidated[room_name][key] = value
        
        # Convert back to list
        result = []
        for room_name, room_data in consolidated.items():
            if room_data:  # Only include rooms with data
                room_data['room_name'] = room_name
                result.append(room_data)
        
        return result
    
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
    
    def create_focused_rooms(self, lighting_data: List[Dict[str, Any]]) -> List[FocusedRoom]:
        """Create focused room objects with consolidated data"""
        rooms = []
        
        print(f"🏠 Creating focused rooms from {len(lighting_data)} consolidated data points")
        
        for room_data in lighting_data:
            try:
                room_name = room_data.get('room_name', 'Unknown Room')
                
                # Calculate data completeness
                core_params = ['illuminance_avg', 'uniformity', 'ugr', 'power_density', 'area']
                available_params = [p for p in core_params if p in room_data and room_data[p] > 0]
                data_completeness = len(available_params) / len(core_params)
                
                # Calculate confidence score based on data quality
                confidence_score = self._calculate_confidence_score(room_data)
                
                # Only create rooms with meaningful data
                if data_completeness > 0.3:  # At least 30% of core parameters
                    room = FocusedRoom(
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
                    
                    rooms.append(room)
                    print(f"✅ Created focused room: {room_name}")
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
    
    def _calculate_compliance(self, room: FocusedRoom) -> FocusedRoom:
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
    
    def process_focused_dialux_pdf(self, pdf_path: Path) -> Optional[FocusedReport]:
        """Process a Dialux PDF with focused analysis"""
        try:
            print(f"🎯 Focused processing of Dialux PDF: {pdf_path.name}")
            
            # Extract text
            text = self.extract_text_from_pdf(pdf_path)
            if not text.strip():
                print("❌ No text extracted from PDF")
                return None
            
            print(f"📄 Extracted {len(text)} characters of text")
            
            # Extract project name
            project_name = self.extract_project_name(text)
            print(f"🏢 Project: {project_name}")
            
            # Extract focused data
            lighting_data = self.extract_focused_data(text)
            print(f"📊 Found {len(lighting_data)} consolidated data points")
            
            if not lighting_data:
                print("❌ No lighting data found")
                return None
            
            # Create focused rooms
            rooms = self.create_focused_rooms(lighting_data)
            print(f"🏠 Created {len(rooms)} focused rooms")
            
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
            
            # Create focused report
            report = FocusedReport(
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
            
            print(f"✅ Successfully created focused report with {len(rooms)} rooms")
            return report
            
        except Exception as e:
            print(f"❌ Error processing PDF: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _determine_project_type(self, rooms: List[FocusedRoom]) -> str:
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
    
    def _calculate_standard_compliance(self, rooms: List[FocusedRoom], standard_name: str) -> float:
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

def test_focused_processor():
    """Test the focused processor"""
    processor = FocusedDialuxProcessor()
    
    # Test with existing PDFs
    test_files = [
        "src/base/EN_12464-1.pdf",
        "src/base/prEN 12464-1.pdf"
    ]
    
    for test_file in test_files:
        pdf_path = Path(test_file)
        if pdf_path.exists():
            print(f"\n🧪 Testing focused processor with: {pdf_path.name}")
            result = processor.process_focused_dialux_pdf(pdf_path)
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
    test_focused_processor()

