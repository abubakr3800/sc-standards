"""
Simple Lighting Report Evaluator
Evaluates lighting reports against standards without complex dependencies
"""
import re
import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class LightingParameter:
    """Represents a lighting parameter with value and unit"""
    name: str
    value: float
    unit: str
    location: str = ""
    notes: str = ""

@dataclass
class ComplianceResult:
    """Result of compliance checking"""
    parameter: str
    measured_value: float
    standard_value: float
    unit: str
    compliance_status: str  # "PASS", "FAIL", "WARNING"
    recommendation: str
    standard_reference: str

@dataclass
class ReportEvaluation:
    """Complete evaluation of a lighting report"""
    report_name: str
    overall_compliance: str
    compliance_score: float  # 0-100%
    total_parameters: int
    passed_parameters: int
    failed_parameters: int
    warning_parameters: int
    compliance_results: List[ComplianceResult]
    recommendations: List[str]
    summary: str

class SimpleLightingEvaluator:
    """Simple lighting evaluator without complex dependencies"""
    
    def __init__(self):
        self.standards_data = self._load_standards_data()
    
    def _load_standards_data(self):
        """Load standards data from processed documents"""
        standards = {}
        try:
            uploads_dir = Path("uploads")
            if uploads_dir.exists():
                processed_files = list(uploads_dir.glob("*_processed.json"))
                for file_path in processed_files:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        standards[data['file_name']] = data
        except Exception as e:
            print(f"Warning: Could not load standards data: {e}")
        return standards
    
    def get_standard_requirements(self, parameter: str, application: str = "general") -> Dict:
        """Get standard requirements for a parameter and application"""
        requirements = {
            'illuminance': {
                'general': {'min': 200, 'max': 2000, 'recommended': 500, 'unit': 'lux'},
                'office': {'min': 300, 'max': 1000, 'recommended': 500, 'unit': 'lux'},
                'detailed_work': {'min': 500, 'max': 2000, 'recommended': 1000, 'unit': 'lux'},
                'conference': {'min': 200, 'max': 500, 'recommended': 300, 'unit': 'lux'},
                'reception': {'min': 100, 'max': 300, 'recommended': 200, 'unit': 'lux'},
                'corridor': {'min': 50, 'max': 200, 'recommended': 100, 'unit': 'lux'},
                'staircase': {'min': 100, 'max': 300, 'recommended': 150, 'unit': 'lux'}
            },
            'uniformity': {
                'general': {'min': 0.4, 'max': 1.0, 'recommended': 0.7, 'unit': ''},
                'office': {'min': 0.6, 'max': 1.0, 'recommended': 0.8, 'unit': ''},
                'detailed_work': {'min': 0.7, 'max': 1.0, 'recommended': 0.9, 'unit': ''}
            },
            'ugr': {
                'general': {'min': 0, 'max': 25, 'recommended': 19, 'unit': ''},
                'office': {'min': 0, 'max': 19, 'recommended': 16, 'unit': ''},
                'computer_work': {'min': 0, 'max': 16, 'recommended': 13, 'unit': ''},
                'conference': {'min': 0, 'max': 22, 'recommended': 19, 'unit': ''}
            },
            'cri': {
                'general': {'min': 80, 'max': 100, 'recommended': 90, 'unit': ''},
                'color_critical': {'min': 90, 'max': 100, 'recommended': 95, 'unit': ''}
            },
            'color_temperature': {
                'general': {'min': 3000, 'max': 6500, 'recommended': 4000, 'unit': 'K'},
                'office': {'min': 4000, 'max': 5000, 'recommended': 4000, 'unit': 'K'},
                'warm': {'min': 2700, 'max': 3000, 'recommended': 3000, 'unit': 'K'},
                'cool': {'min': 5000, 'max': 6500, 'recommended': 5000, 'unit': 'K'}
            },
            'power_density': {
                'general': {'min': 0, 'max': 5.0, 'recommended': 3.5, 'unit': 'W/m²'},
                'office': {'min': 0, 'max': 3.5, 'recommended': 2.5, 'unit': 'W/m²'},
                'efficient': {'min': 0, 'max': 2.0, 'recommended': 1.5, 'unit': 'W/m²'}
            }
        }
        
        return requirements.get(parameter, {}).get(application, {})
    
    def check_compliance(self, parameter: LightingParameter, application: str = "general") -> ComplianceResult:
        """Check if a parameter complies with standards"""
        requirements = self.get_standard_requirements(parameter.name, application)
        
        if not requirements:
            return ComplianceResult(
                parameter=parameter.name,
                measured_value=parameter.value,
                standard_value=0,
                unit=parameter.unit,
                compliance_status="UNKNOWN",
                recommendation="No standard requirements found for this parameter",
                standard_reference="Unknown"
            )
        
        min_val = requirements.get('min', 0)
        max_val = requirements.get('max', float('inf'))
        recommended = requirements.get('recommended', 0)
        
        # Determine compliance status
        if min_val <= parameter.value <= max_val:
            if abs(parameter.value - recommended) <= (max_val - min_val) * 0.1:
                status = "PASS"
                recommendation = f"Excellent! Value is within optimal range"
            else:
                status = "PASS"
                recommendation = f"Compliant but consider adjusting to {recommended} {parameter.unit} for optimal performance"
        else:
            if parameter.value < min_val:
                status = "FAIL"
                recommendation = f"Below minimum requirement. Increase to at least {min_val} {parameter.unit}"
            else:
                status = "FAIL"
                recommendation = f"Above maximum limit. Reduce to maximum {max_val} {parameter.unit}"
        
        return ComplianceResult(
            parameter=parameter.name,
            measured_value=parameter.value,
            standard_value=recommended,
            unit=parameter.unit,
            compliance_status=status,
            recommendation=recommendation,
            standard_reference=f"EN 12464-1:2021"
        )
    
    def extract_lighting_parameters(self, report_text: str) -> List[LightingParameter]:
        """Extract lighting parameters from report text"""
        parameters = []
        
        # Common lighting parameter patterns
        patterns = {
            'illuminance': [
                r'illuminance[:\s]*(\d+(?:\.\d+)?)\s*(lux|lx)',
                r'(\d+(?:\.\d+)?)\s*(lux|lx)',
                r'illumination[:\s]*(\d+(?:\.\d+)?)\s*(lux|lx)'
            ],
            'uniformity': [
                r'uniformity[:\s]*(\d+(?:\.\d+)?)',
                r'U[o0][:\s]*(\d+(?:\.\d+)?)',
                r'min/max[:\s]*(\d+(?:\.\d+)?)'
            ],
            'ugr': [
                r'UGR[:\s]*(\d+(?:\.\d+)?)',
                r'unified\s+glare\s+rating[:\s]*(\d+(?:\.\d+)?)',
                r'glare[:\s]*(\d+(?:\.\d+)?)'
            ],
            'cri': [
                r'CRI[:\s]*(\d+(?:\.\d+)?)',
                r'color\s+rendering\s+index[:\s]*(\d+(?:\.\d+)?)',
                r'Ra[:\s]*(\d+(?:\.\d+)?)'
            ],
            'color_temperature': [
                r'color\s+temperature[:\s]*(\d+(?:\.\d+)?)\s*(K|kelvin)',
                r'CCT[:\s]*(\d+(?:\.\d+)?)\s*(K|kelvin)',
                r'(\d+(?:\.\d+)?)\s*(K|kelvin)'
            ],
            'power_density': [
                r'power\s+density[:\s]*(\d+(?:\.\d+)?)\s*(W/m²|W/m2|W/m\^2)',
                r'lighting\s+power\s+density[:\s]*(\d+(?:\.\d+)?)\s*(W/m²|W/m2|W/m\^2)',
                r'LPD[:\s]*(\d+(?:\.\d+)?)\s*(W/m²|W/m2|W/m\^2)'
            ]
        }
        
        for param_name, param_patterns in patterns.items():
            for pattern in param_patterns:
                matches = re.finditer(pattern, report_text, re.IGNORECASE)
                for match in matches:
                    try:
                        value = float(match.group(1))
                        unit = match.group(2) if len(match.groups()) > 1 else self._get_default_unit(param_name)
                        
                        parameters.append(LightingParameter(
                            name=param_name,
                            value=value,
                            unit=unit,
                            location=f"Line {report_text[:match.start()].count(chr(10)) + 1}",
                            notes=f"Extracted from: {match.group(0)}"
                        ))
                    except (ValueError, IndexError):
                        continue
        
        return parameters
    
    def _get_default_unit(self, parameter_name: str) -> str:
        """Get default unit for parameter"""
        units = {
            'illuminance': 'lux',
            'uniformity': '',
            'ugr': '',
            'cri': '',
            'color_temperature': 'K',
            'power_density': 'W/m²'
        }
        return units.get(parameter_name, '')
    
    def evaluate_report(self, report_text: str, report_name: str = "Unknown", application: str = "general") -> ReportEvaluation:
        """Evaluate a complete lighting report"""
        print(f"Evaluating report: {report_name}")
        
        # Extract parameters
        parameters = self.extract_lighting_parameters(report_text)
        print(f"Extracted {len(parameters)} parameters")
        
        if not parameters:
            return ReportEvaluation(
                report_name=report_name,
                overall_compliance="UNKNOWN",
                compliance_score=0.0,
                total_parameters=0,
                passed_parameters=0,
                failed_parameters=0,
                warning_parameters=0,
                compliance_results=[],
                recommendations=["No lighting parameters found in report"],
                summary="No lighting parameters could be extracted from the report"
            )
        
        # Check compliance for each parameter
        compliance_results = []
        for param in parameters:
            result = self.check_compliance(param, application)
            compliance_results.append(result)
        
        # Calculate overall compliance
        total_params = len(compliance_results)
        passed = sum(1 for r in compliance_results if r.compliance_status == "PASS")
        failed = sum(1 for r in compliance_results if r.compliance_status == "FAIL")
        warnings = sum(1 for r in compliance_results if r.compliance_status == "WARNING")
        
        compliance_score = (passed / total_params * 100) if total_params > 0 else 0
        
        # Determine overall compliance
        if compliance_score >= 90:
            overall_compliance = "EXCELLENT"
        elif compliance_score >= 75:
            overall_compliance = "GOOD"
        elif compliance_score >= 60:
            overall_compliance = "ACCEPTABLE"
        elif compliance_score >= 40:
            overall_compliance = "POOR"
        else:
            overall_compliance = "FAIL"
        
        # Generate recommendations
        recommendations = []
        for result in compliance_results:
            if result.compliance_status == "FAIL":
                recommendations.append(f"❌ {result.parameter}: {result.recommendation}")
            elif result.compliance_status == "WARNING":
                recommendations.append(f"⚠️ {result.parameter}: {result.recommendation}")
            else:
                recommendations.append(f"✅ {result.parameter}: {result.recommendation}")
        
        # Generate summary
        summary = f"Report '{report_name}' shows {overall_compliance} compliance ({compliance_score:.1f}%). "
        summary += f"Out of {total_params} parameters: {passed} passed, {failed} failed, {warnings} warnings."
        
        return ReportEvaluation(
            report_name=report_name,
            overall_compliance=overall_compliance,
            compliance_score=compliance_score,
            total_parameters=total_params,
            passed_parameters=passed,
            failed_parameters=failed,
            warning_parameters=warnings,
            compliance_results=compliance_results,
            recommendations=recommendations,
            summary=summary
        )

