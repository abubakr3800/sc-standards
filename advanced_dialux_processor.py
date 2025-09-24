#!/usr/bin/env python3
"""
Advanced Dialux PDF Processor
Highly accurate extraction for various Dialux report formats
"""
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
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

class AdvancedDialuxProcessor:
    """Advanced processor with highly accurate Dialux data extraction"""
    
    def __init__(self):
        # Comprehensive patterns for different Dialux formats
        self.patterns = {
            # Illuminance patterns - very comprehensive
            'illuminance_avg': [
                r'(?:average|avg|mean|e\s*avg|e\s*average)[:\s]*(\d+(?:\.\d+)?)\s*(?:lux|lx)',
                r'(\d+(?:\.\d+)?)\s*(?:lux|lx)\s*(?:average|avg|mean)',
                r'illuminance[:\s]*(\d+(?:\.\d+)?)\s*(?:lux|lx)',
                r'e[:\s]*(\d+(?:\.\d+)?)\s*(?:lux|lx)',
                r'(\d+(?:\.\d+)?)\s*(?:lux|lx)(?:\s*\(avg\))?',
                r'em[:\s]*(\d+(?:\.\d+)?)\s*(?:lux|lx)',
                r'(\d+(?:\.\d+)?)\s*(?:lux|lx)\s*\(em\)',
                r'(\d+(?:\.\d+)?)\s*(?:lux|lx)\s*\(mean\)'
            ],
            
            'illuminance_min': [
                r'(?:minimum|min|e\s*min|e\s*minimum)[:\s]*(\d+(?:\.\d+)?)\s*(?:lux|lx)',
                r'(\d+(?:\.\d+)?)\s*(?:lux|lx)\s*(?:minimum|min)',
                r'(\d+(?:\.\d+)?)\s*(?:lux|lx)\s*\(min\)',
                r'(\d+(?:\.\d+)?)\s*(?:lux|lx)\s*\(minimum\)'
            ],
            
            'illuminance_max': [
                r'(?:maximum|max|e\s*max|e\s*maximum)[:\s]*(\d+(?:\.\d+)?)\s*(?:lux|lx)',
                r'(\d+(?:\.\d+)?)\s*(?:lux|lx)\s*(?:maximum|max)',
                r'(\d+(?:\.\d+)?)\s*(?:lux|lx)\s*\(max\)',
                r'(\d+(?:\.\d+)?)\s*(?:lux|lx)\s*\(maximum\)'
            ],
            
            # Uniformity patterns
            'uniformity': [
                r'(?:uniformity|uniform|u0|u\s*0)[:\s]*(\d+(?:\.\d+)?)',
                r'(\d+(?:\.\d+)?)\s*(?:uniformity|uniform)',
                r'(\d+(?:\.\d+)?)\s*\(uniformity\)',
                r'(\d+(?:\.\d+)?)\s*\(uniform\)',
                r'u0[:\s]*(\d+(?:\.\d+)?)',
                r'(\d+(?:\.\d+)?)\s*\(u0\)'
            ],
            
            # UGR patterns
            'ugr': [
                r'(?:ugr|glare|u\s*g\s*r)[:\s]*(\d+(?:\.\d+)?)',
                r'(\d+(?:\.\d+)?)\s*(?:ugr|glare)',
                r'(\d+(?:\.\d+)?)\s*\(ugr\)',
                r'(\d+(?:\.\d+)?)\s*\(glare\)',
                r'ugr[:\s]*(\d+(?:\.\d+)?)',
                r'glare[:\s]*(\d+(?:\.\d+)?)'
            ],
            
            # Area patterns
            'area': [
                r'(?:area|size|surface)[:\s]*(\d+(?:\.\d+)?)\s*(?:m²|m2|sqm|m\^2)',
                r'(\d+(?:\.\d+)?)\s*(?:m²|m2|sqm|m\^2)',
                r'(\d+(?:\.\d+)?)\s*(?:m²|m2|sqm|m\^2)\s*(?:area|size)',
                r'(\d+(?:\.\d+)?)\s*(?:m²|m2|sqm|m\^2)\s*\(area\)'
            ],
            
            # Power density patterns
            'power_density': [
                r'(?:power\s+density|density|p\s*density)[:\s]*(\d+(?:\.\d+)?)\s*(?:w/m²|w/m2|watt/m²|watt/m2)',
                r'(\d+(?:\.\d+)?)\s*(?:w/m²|w/m2|watt/m²|watt/m2)',
                r'(\d+(?:\.\d+)?)\s*(?:w/m²|w/m2|watt/m²|watt/m2)\s*(?:power|density)',
                r'(\d+(?:\.\d+)?)\s*(?:w/m²|w/m2|watt/m²|watt/m2)\s*\(power\)',
                r'power[:\s]*(\d+(?:\.\d+)?)\s*(?:w/m²|w/m2|watt/m²|watt/m2)'
            ],
            
            # Room name patterns
            'room_name': [
                r'(?:room|space|area|zone)[:\s]*([^\n\r\d]+?)(?:\s*\d|\s*\(|\s*$)',
                r'([A-Za-z\s]+?)(?:\s*\d+(?:\.\d+)?\s*(?:m²|m2|lux|lx|w/m²))',
                r'([A-Za-z\s]+?)(?:\s*\([^)]*\))?\s*(?:\d+(?:\.\d+)?)',
                r'^([A-Za-z\s]+?)(?:\s*\d)',
                r'([A-Za-z\s]+?)(?:\s*:|\s*$)'
            ]
        }
        
        # Context patterns to identify data sections
        self.context_patterns = [
            r'room\s+\d+',
            r'area\s+\d+',
            r'zone\s+\d+',
            r'space\s+\d+',
            r'illuminance',
            r'lighting',
            r'calculation',
            r'result',
            r'summary'
        ]
    
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
        # Look for project information in first few lines
        lines = text.split('\n')[:20]
        
        for line in lines:
            line = line.strip()
            if len(line) > 5 and not line.isdigit():
                # Skip common non-project words
                skip_words = ['page', 'date', 'time', 'version', 'dialux', 'report', 'calculation']
                if not any(word in line.lower() for word in skip_words):
                    return line
        
        return "Unknown Project"
    
    def extract_lighting_data_advanced(self, text: str) -> List[Dict[str, Any]]:
        """Advanced extraction using multiple strategies"""
        print("🔍 Starting advanced data extraction...")
        
        # Strategy 1: Table-based extraction
        table_data = self._extract_table_data(text)
        print(f"📊 Table extraction found {len(table_data)} data points")
        
        # Strategy 2: Section-based extraction
        section_data = self._extract_section_data(text)
        print(f"📋 Section extraction found {len(section_data)} data points")
        
        # Strategy 3: Line-by-line extraction
        line_data = self._extract_line_data(text)
        print(f"📝 Line extraction found {len(line_data)} data points")
        
        # Strategy 4: Pattern-based extraction
        pattern_data = self._extract_pattern_data(text)
        print(f"🎯 Pattern extraction found {len(pattern_data)} data points")
        
        # Combine and deduplicate
        all_data = table_data + section_data + line_data + pattern_data
        unique_data = self._deduplicate_data(all_data)
        print(f"🔄 After deduplication: {len(unique_data)} unique data points")
        
        return unique_data
    
    def _extract_table_data(self, text: str) -> List[Dict[str, Any]]:
        """Extract data from table-like structures"""
        data_points = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            # Look for lines with multiple numbers (likely table rows)
            numbers = re.findall(r'\d+(?:\.\d+)?', line)
            if len(numbers) >= 3:  # Likely a data row
                # Get context from surrounding lines
                context_start = max(0, i-3)
                context_end = min(len(lines), i+4)
                context = '\n'.join(lines[context_start:context_end])
                
                data_point = self._parse_table_row(line, context, numbers)
                if data_point:
                    data_points.append(data_point)
        
        return data_points
    
    def _extract_section_data(self, text: str) -> List[Dict[str, Any]]:
        """Extract data from structured sections"""
        data_points = []
        
        # Split text into sections
        sections = re.split(r'\n\s*\n', text)
        
        for section in sections:
            if len(section.strip()) < 30:  # Skip very short sections
                continue
            
            # Check if section contains lighting data
            if self._is_lighting_section(section):
                data_point = self._parse_section(section)
                if data_point:
                    data_points.append(data_point)
        
        return data_points
    
    def _extract_line_data(self, text: str) -> List[Dict[str, Any]]:
        """Extract data line by line"""
        data_points = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if len(line) < 10:  # Skip very short lines
                continue
            
            # Look for lines with lighting data
            data_point = self._parse_line(line)
            if data_point:
                data_points.append(data_point)
        
        return data_points
    
    def _extract_pattern_data(self, text: str) -> List[Dict[str, Any]]:
        """Extract data using comprehensive pattern matching"""
        data_points = []
        
        for param_name, patterns in self.patterns.items():
            if param_name == 'room_name':
                continue
                
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    try:
                        value = float(match.group(1))
                        if self._is_reasonable_value(param_name, value):
                            # Try to find room context
                            room_name = self._find_room_context(text, match.start())
                            
                            data_point = {
                                'parameter': param_name,
                                'value': value,
                                'room_name': room_name,
                                'context': match.group(0),
                                'position': match.start()
                            }
                            data_points.append(data_point)
                    except (ValueError, IndexError):
                        continue
        
        return data_points
    
    def _parse_table_row(self, row: str, context: str, numbers: List[str]) -> Optional[Dict[str, Any]]:
        """Parse a table row with context"""
        try:
            data = {}
            
            # Extract room name
            room_name = self._extract_room_name_from_context(context)
            if room_name:
                data['room_name'] = room_name
            
            # Map numbers to parameters based on context and position
            param_mapping = self._map_numbers_to_parameters(numbers, context)
            data.update(param_mapping)
            
            # Validate data
            if len(data) >= 3:  # At least room name + 2 parameters
                return data
        
        except Exception as e:
            print(f"Error parsing table row: {e}")
        
        return None
    
    def _parse_section(self, section: str) -> Optional[Dict[str, Any]]:
        """Parse a text section for lighting data"""
        try:
            data = {}
            
            # Extract room name
            room_name = self._extract_room_name_from_context(section)
            if room_name:
                data['room_name'] = room_name
            
            # Extract parameters using patterns
            for param_name, patterns in self.patterns.items():
                if param_name == 'room_name':
                    continue
                    
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
            
            # Validate data
            if len(data) >= 3:  # At least room name + 2 parameters
                return data
        
        except Exception as e:
            print(f"Error parsing section: {e}")
        
        return None
    
    def _parse_line(self, line: str) -> Optional[Dict[str, Any]]:
        """Parse a single line for lighting data"""
        try:
            data = {}
            
            # Extract room name
            room_name = self._extract_room_name_from_context(line)
            if room_name:
                data['room_name'] = room_name
            
            # Extract parameters
            for param_name, patterns in self.patterns.items():
                if param_name == 'room_name':
                    continue
                    
                for pattern in patterns:
                    match = re.search(pattern, line, re.IGNORECASE)
                    if match:
                        try:
                            value = float(match.group(1))
                            if self._is_reasonable_value(param_name, value):
                                data[param_name] = value
                                break
                        except (ValueError, IndexError):
                            continue
            
            # Validate data
            if len(data) >= 2:  # At least 2 parameters
                return data
        
        except Exception as e:
            print(f"Error parsing line: {e}")
        
        return None
    
    def _extract_room_name_from_context(self, context: str) -> Optional[str]:
        """Extract room name from context"""
        for pattern in self.patterns['room_name']:
            match = re.search(pattern, context, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                if len(name) > 2 and not name.isdigit():
                    return name
        
        return None
    
    def _map_numbers_to_parameters(self, numbers: List[str], context: str) -> Dict[str, float]:
        """Map numbers to parameters based on context"""
        mapping = {}
        
        # Look for parameter indicators in context
        for param_name, patterns in self.patterns.items():
            if param_name == 'room_name':
                continue
                
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
            'power', 'density', 'area', 'room', 'space', 'zone'
        ]
        
        section_lower = section.lower()
        keyword_count = sum(1 for keyword in lighting_keywords if keyword in section_lower)
        
        # Look for numbers (likely lighting values)
        numbers = re.findall(r'\d+(?:\.\d+)?', section)
        
        return keyword_count >= 2 and len(numbers) >= 2
    
    def _find_room_context(self, text: str, position: int) -> str:
        """Find room context around a position in text"""
        # Look for room name in surrounding text
        start = max(0, position - 200)
        end = min(len(text), position + 200)
        context = text[start:end]
        
        room_name = self._extract_room_name_from_context(context)
        return room_name or "Unknown Room"
    
    def _is_reasonable_value(self, param_name: str, value: float) -> bool:
        """Check if a value is reasonable for a given parameter"""
        reasonable_ranges = {
            'area': (1, 10000),  # 1 to 10,000 m²
            'illuminance_avg': (50, 2000),  # 50 to 2000 lux
            'illuminance_min': (10, 1500),  # 10 to 1500 lux
            'illuminance_max': (100, 3000),  # 100 to 3000 lux
            'uniformity': (0.1, 1.0),  # 0.1 to 1.0
            'ugr': (5, 30),  # 5 to 30 UGR
            'power_density': (1, 50)  # 1 to 50 W/m²
        }
        
        if param_name in reasonable_ranges:
            min_val, max_val = reasonable_ranges[param_name]
            return min_val <= value <= max_val
        
        return True
    
    def _deduplicate_data(self, data_points: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate data points"""
        unique_data = []
        seen = set()
        
        for data_point in data_points:
            # Create a key for deduplication
            key = (
                data_point.get('room_name', ''),
                data_point.get('parameter', ''),
                data_point.get('value', 0)
            )
            
            if key not in seen:
                seen.add(key)
                unique_data.append(data_point)
        
        return unique_data
    
    def create_rooms_from_data(self, lighting_data: List[Dict[str, Any]]) -> List[DialuxRoom]:
        """Create DialuxRoom objects from extracted data"""
        rooms = []
        
        # Group data by room name
        room_groups = {}
        for data_point in lighting_data:
            room_name = data_point.get('room_name', 'Unknown Room')
            if room_name not in room_groups:
                room_groups[room_name] = {}
            
            param_name = data_point.get('parameter')
            value = data_point.get('value')
            if param_name and value is not None:
                room_groups[room_name][param_name] = value
        
        # Create room objects
        for room_name, room_data in room_groups.items():
            try:
                room = DialuxRoom(
                    name=room_name,
                    area=room_data.get('area', 0.0),
                    illuminance_avg=room_data.get('illuminance_avg', 0.0),
                    illuminance_min=room_data.get('illuminance_min', 0.0),
                    illuminance_max=room_data.get('illuminance_max', 0.0),
                    uniformity=room_data.get('uniformity', 0.0),
                    ugr=room_data.get('ugr', 0.0),
                    power_density=room_data.get('power_density', 0.0)
                )
                rooms.append(room)
                print(f"✅ Created room: {room_name} with {len(room_data)} parameters")
            except Exception as e:
                print(f"Error creating room {room_name}: {e}")
        
        return rooms
    
    def process_dialux_pdf(self, pdf_path: Path) -> Optional[DialuxReport]:
        """Process a Dialux PDF report with advanced extraction"""
        try:
            print(f"🔍 Advanced processing of Dialux PDF: {pdf_path.name}")
            
            # Extract text
            text = self.extract_text_from_pdf(pdf_path)
            if not text.strip():
                print("❌ No text extracted from PDF")
                return None
            
            print(f"📄 Extracted {len(text)} characters of text")
            
            # Extract project name
            project_name = self.extract_project_name(text)
            print(f"🏢 Project: {project_name}")
            
            # Extract lighting data using advanced methods
            lighting_data = self.extract_lighting_data_advanced(text)
            print(f"📊 Found {len(lighting_data)} data points")
            
            if not lighting_data:
                print("❌ No lighting data found")
                return None
            
            # Create rooms from data
            rooms = self.create_rooms_from_data(lighting_data)
            print(f"🏠 Created {len(rooms)} rooms")
            
            if not rooms:
                print("❌ No rooms could be created from data")
                return None
            
            # Calculate summary statistics
            total_area = sum(room.area for room in rooms)
            total_power = sum(room.area * room.power_density for room in rooms)
            average_power_density = total_power / total_area if total_area > 0 else 0
            overall_uniformity = sum(room.uniformity for room in rooms) / len(rooms) if rooms else 0
            worst_ugr = max(room.ugr for room in rooms) if rooms else 0
            
            # Create report
            report = DialuxReport(
                project_name=project_name,
                rooms=rooms,
                total_area=total_area,
                total_power=total_power,
                average_power_density=average_power_density,
                overall_uniformity=overall_uniformity,
                worst_ugr=worst_ugr
            )
            
            print(f"✅ Successfully processed Dialux report with {len(rooms)} rooms")
            return report
            
        except Exception as e:
            print(f"❌ Error processing PDF: {e}")
            import traceback
            traceback.print_exc()
            return None

def test_advanced_processor():
    """Test the advanced processor"""
    processor = AdvancedDialuxProcessor()
    
    # Test with existing PDFs
    test_files = [
        "src/base/EN_12464-1.pdf",
        "src/base/prEN 12464-1.pdf"
    ]
    
    for test_file in test_files:
        pdf_path = Path(test_file)
        if pdf_path.exists():
            print(f"\n🧪 Testing advanced processor with: {pdf_path.name}")
            result = processor.process_dialux_pdf(pdf_path)
            if result:
                print(f"✅ Success: {len(result.rooms)} rooms, {result.total_area:.1f} m²")
                for room in result.rooms:
                    print(f"   Room: {room.name}")
                    print(f"     Area: {room.area} m²")
                    print(f"     Illuminance: {room.illuminance_avg} lux")
                    print(f"     Uniformity: {room.uniformity}")
                    print(f"     UGR: {room.ugr}")
            else:
                print("❌ Failed to process")

if __name__ == "__main__":
    test_advanced_processor()
