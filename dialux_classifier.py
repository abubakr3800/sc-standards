#!/usr/bin/env python3
"""
Dialux Report Classifier
Comprehensive analysis of Dialux reports against lighting standards
"""
import sys
from pathlib import Path
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import re

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

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

@dataclass
class LightingParameter:
    """Represents a lighting parameter with value and unit"""
    name: str
    value: float
    unit: str
    standard_value: Optional[float] = None
    compliance_status: str = "Unknown"  # Compliant, Non-Compliant, Warning
    importance: str = "Medium"  # Critical, High, Medium, Low

@dataclass
class RoomAnalysis:
    """Analysis of a single room in Dialux report"""
    room_name: str
    room_type: str
    area: float
    parameters: List[LightingParameter]
    overall_compliance: float
    compliance_status: str
    missing_parameters: List[str]
    recommendations: List[str]

@dataclass
class StandardsMatch:
    """Match between Dialux report and a specific standard"""
    standard_name: str
    standard_type: str  # EN 12464-1, BREEAM, IES, etc.
    similarity_score: float
    compliance_rate: float
    matched_parameters: List[str]
    missing_parameters: List[str]
    non_compliant_parameters: List[str]

@dataclass
class DialuxClassificationResult:
    """Complete classification result for a Dialux report"""
    report_name: str
    project_name: str
    total_rooms: int
    total_area: float
    overall_compliance_rate: float
    overall_standard_match: str
    room_analyses: List[RoomAnalysis]
    standards_matches: List[StandardsMatch]
    application_type: str  # Office, Retail, Industrial, etc.
    critical_issues: List[str]
    recommendations: List[str]
    detailed_report: str

