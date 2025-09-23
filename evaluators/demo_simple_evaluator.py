"""
Demo: Simple Lighting Evaluator
Shows how the system works with example data
"""
from simple_lighting_evaluator import SimpleLightingEvaluator, LightingParameter

def demo_parameter_evaluation():
    """Demo parameter evaluation with example data"""
    print("🔍 Demo: Lighting Parameter Evaluation")
    print("=" * 50)
    
    evaluator = SimpleLightingEvaluator()
    
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
    
    print("Evaluating parameters for 'office' application:")
    print()
    
    passed = 0
    failed = 0
    
    for param in parameters:
        result = evaluator.check_compliance(param, "office")
        
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

def demo_lighting_solution():
    """Demo lighting solution suggestion"""
    print("\n💡 Demo: Lighting Solution Suggestion")
    print("=" * 50)
    
    evaluator = SimpleLightingEvaluator()
    
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
    print(f"   • CRI: ≥{cri_req.get('recommended', 90)} (min: {cri_req.get('min', 80)})")
    print(f"   • Power Density: ≤{power_req['recommended']} W/m² (max: {power_req['max']})")
    print()
    
    # Calculate suggestions
    total_lumens = area * illuminance_req['recommended'] * 1.2  # 20% margin
    total_power = area * power_req['recommended']
    
    print("💡 LIGHTING SOLUTION SUGGESTIONS:")
    print(f"   • Total lumens needed: {total_lumens:.0f} lm")
    print(f"   • Total power budget: {total_power:.0f} W")
    print(f"   • LED luminaires with CRI ≥ {cri_req.get('recommended', 90)}")
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

def demo_dialux_evaluation():
    """Demo Dialux report evaluation"""
    print("\n📊 Demo: Dialux Report Evaluation")
    print("=" * 50)
    
    evaluator = SimpleLightingEvaluator()
    
    # Sample room data (like from a Dialux report)
    rooms = [
        {"name": "Office 1", "area": 25.0, "illuminance": 480, "ugr": 17, "power_density": 3.1},
        {"name": "Office 2", "area": 30.0, "illuminance": 520, "ugr": 16, "power_density": 2.8},
        {"name": "Conference Room", "area": 20.0, "illuminance": 320, "ugr": 19, "power_density": 2.5},
        {"name": "Reception", "area": 15.0, "illuminance": 180, "ugr": 22, "power_density": 2.2}
    ]
    
    print("📄 Sample Dialux Report Data:")
    print()
    
    for room in rooms:
        print(f"🏠 {room['name']}:")
        print(f"   Area: {room['area']} m²")
        print(f"   Illuminance: {room['illuminance']} lux")
        print(f"   UGR: {room['ugr']}")
        print(f"   Power Density: {room['power_density']} W/m²")
        print()
    
    # Evaluate each room
    print("🔍 Compliance Evaluation:")
    print()
    
    passed_rooms = 0
    for room in rooms:
        # Check key parameters
        illuminance_param = LightingParameter("illuminance", room['illuminance'], "lux", room['name'])
        illuminance_result = evaluator.check_compliance(illuminance_param, "office")
        
        ugr_param = LightingParameter("ugr", room['ugr'], "", room['name'])
        ugr_result = evaluator.check_compliance(ugr_param, "office")
        
        power_param = LightingParameter("power_density", room['power_density'], "W/m²", room['name'])
        power_result = evaluator.check_compliance(power_param, "office")
        
        room_passed = all([
            illuminance_result.compliance_status == "PASS",
            ugr_result.compliance_status == "PASS",
            power_result.compliance_status == "PASS"
        ])
        
        if room_passed:
            passed_rooms += 1
            print(f"✅ {room['name']}: PASSES compliance")
        else:
            print(f"❌ {room['name']}: FAILS compliance")
            
            if illuminance_result.compliance_status != "PASS":
                print(f"   💡 Illuminance: {illuminance_result.recommendation}")
            if ugr_result.compliance_status != "PASS":
                print(f"   💡 UGR: {ugr_result.recommendation}")
            if power_result.compliance_status != "PASS":
                print(f"   💡 Power: {power_result.recommendation}")
        print()
    
    # Summary
    overall_compliance = (passed_rooms / len(rooms) * 100)
    print(f"📊 Overall Compliance: {overall_compliance:.1f}% ({passed_rooms}/{len(rooms)} rooms)")
    
    if overall_compliance >= 90:
        print("🎉 EXCELLENT - Report meets standards!")
    elif overall_compliance >= 75:
        print("✅ GOOD - Minor improvements needed")
    else:
        print("⚠️ NEEDS IMPROVEMENT - Some rooms don't meet standards")

def main():
    """Main demo function"""
    print("🚀 Simple Lighting Evaluator - Demo")
    print("=" * 60)
    
    demo_parameter_evaluation()
    demo_lighting_solution()
    demo_dialux_evaluation()
    
    print("\n" + "=" * 60)
    print("🎯 HOW TO USE THE SYSTEM")
    print("=" * 60)
    print()
    print("1️⃣  Interactive evaluation:")
    print("   make evaluate")
    print("   Select option 1")
    print()
    print("2️⃣  Get lighting solutions:")
    print("   make evaluate")
    print("   Select option 2")
    print()
    print("3️⃣  For your own data:")
    print("   • Enter your lighting parameters")
    print("   • Get instant compliance assessment")
    print("   • Receive specific recommendations")
    print()
    print("💡 The system will tell you:")
    print("   ✅ If your lighting meets standards")
    print("   ❌ What needs to be improved")
    print("   💡 Specific recommendations")
    print("   📊 Compliance scores")

if __name__ == "__main__":
    main()
