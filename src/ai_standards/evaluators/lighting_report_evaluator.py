"""
Lighting Report Evaluator
Compares lighting reports against standards and provides recommendations
"""
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from loguru import logger

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

class LightingReportEvaluator:
    """Evaluates lighting reports against standards"""
    
    def __init__(self):
        self.standards_data = {}
        self._load_standards()
    
    def _load_standards(self):
        """Load standards data from processed documents"""
        try:
            from ..core.config import config
            
            processed_files = list(config.UPLOADS_DIR.glob("*_processed.json"))
            for file_path in processed_files:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.standards_data[data['file_name']] = data
            
            logger.info(f"Loaded {len(self.standards_data)} standards")
        except Exception as e:
            logger.error(f"Failed to load standards: {e}")
    
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
    
    def evaluate_report(self, report_text: str, report_name: str = "Unknown", application: str = "general") -> ReportEvaluation:
        """Evaluate a complete lighting report"""
        logger.info(f"Evaluating report: {report_name}")
        
        # Extract parameters
        parameters = self.extract_lighting_parameters(report_text)
        logger.info(f"Extracted {len(parameters)} parameters")
        
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
    
    def suggest_application(self, parameters: List[LightingParameter]) -> str:
        """Suggest the most likely application based on parameters"""
        # Analyze parameters to determine application
        illuminance_values = [p.value for p in parameters if p.name == 'illuminance']
        
        if not illuminance_values:
            return "general"
        
        avg_illuminance = sum(illuminance_values) / len(illuminance_values)
        
        if avg_illuminance >= 800:
            return "detailed_work"
        elif avg_illuminance >= 500:
            return "office"
        elif avg_illuminance >= 300:
            return "conference"
        elif avg_illuminance >= 150:
            return "reception"
        else:
            return "corridor"
