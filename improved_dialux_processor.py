#!/usr/bin/env python3
"""
Improved Dialux PDF Processor
Enhanced processing for various Dialux report formats with better data extraction
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

class ImprovedDialuxProcessor:
    """Enhanced processor for Dialux PDF reports with better data extraction"""
    
    def __init__(self):
        # More comprehensive patterns for different Dialux formats
        self.room_patterns = {
            'name': [
                r'Room[:\s]*([^\n\r]+)',
                r'Space[:\s]*([^\n\r]+)',
                r'Area[:\s]*([^\n\r]+)',
                r'Zone[:\s]*([^\n\r]+)',
                r'([A-Za-z\s]+)\s*\([^)]*\)',  # Room name in parentheses
                r'^([A-Za-z\s]+)$'  # Standalone room names
            ],
            'area': [
                r'Area[:\s]*(\d+(?:\.\d+)?)\s*m²',
                r'Size[:\s]*(\d+(?:\.\d+)?)\s*m²',
                r'(\d+(?:\.\d+)?)\s*m²',
                r'Area[:\s]*(\d+(?:\.\d+)?)',
                r'(\d+(?:\.\d+)?)\s*sqm'
            ],
            'illuminance_avg': [
                r'Average[:\s]*(\d+(?:\.\d+)?)\s*lux',
                r'Avg[:\s]*(\d+(?:\.\d+)?)\s*lux',
                r'Mean[:\s]*(\d+(?:\.\d+)?)\s*lux',
                r'Illuminance[:\s]*(\d+(?:\.\d+)?)\s*lux',
                r'E[:\s]*(\d+(?:\.\d+)?)\s*lux',
                r'(\d+(?:\.\d+)?)\s*lux\s*\(avg\)',
                r'(\d+(?:\.\d+)?)\s*lx'
            ],
            'illuminance_min': [
                r'Minimum[:\s]*(\d+(?:\.\d+)?)\s*lux',
                r'Min[:\s]*(\d+(?:\.\d+)?)\s*lux',
                r'(\d+(?:\.\d+)?)\s*lux\s*\(min\)',
                r'Lowest[:\s]*(\d+(?:\.\d+)?)\s*lux'
            ],
            'illuminance_max': [
                r'Maximum[:\s]*(\d+(?:\.\d+)?)\s*lux',
                r'Max[:\s]*(\d+(?:\.\d+)?)\s*lux',
                r'(\d+(?:\.\d+)?)\s*lux\s*\(max\)',
                r'Highest[:\s]*(\d+(?:\.\d+)?)\s*lux'
            ],
            'uniformity': [
                r'Uniformity[:\s]*(\d+(?:\.\d+)?)',
                r'Uniform[:\s]*(\d+(?:\.\d+)?)',
                r'U[:\s]*(\d+(?:\.\d+)?)',
                r'(\d+(?:\.\d+)?)\s*\(uniformity\)'
            ],
            'ugr': [
                r'UGR[:\s]*(\d+(?:\.\d+)?)',
                r'Glare[:\s]*(\d+(?:\.\d+)?)',
                r'(\d+(?:\.\d+)?)\s*\(UGR\)',
                r'(\d+(?:\.\d+)?)\s*\(glare\)'
            ],
            'power_density': [
                r'Power\s+Density[:\s]*(\d+(?:\.\d+)?)\s*W/m²',
                r'Density[:\s]*(\d+(?:\.\d+)?)\s*W/m²',
                r'(\d+(?:\.\d+)?)\s*W/m²',
                r'(\d+(?:\.\d+)?)\s*Watt/m²',
                r'Power[:\s]*(\d+(?:\.\d+)?)\s*W/m²'
            ]
        }
        
        # Patterns for project information
        self.project_patterns = [
            r'Project[:\s]*([^\n\r]+)',
            r'Title[:\s]*([^\n\r]+)',
            r'Name[:\s]*([^\n\r]+)',
            r'Building[:\s]*([^\n\r]+)',
            r'File[:\s]*([^\n\r]+)',
            r'Report[:\s]*([^\n\r]+)'
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
        
        # Try pdfminer as last resort
        if not text:
            try:
                from pdfminer.high_level import extract_text
                text = extract_text(pdf_path)
                print(f"✅ Extracted {len(text)} characters using pdfminer")
            except Exception as e:
                print(f"pdfminer failed: {e}")
        
        return text
    
    def extract_project_name(self, text: str) -> str:
        """Extract project name from text"""
        for pattern in self.project_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                if len(name) > 3:  # Avoid very short matches
                    return name
        
        # Fallback: use first line or filename
        lines = text.split('\n')
        for line in lines[:10]:  # Check first 10 lines
            line = line.strip()
            if len(line) > 5 and not line.isdigit():
                return line
        
        return "Unknown Project"
    
    def extract_lighting_data(self, text: str) -> List[Dict[str, Any]]:
        """Extract lighting data from text using multiple approaches"""
        data_points = []
        
        # Method 1: Look for structured data patterns
        structured_data = self._extract_structured_data(text)
        data_points.extend(structured_data)
        
        # Method 2: Look for table-like data
        table_data = self._extract_table_data(text)
        data_points.extend(table_data)
        
        # Method 3: Look for scattered values
        scattered_data = self._extract_scattered_data(text)
        data_points.extend(scattered_data)
        
        return data_points
    
    def _extract_structured_data(self, text: str) -> List[Dict[str, Any]]:
        """Extract data from structured sections"""
        data_points = []
        
        # Look for sections that might contain room data
        sections = re.split(r'\n\s*\n', text)
        
        for section in sections:
            if len(section.strip()) < 20:  # Skip very short sections
                continue
            
            # Look for numeric values in the section
            numbers = re.findall(r'\d+(?:\.\d+)?', section)
            if len(numbers) >= 3:  # Likely to contain lighting data
                data_point = self._parse_section_data(section, numbers)
                if data_point:
                    data_points.append(data_point)
        
        return data_points
    
    def _extract_table_data(self, text: str) -> List[Dict[str, Any]]:
        """Extract data from table-like structures"""
        data_points = []
        
        # Look for lines that contain multiple numeric values
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            # Check if line contains multiple numbers (likely a data row)
            numbers = re.findall(r'\d+(?:\.\d+)?', line)
            if len(numbers) >= 3:
                # Try to extract context from surrounding lines
                context_lines = lines[max(0, i-2):i+3]
                data_point = self._parse_table_row(line, context_lines)
                if data_point:
                    data_points.append(data_point)
        
        return data_points
    
    def _extract_scattered_data(self, text: str) -> List[Dict[str, Any]]:
        """Extract scattered lighting values from text"""
        data_points = []
        
        # Extract all potential lighting values
        for param_name, patterns in self.room_patterns.items():
            if param_name == 'name':  # Skip name patterns
                continue
                
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    try:
                        value = float(match.group(1))
                        data_points.append({
                            'parameter': param_name,
                            'value': value,
                            'context': match.group(0),
                            'position': match.start()
                        })
                    except (ValueError, IndexError):
                        continue
        
        return data_points
    
    def _parse_section_data(self, section: str, numbers: List[str]) -> Optional[Dict[str, Any]]:
        """Parse data from a text section"""
        try:
            # Try to identify what each number represents
            data = {}
            
            # Look for parameter names near numbers
            for param_name, patterns in self.room_patterns.items():
                if param_name == 'name':
                    continue
                    
                for pattern in patterns:
                    match = re.search(pattern, section, re.IGNORECASE)
                    if match:
                        try:
                            value = float(match.group(1))
                            data[param_name] = value
                        except (ValueError, IndexError):
                            continue
            
            # If we found at least 2 parameters, this is likely valid data
            if len(data) >= 2:
                # Try to extract room name
                name_match = re.search(r'([A-Za-z\s]+)', section)
                if name_match:
                    data['name'] = name_match.group(1).strip()
                else:
                    data['name'] = f"Room {len(data_points) + 1}"
                
                return data
        
        except Exception as e:
            print(f"Error parsing section: {e}")
        
        return None
    
    def _parse_table_row(self, row: str, context_lines: List[str]) -> Optional[Dict[str, Any]]:
        """Parse data from a table row"""
        try:
            # Extract numbers from the row
            numbers = re.findall(r'\d+(?:\.\d+)?', row)
            if len(numbers) < 2:
                return None
            
            # Try to map numbers to parameters based on context
            data = {}
            
            # Look for parameter indicators in context
            context_text = ' '.join(context_lines)
            
            for param_name, patterns in self.room_patterns.items():
                if param_name == 'name':
                    continue
                    
                for pattern in patterns:
                    if re.search(pattern, context_text, re.IGNORECASE):
                        # Find the corresponding number
                        for num_str in numbers:
                            try:
                                value = float(num_str)
                                if self._is_reasonable_value(param_name, value):
                                    data[param_name] = value
                                    break
                            except ValueError:
                                continue
            
            if len(data) >= 2:
                # Extract room name
                name_match = re.search(r'([A-Za-z\s]+)', row)
                if name_match:
                    data['name'] = name_match.group(1).strip()
                else:
                    data['name'] = f"Room {len(data_points) + 1}"
                
                return data
        
        except Exception as e:
            print(f"Error parsing table row: {e}")
        
        return None
    
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
    
    def create_rooms_from_data(self, lighting_data: List[Dict[str, Any]]) -> List[DialuxRoom]:
        """Create DialuxRoom objects from extracted data"""
        rooms = []
        
        # Group data by room name
        room_groups = {}
        for data_point in lighting_data:
            if 'name' in data_point:
                room_name = data_point['name']
                if room_name not in room_groups:
                    room_groups[room_name] = {}
                room_groups[room_name].update(data_point)
        
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
            except Exception as e:
                print(f"Error creating room {room_name}: {e}")
        
        return rooms
    
    def process_dialux_pdf(self, pdf_path: Path) -> Optional[DialuxReport]:
        """Process a Dialux PDF report with improved extraction"""
        try:
            print(f"🔍 Processing Dialux PDF: {pdf_path.name}")
            
            # Extract text
            text = self.extract_text_from_pdf(pdf_path)
            if not text.strip():
                print("❌ No text extracted from PDF")
                return None
            
            print(f"📄 Extracted {len(text)} characters of text")
            
            # Extract project name
            project_name = self.extract_project_name(text)
            print(f"🏢 Project: {project_name}")
            
            # Extract lighting data
            lighting_data = self.extract_lighting_data(text)
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

def test_processor():
    """Test the improved processor"""
    processor = ImprovedDialuxProcessor()
    
    # Test with existing PDFs
    test_files = [
        "src/base/EN_12464-1.pdf",
        "src/base/prEN 12464-1.pdf",
        "src/base/ODLI20150723_001-UPD-en_AA-Lighting-for-BREEAM-in-offices.pdf"
    ]
    
    for test_file in test_files:
        pdf_path = Path(test_file)
        if pdf_path.exists():
            print(f"\n🧪 Testing with: {pdf_path.name}")
            result = processor.process_dialux_pdf(pdf_path)
            if result:
                print(f"✅ Success: {len(result.rooms)} rooms, {result.total_area:.1f} m²")
            else:
                print("❌ Failed to process")

if __name__ == "__main__":
    test_processor()