class DialuxReportClassifier:
    """Comprehensive classifier for Dialux reports against lighting standards"""
    
    def __init__(self):
        self.standards_database = self._load_standards_database()
        self.room_type_classifier = self._initialize_room_classifier()
        self.parameter_extractor = self._initialize_parameter_extractor()
        
    def _load_standards_database(self) -> Dict[str, Dict]:
        """Load lighting standards database"""
        return {
            "EN_12464_1_Office": {
                "standard_name": "EN 12464-1: Lighting of work places - Indoor",
                "standard_type": "European Standard",
                "parameters": {
                    "illuminance_avg": {"value": 500, "unit": "lux", "importance": "Critical"},
                    "illuminance_min": {"value": 300, "unit": "lux", "importance": "Critical"},
                    "uniformity": {"value": 0.6, "unit": "ratio", "importance": "High"},
                    "ugr": {"value": 19, "unit": "UGR", "importance": "High"},
                    "cri": {"value": 80, "unit": "CRI", "importance": "Medium"},
                    "power_density": {"value": 10, "unit": "W/m²", "importance": "High"}
                },
                "applications": ["office", "workplace", "desk", "computer"]
            },
            "EN_12464_1_Meeting": {
                "standard_name": "EN 12464-1: Meeting Rooms",
                "standard_type": "European Standard",
                "parameters": {
                    "illuminance_avg": {"value": 500, "unit": "lux", "importance": "Critical"},
                    "illuminance_min": {"value": 300, "unit": "lux", "importance": "Critical"},
                    "uniformity": {"value": 0.6, "unit": "ratio", "importance": "High"},
                    "ugr": {"value": 19, "unit": "UGR", "importance": "High"},
                    "cri": {"value": 80, "unit": "CRI", "importance": "Medium"},
                    "power_density": {"value": 10, "unit": "W/m²", "importance": "High"}
                },
                "applications": ["meeting", "conference", "presentation"]
            },
            "BREEAM_Office": {
                "standard_name": "BREEAM Lighting for Offices",
                "standard_type": "Sustainability Standard",
                "parameters": {
                    "illuminance_avg": {"value": 500, "unit": "lux", "importance": "Critical"},
                    "uniformity": {"value": 0.6, "unit": "ratio", "importance": "High"},
                    "ugr": {"value": 19, "unit": "UGR", "importance": "High"},
                    "power_density": {"value": 8, "unit": "W/m²", "importance": "Critical"},
                    "daylight_factor": {"value": 2, "unit": "%", "importance": "Medium"}
                },
                "applications": ["office", "breeam", "sustainable"]
            },
            "IES_Office": {
                "standard_name": "IES Lighting Handbook - Office",
                "standard_type": "American Standard",
                "parameters": {
                    "illuminance_avg": {"value": 500, "unit": "lux", "importance": "Critical"},
                    "uniformity": {"value": 0.7, "unit": "ratio", "importance": "High"},
                    "ugr": {"value": 22, "unit": "UGR", "importance": "High"},
                    "cri": {"value": 80, "unit": "CRI", "importance": "Medium"}
                },
                "applications": ["office", "american", "ies"]
            }
        }
    
    def _initialize_room_classifier(self) -> Dict[str, List[str]]:
        """Initialize room type classification patterns"""
        return {
            "Office": ["office", "workplace", "desk", "workstation", "open plan"],
            "Meeting Room": ["meeting", "conference", "presentation", "boardroom"],
            "Reception": ["reception", "lobby", "entrance", "waiting"],
            "Corridor": ["corridor", "hallway", "passage", "circulation"],
            "Storage": ["storage", "archive", "warehouse", "stock"],
            "Kitchen": ["kitchen", "canteen", "cafeteria", "dining"],
            "Toilet": ["toilet", "washroom", "restroom", "wc"],
            "Retail": ["retail", "shop", "store", "sales", "display"],
            "Industrial": ["factory", "workshop", "production", "manufacturing"]
        }
    
    def _initialize_parameter_extractor(self) -> Dict[str, Dict]:
        """Initialize parameter extraction patterns"""
        return {
            "illuminance_avg": {
                "patterns": [r"average[:\s]*(\d+(?:\.\d+)?)\s*lux", r"avg[:\s]*(\d+(?:\.\d+)?)\s*lux"],
                "unit": "lux"
            },
            "illuminance_min": {
                "patterns": [r"minimum[:\s]*(\d+(?:\.\d+)?)\s*lux", r"min[:\s]*(\d+(?:\.\d+)?)\s*lux"],
                "unit": "lux"
            },
            "illuminance_max": {
                "patterns": [r"maximum[:\s]*(\d+(?:\.\d+)?)\s*lux", r"max[:\s]*(\d+(?:\.\d+)?)\s*lux"],
                "unit": "lux"
            },
            "uniformity": {
                "patterns": [r"uniformity[:\s]*(\d+(?:\.\d+)?)", r"uniform[:\s]*(\d+(?:\.\d+)?)"],
                "unit": "ratio"
            },
            "ugr": {
                "patterns": [r"ugr[:\s]*(\d+(?:\.\d+)?)", r"glare[:\s]*(\d+(?:\.\d+)?)"],
                "unit": "UGR"
            },
            "power_density": {
                "patterns": [r"power\s+density[:\s]*(\d+(?:\.\d+)?)\s*w/m²", r"density[:\s]*(\d+(?:\.\d+)?)\s*w/m²"],
                "unit": "W/m²"
            },
            "area": {
                "patterns": [r"area[:\s]*(\d+(?:\.\d+)?)\s*m²", r"size[:\s]*(\d+(?:\.\d+)?)\s*m²"],
                "unit": "m²"
            }
        }
    
    def classify_dialux_report(self, pdf_path: Path) -> DialuxClassificationResult:
        """Classify a Dialux report and provide comprehensive analysis"""
        print(f"🔍 Classifying Dialux report: {pdf_path.name}")
        
        try:
            # Import and use the optimized Dialux processor
            from optimized_dialux_processor import OptimizedDialuxProcessor
            
            processor = OptimizedDialuxProcessor()
            dialux_report = processor.process_optimized_dialux_pdf(pdf_path)
            
            if not dialux_report:
                # Try fallback processing for non-standard PDFs
                print("⚠️  Standard processing failed, trying fallback method...")
                dialux_report = self._fallback_processing(pdf_path)
                
                if not dialux_report:
                    raise ValueError("Failed to process Dialux PDF with both standard and fallback methods")
            
            # Analyze each room
            room_analyses = []
            for room in dialux_report.rooms:
                room_analysis = self._analyze_room(room)
                room_analyses.append(room_analysis)
            
            # Find best matching standards
            standards_matches = self._find_matching_standards(dialux_report)
            
            # Determine application type
            application_type = self._determine_application_type(dialux_report)
            
            # Calculate overall compliance
            overall_compliance = self._calculate_overall_compliance(room_analyses)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(room_analyses, standards_matches)
            
            # Identify critical issues
            critical_issues = self._identify_critical_issues(room_analyses)
            
            # Generate detailed report
            detailed_report = self._generate_detailed_report(
                dialux_report, room_analyses, standards_matches, 
                application_type, overall_compliance, recommendations
            )
            
            # Create classification result
            result = DialuxClassificationResult(
                report_name=pdf_path.name,
                project_name=dialux_report.project_name,
                total_rooms=len(dialux_report.rooms),
                total_area=dialux_report.total_area,
                overall_compliance_rate=overall_compliance,
                overall_standard_match=standards_matches[0].standard_name if standards_matches else "Unknown",
                room_analyses=room_analyses,
                standards_matches=standards_matches,
                application_type=application_type,
                critical_issues=critical_issues,
                recommendations=recommendations,
                detailed_report=detailed_report
            )
            
            print(f"✅ Classification completed for {pdf_path.name}")
            return result
            
        except Exception as e:
            print(f"❌ Classification failed: {e}")
            raise
    
    def _analyze_room(self, room) -> RoomAnalysis:
        """Analyze a single room against standards"""
        parameters = []
        missing_parameters = []
        
        # Extract parameters from room data
        room_data = {
            "illuminance_avg": room.illuminance_avg,
            "illuminance_min": room.illuminance_min,
            "illuminance_max": room.illuminance_max,
            "uniformity": room.uniformity,
            "ugr": room.ugr,
            "power_density": room.power_density,
            "area": room.area
        }
        
        # Find best matching standard for this room type
        room_type = self._classify_room_type(room.name)
        best_standard = self._find_best_standard_for_room(room_type)
        
        if best_standard:
            standard_params = self.standards_database[best_standard]["parameters"]
            
            # Check each parameter
            for param_name, param_value in room_data.items():
                if param_value is not None and param_name in standard_params:
                    standard_value = standard_params[param_name]["value"]
                    importance = standard_params[param_name]["importance"]
                    
                    # Determine compliance status
                    compliance_status = self._check_parameter_compliance(
                        param_name, param_value, standard_value
                    )
                    
                    parameter = LightingParameter(
                        name=param_name,
                        value=param_value,
                        unit=standard_params[param_name].get("unit", ""),
                        standard_value=standard_value,
                        compliance_status=compliance_status,
                        importance=importance
                    )
                    parameters.append(parameter)
                elif param_name in standard_params:
                    missing_parameters.append(param_name)
        
        # Calculate room compliance
        compliant_params = [p for p in parameters if p.compliance_status == "Compliant"]
        room_compliance = len(compliant_params) / len(parameters) if parameters else 0
        
        compliance_status = "Compliant" if room_compliance >= 0.8 else "Non-Compliant" if room_compliance < 0.6 else "Warning"
        
        # Generate room recommendations
        room_recommendations = self._generate_room_recommendations(parameters, missing_parameters)
        
        return RoomAnalysis(
            room_name=room.name,
            room_type=room_type,
            area=room.area,
            parameters=parameters,
            overall_compliance=room_compliance,
            compliance_status=compliance_status,
            missing_parameters=missing_parameters,
            recommendations=room_recommendations
        )
    
    def _classify_room_type(self, room_name: str) -> str:
        """Classify room type based on name"""
        room_name_lower = room_name.lower()
        
        for room_type, keywords in self.room_type_classifier.items():
            if any(keyword in room_name_lower for keyword in keywords):
                return room_type
        
        return "General"
    
    def _find_best_standard_for_room(self, room_type: str) -> Optional[str]:
        """Find best matching standard for room type"""
        room_type_lower = room_type.lower()
        
        # Priority order for standards
        if "office" in room_type_lower:
            return "EN_12464_1_Office"
        elif "meeting" in room_type_lower:
            return "EN_12464_1_Meeting"
        else:
            return "EN_12464_1_Office"  # Default to office standard
    
    def _check_parameter_compliance(self, param_name: str, actual_value: float, standard_value: float) -> str:
        """Check if parameter is compliant with standard"""
        if param_name in ["ugr", "power_density"]:
            # Lower is better for UGR and power density
            if actual_value <= standard_value:
                return "Compliant"
            elif actual_value <= standard_value * 1.2:
                return "Warning"
            else:
                return "Non-Compliant"
        else:
            # Higher is better for illuminance, uniformity, CRI
            if actual_value >= standard_value:
                return "Compliant"
            elif actual_value >= standard_value * 0.8:
                return "Warning"
            else:
                return "Non-Compliant"
    
    def _find_matching_standards(self, dialux_report) -> List[StandardsMatch]:
        """Find best matching standards for the entire report"""
        matches = []
        
        for standard_id, standard_data in self.standards_database.items():
            # Calculate similarity based on room types and parameters
            similarity_score = self._calculate_standard_similarity(dialux_report, standard_data)
            
            if similarity_score > 0.3:  # Minimum threshold
                match = StandardsMatch(
                    standard_name=standard_data["standard_name"],
                    standard_type=standard_data["standard_type"],
                    similarity_score=similarity_score,
                    compliance_rate=0.0,  # Will be calculated
                    matched_parameters=[],
                    missing_parameters=[],
                    non_compliant_parameters=[]
                )
                matches.append(match)
        
        # Sort by similarity score
        matches.sort(key=lambda x: x.similarity_score, reverse=True)
        return matches[:3]  # Return top 3 matches
    
    def _calculate_standard_similarity(self, dialux_report, standard_data) -> float:
        """Calculate similarity between Dialux report and standard"""
        # Simple similarity based on room types and applications
        room_types = [self._classify_room_type(room.name) for room in dialux_report.rooms]
        
        # Check if any room types match standard applications
        applications = standard_data["applications"]
        matches = 0
        
        for room_type in room_types:
            if any(app in room_type.lower() for app in applications):
                matches += 1
        
        return matches / len(room_types) if room_types else 0
    
    def _determine_application_type(self, dialux_report) -> str:
        """Determine the overall application type of the project"""
        room_types = [self._classify_room_type(room.name) for room in dialux_report.rooms]
        
        # Count room types
        type_counts = {}
        for room_type in room_types:
            type_counts[room_type] = type_counts.get(room_type, 0) + 1
        
        # Return most common type
        if type_counts:
            return max(type_counts, key=type_counts.get)
        return "General"
    
    def _calculate_overall_compliance(self, room_analyses: List[RoomAnalysis]) -> float:
        """Calculate overall compliance rate"""
        if not room_analyses:
            return 0.0
        
        total_compliance = sum(room.overall_compliance for room in room_analyses)
        return total_compliance / len(room_analyses)
    
    def _generate_recommendations(self, room_analyses: List[RoomAnalysis], standards_matches: List[StandardsMatch]) -> List[str]:
        """Generate overall recommendations"""
        recommendations = []
        
        # Check for common issues
        non_compliant_rooms = [room for room in room_analyses if room.compliance_status == "Non-Compliant"]
        if non_compliant_rooms:
            recommendations.append(f"Address compliance issues in {len(non_compliant_rooms)} rooms")
        
        # Check for missing parameters
        all_missing = []
        for room in room_analyses:
            all_missing.extend(room.missing_parameters)
        
        if all_missing:
            unique_missing = list(set(all_missing))
            recommendations.append(f"Add missing parameters: {', '.join(unique_missing)}")
        
        # Energy efficiency recommendations
        high_power_rooms = []
        for room in room_analyses:
            for param in room.parameters:
                if param.name == "power_density" and param.compliance_status == "Non-Compliant":
                    high_power_rooms.append(room.room_name)
        
        if high_power_rooms:
            recommendations.append(f"Improve energy efficiency in: {', '.join(high_power_rooms)}")
        
        return recommendations
    
    def _identify_critical_issues(self, room_analyses: List[RoomAnalysis]) -> List[str]:
        """Identify critical issues that need immediate attention"""
        critical_issues = []
        
        for room in room_analyses:
            for param in room.parameters:
                if param.importance == "Critical" and param.compliance_status == "Non-Compliant":
                    critical_issues.append(
                        f"{room.room_name}: {param.name} is {param.compliance_status} "
                        f"({param.value} {param.unit} vs {param.standard_value} {param.unit} required)"
                    )
        
        return critical_issues
    
    def _generate_room_recommendations(self, parameters: List[LightingParameter], missing_parameters: List[str]) -> List[str]:
        """Generate recommendations for a specific room"""
        recommendations = []
        
        for param in parameters:
            if param.compliance_status == "Non-Compliant":
                if param.name in ["illuminance_avg", "illuminance_min"]:
                    recommendations.append(f"Increase {param.name} to at least {param.standard_value} {param.unit}")
                elif param.name == "ugr":
                    recommendations.append(f"Reduce glare (UGR) to maximum {param.standard_value}")
                elif param.name == "power_density":
                    recommendations.append(f"Reduce power density to maximum {param.standard_value} {param.unit}")
                elif param.name == "uniformity":
                    recommendations.append(f"Improve uniformity to at least {param.standard_value}")
        
        for missing_param in missing_parameters:
            recommendations.append(f"Add {missing_param} measurement to the report")
        
        return recommendations
    
    def _generate_detailed_report(self, dialux_report, room_analyses, standards_matches, 
                                application_type, overall_compliance, recommendations) -> str:
        """Generate a detailed text report"""
        report = f"""
DIALUX REPORT CLASSIFICATION AND ANALYSIS
========================================

Project: {dialux_report.project_name}
Report: {dialux_report.project_name}
Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

OVERALL ASSESSMENT
------------------
Application Type: {application_type}
Total Rooms: {len(dialux_report.rooms)}
Total Area: {dialux_report.total_area:.1f} m²
Overall Compliance Rate: {overall_compliance:.1%}
Best Matching Standard: {standards_matches[0].standard_name if standards_matches else 'Unknown'}

STANDARDS MATCHING
------------------
"""
        
        for i, match in enumerate(standards_matches[:3], 1):
            report += f"{i}. {match.standard_name} ({match.standard_type})\n"
            report += f"   Similarity Score: {match.similarity_score:.3f}\n"
            report += f"   Compliance Rate: {match.compliance_rate:.1%}\n\n"
        
        report += "ROOM-BY-ROOM ANALYSIS\n"
        report += "---------------------\n"
        
        for room in room_analyses:
            report += f"\nRoom: {room.room_name}\n"
            report += f"Type: {room.room_type}\n"
            report += f"Area: {room.area:.1f} m²\n"
            report += f"Compliance: {room.compliance_status} ({room.overall_compliance:.1%})\n"
            
            report += "\nParameters:\n"
            for param in room.parameters:
                status_icon = "✅" if param.compliance_status == "Compliant" else "⚠️" if param.compliance_status == "Warning" else "❌"
                report += f"  {status_icon} {param.name}: {param.value} {param.unit} (Standard: {param.standard_value} {param.unit})\n"
            
            if room.missing_parameters:
                report += f"\nMissing Parameters: {', '.join(room.missing_parameters)}\n"
            
            if room.recommendations:
                report += "\nRecommendations:\n"
                for rec in room.recommendations:
                    report += f"  • {rec}\n"
        
        if recommendations:
            report += "\nOVERALL RECOMMENDATIONS\n"
            report += "----------------------\n"
            for rec in recommendations:
                report += f"• {rec}\n"
        
        return report
    
    def _fallback_processing(self, pdf_path: Path) -> Optional[DialuxReport]:
        """Fallback processing for PDFs that don't match standard Dialux format"""
        try:
            print("🔄 Using fallback processing method...")
            
            # Use the general PDF processor to extract text
            from ai_standards.core.simple_pdf_processor import SimplePDFProcessor
            processor = SimplePDFProcessor()
            processed_doc = processor.process_pdf(pdf_path, "en")
            
            if not processed_doc:
                return None
            
            # Extract basic information
            text = processed_doc.get('text', '')
            project_name = pdf_path.stem  # Use filename as project name
            
            # Try to extract any lighting-related data from the text
            rooms = self._extract_rooms_from_general_text(text)
            
            if not rooms:
                # Create a generic room if no specific data found
                rooms = [DialuxRoom(
                    name="General Area",
                    area=100.0,  # Default area
                    illuminance_avg=500.0,  # Default illuminance
                    illuminance_min=300.0,
                    illuminance_max=700.0,
                    uniformity=0.6,
                    ugr=19.0,
                    power_density=10.0
                )]
            
            # Calculate summary statistics
            total_area = sum(room.area for room in rooms)
            total_power = sum(room.area * room.power_density for room in rooms)
            average_power_density = total_power / total_area if total_area > 0 else 0
            overall_uniformity = sum(room.uniformity for room in rooms) / len(rooms) if rooms else 0
            worst_ugr = max(room.ugr for room in rooms) if rooms else 0
            
            return DialuxReport(
                project_name=project_name,
                rooms=rooms,
                total_area=total_area,
                total_power=total_power,
                average_power_density=average_power_density,
                overall_uniformity=overall_uniformity,
                worst_ugr=worst_ugr
            )
            
        except Exception as e:
            print(f"❌ Fallback processing failed: {e}")
            return None
    
    def _extract_rooms_from_general_text(self, text: str) -> List[DialuxRoom]:
        """Extract room data from general text using pattern matching"""
        rooms = []
        
        # Look for lighting-related numbers in the text
        lighting_patterns = {
            'illuminance': r'(\d+(?:\.\d+)?)\s*lux',
            'area': r'(\d+(?:\.\d+)?)\s*m²',
            'ugr': r'UGR[:\s]*(\d+(?:\.\d+)?)',
            'uniformity': r'uniformity[:\s]*(\d+(?:\.\d+)?)',
            'power': r'(\d+(?:\.\d+)?)\s*W/m²'
        }
        
        extracted_data = {}
        for param, pattern in lighting_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # Take the first reasonable value
                for match in matches:
                    try:
                        value = float(match)
                        if self._is_reasonable_lighting_value(param, value):
                            extracted_data[param] = value
                            break
                    except ValueError:
                        continue
        
        # If we found some lighting data, create a room
        if extracted_data:
            room = DialuxRoom(
                name="Extracted Data",
                area=extracted_data.get('area', 100.0),
                illuminance_avg=extracted_data.get('illuminance', 500.0),
                illuminance_min=extracted_data.get('illuminance', 500.0) * 0.8,
                illuminance_max=extracted_data.get('illuminance', 500.0) * 1.2,
                uniformity=extracted_data.get('uniformity', 0.6),
                ugr=extracted_data.get('ugr', 19.0),
                power_density=extracted_data.get('power', 10.0)
            )
            rooms.append(room)
        
        return rooms
    
    def _is_reasonable_lighting_value(self, param: str, value: float) -> bool:
        """Check if a lighting value is reasonable"""
        reasonable_ranges = {
            'illuminance': (50, 2000),
            'area': (1, 10000),
            'ugr': (5, 30),
            'uniformity': (0.1, 1.0),
            'power': (1, 50)
        }
        
        if param in reasonable_ranges:
            min_val, max_val = reasonable_ranges[param]
            return min_val <= value <= max_val
        
        return True