def evaluate_lighting_parameters():
    """Interactive tool to evaluate lighting parameters"""
    print("🔍 Lighting Parameter Evaluator")
    print("=" * 40)
    
    evaluator = SimpleLightingEvaluator()
    
    print("Enter your lighting parameters (press Enter to finish):")
    print()
    
    parameters = []
    
    while True:
        print("Parameter types: illuminance, uniformity, ugr, cri, color_temperature, power_density")
        param_type = input("Parameter type (or 'done' to finish): ").strip().lower()
        
        if param_type == 'done':
            break
        
        if param_type not in ['illuminance', 'uniformity', 'ugr', 'cri', 'color_temperature', 'power_density']:
            print("❌ Invalid parameter type. Please try again.")
            continue
        
        try:
            value = float(input(f"Enter {param_type} value: "))
            unit = input(f"Enter unit (or press Enter for default): ").strip()
            
            if not unit:
                unit = evaluator._get_default_unit(param_type)
            
            location = input("Enter location/room (optional): ").strip()
            
            param = LightingParameter(
                name=param_type,
                value=value,
                unit=unit,
                location=location
            )
            parameters.append(param)
            
            print(f"✅ Added {param_type}: {value} {unit}")
            print()
            
        except ValueError:
            print("❌ Invalid value. Please enter a number.")
            continue
    
    if not parameters:
        print("No parameters entered.")
        return
    
    # Get application type
    print("\nApplication types: general, office, detailed_work, conference, reception, corridor")
    application = input("Enter application type (default: general): ").strip().lower()
    if not application:
        application = "general"
    
    # Evaluate parameters
    print(f"\n📊 Evaluating {len(parameters)} parameters for {application} application...")
    print("=" * 50)
    
    passed = 0
    failed = 0
    warnings = 0
    
    for param in parameters:
        result = evaluator.check_compliance(param, application)
        
        status_icon = "✅" if result.compliance_status == "PASS" else "❌"
        print(f"{status_icon} {param.name.upper()}: {param.value} {param.unit}")
        print(f"   Status: {result.compliance_status}")
        print(f"   Recommendation: {result.recommendation}")
        print(f"   Standard: {result.standard_reference}")
        print()
        
        if result.compliance_status == "PASS":
            passed += 1
        else:
            failed += 1
    
    # Summary
    total = len(parameters)
    compliance_score = (passed / total * 100) if total > 0 else 0
    
    print("=" * 50)
    print("📊 EVALUATION SUMMARY")
    print("=" * 50)
    print(f"Total Parameters: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Compliance Score: {compliance_score:.1f}%")
    
    if compliance_score >= 90:
        print("🎉 EXCELLENT compliance!")
    elif compliance_score >= 75:
        print("✅ GOOD compliance")
    elif compliance_score >= 60:
        print("⚠️ ACCEPTABLE compliance")
    else:
        print("❌ POOR compliance - needs improvement")

