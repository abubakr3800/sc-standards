"""
Add More Standards Data
Adds comprehensive lighting standards data for better accuracy
"""
import json
from pathlib import Path
from typing import Dict, List, Any

class StandardsDataEnhancer:
    """Enhances standards data with comprehensive lighting requirements"""
    
    def __init__(self):
        self.uploads_dir = Path("uploads")
        self.enhanced_data = {}
    
    def add_comprehensive_standards(self):
        """Add comprehensive lighting standards data"""
        print("📚 Adding comprehensive lighting standards data...")
        
        # EN 12464-1:2021 comprehensive data
        en12464_data = {
            "standard": "EN 12464-1:2021",
            "title": "Light and lighting - Lighting of work places - Part 1: Indoor work places",
            "applications": {
                "office_general": {
                    "illuminance": {"maintained": 500, "minimum": 300, "maximum": 1000},
                    "ugr": {"maximum": 19, "recommended": 16},
                    "cri": {"minimum": 80, "recommended": 90},
                    "uniformity": {"minimum": 0.6, "recommended": 0.8},
                    "power_density": {"maximum": 3.5, "recommended": 2.5}
                },
                "office_computer": {
                    "illuminance": {"maintained": 500, "minimum": 300, "maximum": 1000},
                    "ugr": {"maximum": 16, "recommended": 13},
                    "cri": {"minimum": 80, "recommended": 90},
                    "uniformity": {"minimum": 0.6, "recommended": 0.8},
                    "power_density": {"maximum": 3.5, "recommended": 2.5}
                },
                "conference_room": {
                    "illuminance": {"maintained": 300, "minimum": 200, "maximum": 500},
                    "ugr": {"maximum": 22, "recommended": 19},
                    "cri": {"minimum": 80, "recommended": 90},
                    "uniformity": {"minimum": 0.6, "recommended": 0.8},
                    "power_density": {"maximum": 3.5, "recommended": 2.5}
                },
                "corridor": {
                    "illuminance": {"maintained": 100, "minimum": 50, "maximum": 200},
                    "ugr": {"maximum": 25, "recommended": 22},
                    "cri": {"minimum": 80, "recommended": 80},
                    "uniformity": {"minimum": 0.4, "recommended": 0.6},
                    "power_density": {"maximum": 2.0, "recommended": 1.5}
                },
                "reception": {
                    "illuminance": {"maintained": 200, "minimum": 100, "maximum": 300},
                    "ugr": {"maximum": 25, "recommended": 22},
                    "cri": {"minimum": 80, "recommended": 90},
                    "uniformity": {"minimum": 0.6, "recommended": 0.8},
                    "power_density": {"maximum": 3.0, "recommended": 2.0}
                },
                "staircase": {
                    "illuminance": {"maintained": 150, "minimum": 100, "maximum": 300},
                    "ugr": {"maximum": 25, "recommended": 22},
                    "cri": {"minimum": 80, "recommended": 80},
                    "uniformity": {"minimum": 0.4, "recommended": 0.6},
                    "power_density": {"maximum": 2.5, "recommended": 2.0}
                },
                "detailed_work": {
                    "illuminance": {"maintained": 1000, "minimum": 500, "maximum": 2000},
                    "ugr": {"maximum": 16, "recommended": 13},
                    "cri": {"minimum": 90, "recommended": 95},
                    "uniformity": {"minimum": 0.7, "recommended": 0.9},
                    "power_density": {"maximum": 5.0, "recommended": 4.0}
                },
                "meeting_room": {
                    "illuminance": {"maintained": 300, "minimum": 200, "maximum": 500},
                    "ugr": {"maximum": 22, "recommended": 19},
                    "cri": {"minimum": 80, "recommended": 90},
                    "uniformity": {"minimum": 0.6, "recommended": 0.8},
                    "power_density": {"maximum": 3.5, "recommended": 2.5}
                },
                "open_plan_office": {
                    "illuminance": {"maintained": 500, "minimum": 300, "maximum": 1000},
                    "ugr": {"maximum": 19, "recommended": 16},
                    "cri": {"minimum": 80, "recommended": 90},
                    "uniformity": {"minimum": 0.6, "recommended": 0.8},
                    "power_density": {"maximum": 3.5, "recommended": 2.5}
                },
                "break_room": {
                    "illuminance": {"maintained": 200, "minimum": 100, "maximum": 300},
                    "ugr": {"maximum": 25, "recommended": 22},
                    "cri": {"minimum": 80, "recommended": 80},
                    "uniformity": {"minimum": 0.6, "recommended": 0.8},
                    "power_density": {"maximum": 3.0, "recommended": 2.0}
                }
            },
            "definitions": {
                "illuminance": "The amount of light falling on a surface, measured in lux (lx). It indicates how bright a surface appears to the human eye.",
                "ugr": "Unified Glare Rating - a measure of glare from luminaires, with lower values indicating less glare. Values range from 10 (no glare) to 30 (unacceptable glare).",
                "cri": "Color Rendering Index - measures how accurately a light source renders colors compared to natural light. Values range from 0 to 100, with 100 being perfect color rendering.",
                "uniformity": "The ratio of minimum illuminance to average illuminance in a space. Higher values indicate more even lighting distribution.",
                "power_density": "The amount of electrical power consumed per unit area, measured in W/m². Lower values indicate more energy-efficient lighting."
            },
            "measurement_conditions": {
                "illuminance": "Measured at working plane height (0.8m for seated work, 1.0m for standing work)",
                "ugr": "Calculated for observer position at 1.2m height, looking horizontally",
                "cri": "Measured using standard color samples under the light source",
                "uniformity": "Calculated as ratio of minimum to average illuminance in the space",
                "power_density": "Total lighting power divided by floor area"
            }
        }
        
        # BREEAM lighting requirements
        breeam_data = {
            "standard": "BREEAM",
            "title": "Building Research Establishment Environmental Assessment Method",
            "applications": {
                "office_general": {
                    "illuminance": {"maintained": 500, "minimum": 300, "maximum": 1000},
                    "ugr": {"maximum": 19, "recommended": 16},
                    "cri": {"minimum": 80, "recommended": 90},
                    "uniformity": {"minimum": 0.6, "recommended": 0.8},
                    "power_density": {"maximum": 3.5, "recommended": 2.5}
                },
                "conference_room": {
                    "illuminance": {"maintained": 300, "minimum": 200, "maximum": 500},
                    "ugr": {"maximum": 22, "recommended": 19},
                    "cri": {"minimum": 80, "recommended": 90},
                    "uniformity": {"minimum": 0.6, "recommended": 0.8},
                    "power_density": {"maximum": 3.5, "recommended": 2.5}
                }
            },
            "energy_requirements": {
                "lighting_power_density": "Maximum 3.5 W/m² for office spaces",
                "daylight_factor": "Minimum 2% for 80% of floor area",
                "lighting_controls": "Required for energy efficiency credits"
            }
        }
        
        # ISO 8995-1:2013 data
        iso8995_data = {
            "standard": "ISO 8995-1:2013",
            "title": "Lighting of work places - Part 1: Indoor work places",
            "applications": {
                "office_general": {
                    "illuminance": {"maintained": 500, "minimum": 300, "maximum": 1000},
                    "ugr": {"maximum": 19, "recommended": 16},
                    "cri": {"minimum": 80, "recommended": 90},
                    "uniformity": {"minimum": 0.6, "recommended": 0.8},
                    "power_density": {"maximum": 3.5, "recommended": 2.5}
                }
            }
        }
        
        # Save enhanced data
        self.enhanced_data = {
            "en12464_2021": en12464_data,
            "breeam": breeam_data,
            "iso8995_2013": iso8995_data
        }
        
        self._save_enhanced_data()
        print("✅ Enhanced standards data added successfully!")
    
    def _save_enhanced_data(self):
        """Save enhanced data to file"""
        output_file = self.uploads_dir / "enhanced_standards_data.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.enhanced_data, f, indent=2, ensure_ascii=False)
        
        print(f"📁 Saved enhanced data to {output_file}")
        
        # Also create a simplified version for easy access
        simplified_data = self._create_simplified_data()
        simplified_file = self.uploads_dir / "simplified_standards_data.json"
        
        with open(simplified_file, 'w', encoding='utf-8') as f:
            json.dump(simplified_data, f, indent=2, ensure_ascii=False)
        
        print(f"📁 Saved simplified data to {simplified_file}")
    
    def _create_simplified_data(self) -> Dict:
        """Create simplified data structure for easy access"""
        simplified = {
            "applications": {},
            "parameters": {},
            "definitions": {},
            "measurement_conditions": {}
        }
        
        # Extract all applications
        for standard_name, standard_data in self.enhanced_data.items():
            if "applications" in standard_data:
                for app_name, app_data in standard_data["applications"].items():
                    if app_name not in simplified["applications"]:
                        simplified["applications"][app_name] = app_data
        
        # Extract definitions
        for standard_name, standard_data in self.enhanced_data.items():
            if "definitions" in standard_data:
                simplified["definitions"].update(standard_data["definitions"])
        
        # Extract measurement conditions
        for standard_name, standard_data in self.enhanced_data.items():
            if "measurement_conditions" in standard_data:
                simplified["measurement_conditions"].update(standard_data["measurement_conditions"])
        
        return simplified

def main():
    """Main function"""
    print("📚 ADDING COMPREHENSIVE STANDARDS DATA")
    print("=" * 50)
    
    enhancer = StandardsDataEnhancer()
    enhancer.add_comprehensive_standards()
    
    print("\n✅ ENHANCEMENT COMPLETED!")
    print("=" * 50)
    print("📁 Check uploads/enhanced_standards_data.json for detailed data")
    print("📁 Check uploads/simplified_standards_data.json for simplified access")
    print("\n🚀 This will significantly improve chat accuracy!")

if __name__ == "__main__":
    main()