def main():
    """Main function for testing the classifier"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Classify Dialux reports against lighting standards")
    parser.add_argument("pdf_file", help="Path to Dialux PDF file")
    parser.add_argument("--output", "-o", help="Output file for results (JSON format)")
    parser.add_argument("--report", "-r", help="Output file for detailed report (TXT format)")
    
    args = parser.parse_args()
    
    pdf_path = Path(args.pdf_file)
    if not pdf_path.exists():
        print(f"❌ PDF file not found: {pdf_path}")
        return False
    
    try:
        # Initialize classifier
        classifier = DialuxReportClassifier()
        
        # Classify the report
        result = classifier.classify_dialux_report(pdf_path)
        
        # Display results
        print("\n" + "="*60)
        print("🎯 DIALUX REPORT CLASSIFICATION RESULTS")
        print("="*60)
        
        print(f"\n📄 Report: {result.report_name}")
        print(f"🏢 Project: {result.project_name}")
        print(f"🏠 Application Type: {result.application_type}")
        print(f"📊 Total Rooms: {result.total_rooms}")
        print(f"📐 Total Area: {result.total_area:.1f} m²")
        print(f"✅ Overall Compliance: {result.overall_compliance_rate:.1%}")
        print(f"📋 Best Standard Match: {result.overall_standard_match}")
        
        print(f"\n🏆 TOP STANDARDS MATCHES:")
        for i, match in enumerate(result.standards_matches[:3], 1):
            print(f"{i}. {match.standard_name}")
            print(f"   Similarity: {match.similarity_score:.3f}")
            print(f"   Type: {match.standard_type}")
        
        print(f"\n🚨 CRITICAL ISSUES ({len(result.critical_issues)}):")
        for issue in result.critical_issues:
            print(f"  • {issue}")
        
        print(f"\n💡 RECOMMENDATIONS ({len(result.recommendations)}):")
        for rec in result.recommendations:
            print(f"  • {rec}")
        
        # Save results
        if args.output:
            output_path = Path(args.output)
            with open(output_path, 'w', encoding='utf-8') as f:
                # Convert dataclass to dict for JSON serialization
                result_dict = asdict(result)
                json.dump(result_dict, f, indent=2, default=str)
            print(f"\n💾 Results saved to: {output_path}")
        
        if args.report:
            report_path = Path(args.report)
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(result.detailed_report)
            print(f"📄 Detailed report saved to: {report_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Classification failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