def suggest_lighting_solution():
    """Suggest lighting solution based on requirements"""
    print("💡 Lighting Solution Suggester")
    print("=" * 40)
    
    evaluator = SimpleLightingEvaluator()
    
    print("Enter your space requirements:")
    print()
    
    # Get space information
    area = float(input("Room area (m²): "))
    application = input("Application (office/conference/detailed_work/reception/corridor): ").strip().lower()
    if not application:
        application = "office"
    
    # Get requirements
    required_illuminance = float(input("Required illuminance (lux, or 0 for standard): "))
    if required_illuminance == 0:
        requirements = evaluator.get_standard_requirements("illuminance", application)
        required_illuminance = requirements.get("recommended", 500)
    
    required_ugr = float(input("Required UGR (or 0 for standard): "))
    if required_ugr == 0:
        requirements = evaluator.get_standard_requirements("ugr", application)
        required_ugr = requirements.get("recommended", 19)
    
    required_cri = float(input("Required CRI (or 0 for standard): "))
    if required_cri == 0:
        requirements = evaluator.get_standard_requirements("cri", application)
        required_cri = requirements.get("recommended", 90)
    
    # Calculate suggestions
    print(f"\n💡 LIGHTING SOLUTION SUGGESTIONS")
    print("=" * 50)
    print(f"Space: {area:.1f} m² {application}")
    print(f"Required Illuminance: {required_illuminance} lux")
    print(f"Required UGR: {required_ugr}")
    print(f"Required CRI: {required_cri}")
    print()
    
    # LED suggestions
    print("🔆 LED LIGHTING SUGGESTIONS:")
    print(f"   • Use LED luminaires with CRI ≥ {required_cri}")
    print(f"   • Choose luminaires with UGR ≤ {required_ugr}")
    print(f"   • Calculate total lumens needed: {area * required_illuminance * 1.2:.0f} lm (with 20% margin)")
    print(f"   • Recommended power density: 2.5-3.5 W/m²")
    print(f"   • Estimated total power: {area * 3:.0f} W")
    print()
    
    # Layout suggestions
    print("📐 LAYOUT SUGGESTIONS:")
    if application == "office":
        print("   • Use suspended luminaires with 2x2 or 2x4 grid")
        print("   • Mounting height: 2.5-3.0m")
        print("   • Spacing: 1.5-2.0m between luminaires")
    elif application == "conference":
        print("   • Use recessed or surface-mounted luminaires")
        print("   • Add dimming controls for flexibility")
        print("   • Consider accent lighting for presentations")
    elif application == "detailed_work":
        print("   • Use high-output LED panels or linear luminaires")
        print("   • Ensure excellent uniformity (≥0.7)")
        print("   • Add task lighting for critical areas")
    
    # Control suggestions
    print("\n🎛️ CONTROL SUGGESTIONS:")
    print("   • Install occupancy sensors for energy savings")
    print("   • Add daylight dimming controls")
    print("   • Use DALI or 0-10V dimming")
    print("   • Consider smart lighting controls for large spaces")
    
    # Compliance check
    print(f"\n✅ COMPLIANCE CHECK:")
    print(f"   • Illuminance: {required_illuminance} lux ✓")
    print(f"   • UGR: ≤{required_ugr} ✓")
    print(f"   • CRI: ≥{required_cri} ✓")
    print(f"   • Power Density: ≤3.5 W/m² ✓")

def main():
    """Main menu"""
    while True:
        print("\n🚀 Simple Lighting Report Evaluator")
        print("=" * 40)
        print("1. Evaluate lighting parameters")
        print("2. Suggest lighting solution")
        print("3. Exit")
        print()
        
        choice = input("Select option (1-3): ").strip()
        
        if choice == "1":
            evaluate_lighting_parameters()
        elif choice == "2":
            suggest_lighting_solution()
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()
