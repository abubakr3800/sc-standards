"""
Dialux Report Processor
Specialized processor for Dialux lighting calculation reports
"""
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from loguru import logger

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

class DialuxProcessor:
    """Processes Dialux reports and extracts lighting data"""
    
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
    
    def extract_project_name(self, text: str) -> str:
        """Extract project name from Dialux report"""
        patterns = [
            r'Project[:\s]*([^\n\r]+)',
            r'Title[:\s]*([^\n\r]+)',
            r'Name[:\s]*([^\n\r]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return "Unknown Project"
    
    def extract_room_data(self, text: str) -> List[DialuxRoom]:
        """Extract room data from Dialux report"""
        rooms = []
        
        # Split text into sections (look for room separators)
        room_sections = re.split(r'(?i)(?:room|space|area)[:\s]*', text)
        
        for i, section in enumerate(room_sections[1:], 1):  # Skip first empty section
            try:
                room_data = {}
                
                # Extract room name (first line or from context)
                name_match = re.search(r'^([^\n\r]+)', section.strip())
                room_data['name'] = name_match.group(1).strip() if name_match else f"Room {i}"
                
                # Extract numerical data
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
                logger.warning(f"Failed to parse room section {i}: {e}")
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
    
    def process_dialux_report(self, file_path: Path) -> Optional[DialuxReport]:
        """Process a Dialux report file"""
        try:
            logger.info(f"Processing Dialux report: {file_path.name}")
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            
            # Extract project name
            project_name = self.extract_project_name(text)
            
            # Extract room data
            rooms = self.extract_room_data(text)
            
            if not rooms:
                logger.warning("No room data found in Dialux report")
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
            
            logger.info(f"Successfully processed Dialux report with {len(rooms)} rooms")
            return report
            
        except Exception as e:
            logger.error(f"Failed to process Dialux report {file_path.name}: {e}")
            return None
    
    def export_to_json(self, report: DialuxReport, output_path: Path):
        """Export Dialux report to JSON format"""
        try:
            data = {
                'project_name': report.project_name,
                'total_area': report.total_area,
                'total_power': report.total_power,
                'average_power_density': report.average_power_density,
                'overall_uniformity': report.overall_uniformity,
                'worst_ugr': report.worst_ugr,
                'rooms': [
                    {
                        'name': room.name,
                        'area': room.area,
                        'illuminance_avg': room.illuminance_avg,
                        'illuminance_min': room.illuminance_min,
                        'illuminance_max': room.illuminance_max,
                        'uniformity': room.uniformity,
                        'ugr': room.ugr,
                        'power_density': room.power_density
                    }
                    for room in report.rooms
                ]
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Exported Dialux report to {output_path}")
            
        except Exception as e:
            logger.error(f"Failed to export Dialux report: {e}")
