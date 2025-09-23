"""
Lighting Report Evaluator
Evaluates lighting reports against standards and provides recommendations
"""
import sys
import json
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

def evaluate_lighting_parameters():
    """Interactive tool to evaluate lighting parameters"""
    print("🔍 Lighting Parameter Evaluator")
    print("=" * 40)
    
    try:
        from ai_standards.evaluators.lighting_report_evaluator import LightingReportEvaluator
        
        evaluator = LightingReportEvaluator()
        
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
                
                from ai_standards.evaluators.lighting_report_evaluator import LightingParameter
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
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def evaluate_dialux_report():
    """Evaluate a Dialux report file"""
    print("📊 Dialux Report Evaluator")
    print("=" * 40)
    
    try:
        from ai_standards.processors.dialux_processor import DialuxProcessor
        from ai_standards.evaluators.lighting_report_evaluator import LightingReportEvaluator
        
        # Get file path
        file_path = input("Enter path to Dialux report file: ").strip()
        if not file_path:
            print("❌ No file path provided")
            return
        
        file_path = Path(file_path)
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            return
        
        # Process Dialux report
        print(f"📄 Processing Dialux report: {file_path.name}")
        processor = DialuxProcessor()
        dialux_report = processor.process_dialux_report(file_path)
        
        if not dialux_report:
            print("❌ Failed to process Dialux report")
            return
        
        print(f"✅ Processed report: {dialux_report.project_name}")
        print(f"   Rooms: {len(dialux_report.rooms)}")
        print(f"   Total Area: {dialux_report.total_area:.1f} m²")
        print(f"   Average Power Density: {dialux_report.average_power_density:.2f} W/m²")
        
        # Evaluate each room
        evaluator = LightingReportEvaluator()
        
        print(f"\n🔍 Evaluating each room...")
        print("=" * 50)
        
        total_rooms = len(dialux_report.rooms)
        passed_rooms = 0
        
        for room in dialux_report.rooms:
            print(f"\n🏠 Room: {room.name}")
            print(f"   Area: {room.area:.1f} m²")
            print(f"   Illuminance: {room.illuminance_avg:.0f} lux (min: {room.illuminance_min:.0f}, max: {room.illuminance_max:.0f})")
            print(f"   Uniformity: {room.uniformity:.2f}")
            print(f"   UGR: {room.ugr:.1f}")
            print(f"   Power Density: {room.power_density:.2f} W/m²")
            
            # Check compliance for key parameters
            from ai_standards.evaluators.lighting_report_evaluator import LightingParameter
            
            # Illuminance check
            illuminance_param = LightingParameter("illuminance", room.illuminance_avg, "lux", room.name)
            illuminance_result = evaluator.check_compliance(illuminance_param, "office")
            
            # UGR check
            ugr_param = LightingParameter("ugr", room.ugr, "", room.name)
            ugr_result = evaluator.check_compliance(ugr_param, "office")
            
            # Power density check
            power_param = LightingParameter("power_density", room.power_density, "W/m²", room.name)
            power_result = evaluator.check_compliance(power_param, "office")
            
            # Room compliance
            room_passed = all([
                illuminance_result.compliance_status == "PASS",
                ugr_result.compliance_status == "PASS",
                power_result.compliance_status == "PASS"
            ])
            
            if room_passed:
                passed_rooms += 1
                print("   ✅ Room PASSES compliance")
            else:
                print("   ❌ Room FAILS compliance")
            
            # Show recommendations
            if illuminance_result.compliance_status != "PASS":
                print(f"   💡 Illuminance: {illuminance_result.recommendation}")
            if ugr_result.compliance_status != "PASS":
                print(f"   💡 UGR: {ugr_result.recommendation}")
            if power_result.compliance_status != "PASS":
                print(f"   💡 Power: {power_result.recommendation}")
        
        # Overall summary
        overall_compliance = (passed_rooms / total_rooms * 100) if total_rooms > 0 else 0
        
        print(f"\n" + "=" * 50)
        print("📊 DIALUX REPORT SUMMARY")
        print("=" * 50)
        print(f"Project: {dialux_report.project_name}")
        print(f"Total Rooms: {total_rooms}")
        print(f"Compliant Rooms: {passed_rooms}")
        print(f"Overall Compliance: {overall_compliance:.1f}%")
        
        if overall_compliance >= 90:
            print("🎉 EXCELLENT - Report meets standards!")
        elif overall_compliance >= 75:
            print("✅ GOOD - Minor improvements needed")
        elif overall_compliance >= 60:
            print("⚠️ ACCEPTABLE - Some improvements required")
        else:
            print("❌ POOR - Significant improvements needed")
        
        # Save evaluation results
        output_file = file_path.parent / f"{file_path.stem}_evaluation.json"
        evaluation_data = {
            "project_name": dialux_report.project_name,
            "evaluation_date": datetime.now().isoformat(),
            "overall_compliance": overall_compliance,
            "total_rooms": total_rooms,
            "compliant_rooms": passed_rooms,
            "rooms": [
                {
                    "name": room.name,
                    "area": room.area,
                    "illuminance_avg": room.illuminance_avg,
                    "uniformity": room.uniformity,
                    "ugr": room.ugr,
                    "power_density": room.power_density
                }
                for room in dialux_report.rooms
            ]
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(evaluation_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Evaluation saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def suggest_lighting_solution():
    """Suggest lighting solution based on requirements"""
    print("💡 Lighting Solution Suggester")
    print("=" * 40)
    
    try:
        from ai_standards.evaluators.lighting_report_evaluator import LightingReportEvaluator
        
        evaluator = LightingReportEvaluator()
        
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
        
    except ValueError:
        print("❌ Invalid input. Please enter numbers for numerical values.")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main menu"""
    while True:
        print("\n🚀 Lighting Report Evaluator")
        print("=" * 40)
        print("1. Evaluate lighting parameters")
        print("2. Evaluate Dialux report")
        print("3. Suggest lighting solution")
        print("4. Exit")
        print()
        
        choice = input("Select option (1-4): ").strip()
        
        if choice == "1":
            evaluate_lighting_parameters()
        elif choice == "2":
            evaluate_dialux_report()
        elif choice == "3":
            suggest_lighting_solution()
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select 1-4.")

if __name__ == "__main__":
    main()
