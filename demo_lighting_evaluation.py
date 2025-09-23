"""
Demo: Lighting Report Evaluation System
Shows how to evaluate lighting reports against standards
"""
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

def demo_parameter_evaluation():
    """Demo: Evaluate individual lighting parameters"""
    print("🔍 Demo: Lighting Parameter Evaluation")
    print("=" * 50)
    
    try:
        from ai_standards.evaluators.lighting_report_evaluator import (
            LightingReportEvaluator, LightingParameter
        )
        
        evaluator = LightingReportEvaluator()
        
        # Example parameters from a lighting report
        print("📊 Example: Office lighting parameters")
        print()
        
        parameters = [
            LightingParameter("illuminance", 450, "lux", "Main office"),
            LightingParameter("uniformity", 0.65, "", "Main office"),
            LightingParameter("ugr", 18, "", "Main office"),
            LightingParameter("cri", 85, "", "Main office"),
            LightingParameter("power_density", 3.2, "W/m²", "Main office")
        ]
        
        for param in parameters:
            result = evaluator.check_compliance(param, "office")
            
            status_icon = "✅" if result.compliance_status == "PASS" else "❌"
            print(f"{status_icon} {param.name.upper()}: {param.value} {param.unit}")
            print(f"   Status: {result.compliance_status}")
            print(f"   Recommendation: {result.recommendation}")
            print()
        
        print("💡 This shows how the system evaluates each parameter against standards")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_dialux_evaluation():
    """Demo: Evaluate a Dialux report"""
    print("\n📊 Demo: Dialux Report Evaluation")
    print("=" * 50)
    
    try:
        from ai_standards.processors.dialux_processor import DialuxProcessor, DialuxRoom
        from ai_standards.evaluators.lighting_report_evaluator import LightingReportEvaluator
        
        # Create a sample Dialux report
        print("📄 Sample Dialux Report Data:")
        print()
        
        sample_rooms = [
            DialuxRoom("Office 1", 25.0, 480, 420, 520, 0.68, 17, 3.1),
            DialuxRoom("Office 2", 30.0, 520, 450, 580, 0.72, 16, 2.8),
            DialuxRoom("Conference Room", 20.0, 320, 280, 360, 0.75, 19, 2.5),
            DialuxRoom("Reception", 15.0, 180, 150, 220, 0.65, 22, 2.2)
        ]
        
        for room in sample_rooms:
            print(f"🏠 {room.name}:")
            print(f"   Area: {room.area} m²")
            print(f"   Illuminance: {room.illuminance_avg} lux (min: {room.illuminance_min}, max: {room.illuminance_max})")
            print(f"   Uniformity: {room.uniformity}")
            print(f"   UGR: {room.ugr}")
            print(f"   Power Density: {room.power_density} W/m²")
            print()
        
        # Evaluate compliance
        evaluator = LightingReportEvaluator()
        print("🔍 Compliance Evaluation:")
        print()
        
        passed_rooms = 0
        for room in sample_rooms:
            # Check key parameters
            from ai_standards.evaluators.lighting_report_evaluator import LightingParameter
            
            illuminance_param = LightingParameter("illuminance", room.illuminance_avg, "lux", room.name)
            illuminance_result = evaluator.check_compliance(illuminance_param, "office")
            
            ugr_param = LightingParameter("ugr", room.ugr, "", room.name)
            ugr_result = evaluator.check_compliance(ugr_param, "office")
            
            power_param = LightingParameter("power_density", room.power_density, "W/m²", room.name)
            power_result = evaluator.check_compliance(power_param, "office")
            
            room_passed = all([
                illuminance_result.compliance_status == "PASS",
                ugr_result.compliance_status == "PASS", 
                power_result.compliance_status == "PASS"
            ])
            
            if room_passed:
                passed_rooms += 1
                print(f"✅ {room.name}: PASSES compliance")
            else:
                print(f"❌ {room.name}: FAILS compliance")
                
                if illuminance_result.compliance_status != "PASS":
                    print(f"   💡 Illuminance: {illuminance_result.recommendation}")
                if ugr_result.compliance_status != "PASS":
                    print(f"   💡 UGR: {ugr_result.recommendation}")
                if power_result.compliance_status != "PASS":
                    print(f"   💡 Power: {power_result.recommendation}")
            print()
        
        # Summary
        overall_compliance = (passed_rooms / len(sample_rooms) * 100)
        print(f"📊 Overall Compliance: {overall_compliance:.1f}% ({passed_rooms}/{len(sample_rooms)} rooms)")
        
        if overall_compliance >= 90:
            print("🎉 EXCELLENT - Report meets standards!")
        elif overall_compliance >= 75:
            print("✅ GOOD - Minor improvements needed")
        else:
            print("⚠️ NEEDS IMPROVEMENT - Some rooms don't meet standards")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_lighting_solution():
    """Demo: Suggest lighting solution"""
    print("\n💡 Demo: Lighting Solution Suggestion")
    print("=" * 50)
    
    try:
        from ai_standards.evaluators.lighting_report_evaluator import LightingReportEvaluator
        
        evaluator = LightingReportEvaluator()
        
        # Example: Office space requirements
        print("📋 Example: Office Space Requirements")
        print()
        
        area = 50.0  # m²
        application = "office"
        
        # Get standard requirements
        illuminance_req = evaluator.get_standard_requirements("illuminance", application)
        ugr_req = evaluator.get_standard_requirements("ugr", application)
        cri_req = evaluator.get_standard_requirements("cri", application)
        power_req = evaluator.get_standard_requirements("power_density", application)
        
        print(f"🏢 Space: {area} m² {application}")
        print(f"📊 Requirements:")
        print(f"   • Illuminance: {illuminance_req['recommended']} lux (min: {illuminance_req['min']}, max: {illuminance_req['max']})")
        print(f"   • UGR: ≤{ugr_req['recommended']} (max: {ugr_req['max']})")
        print(f"   • CRI: ≥{cri_req['recommended']} (min: {cri_req['min']})")
        print(f"   • Power Density: ≤{power_req['recommended']} W/m² (max: {power_req['max']})")
        print()
        
        # Calculate suggestions
        total_lumens = area * illuminance_req['recommended'] * 1.2  # 20% margin
        total_power = area * power_req['recommended']
        
        print("💡 LIGHTING SOLUTION SUGGESTIONS:")
        print(f"   • Total lumens needed: {total_lumens:.0f} lm")
        print(f"   • Total power budget: {total_power:.0f} W")
        print(f"   • LED luminaires with CRI ≥ {cri_req['recommended']}")
        print(f"   • Luminaires with UGR ≤ {ugr_req['recommended']}")
        print()
        
        print("🔧 LAYOUT SUGGESTIONS:")
        print("   • Use 2x2 or 2x4 LED panels")
        print("   • Mounting height: 2.5-3.0m")
        print("   • Spacing: 1.5-2.0m between luminaires")
        print("   • Add occupancy sensors")
        print("   • Install daylight dimming controls")
        print()
        
        print("✅ This solution will meet all standard requirements!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main demo function"""
    print("🚀 Lighting Report Evaluation System - Demo")
    print("=" * 60)
    
    demo_parameter_evaluation()
    demo_dialux_evaluation()
    demo_lighting_solution()
    
    print("\n" + "=" * 60)
    print("🎯 HOW TO USE THE SYSTEM")
    print("=" * 60)
    print()
    print("1️⃣  Evaluate individual parameters:")
    print("   python evaluate_lighting_report.py")
    print("   Select option 1")
    print()
    print("2️⃣  Evaluate Dialux reports:")
    print("   python evaluate_lighting_report.py")
    print("   Select option 2")
    print()
    print("3️⃣  Get lighting solutions:")
    print("   python evaluate_lighting_report.py")
    print("   Select option 3")
    print()
    print("4️⃣  Upload your own reports:")
    print("   • Place PDF reports in base/ folder")
    print("   • Run: make auto-process")
    print("   • Use the evaluation tools")
    print()
    print("💡 The system will tell you:")
    print("   ✅ If your lighting meets standards")
    print("   ❌ What needs to be improved")
    print("   💡 Specific recommendations")
    print("   📊 Compliance scores")

if __name__ == "__main__":
    main()
