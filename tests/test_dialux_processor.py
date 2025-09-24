"""
Test Dialux PDF Processor
Shows how to use the Dialux PDF processing functionality
"""
from pathlib import Path

def test_dialux_processor():
    """Test the Dialux PDF processor with example data"""
    print("🧪 Testing Dialux PDF Processor")
    print("=" * 40)
    
    try:
        from dialux_pdf_processor import DialuxPDFProcessor, DialuxRoom, DialuxReport
        
        # Create a sample processor
        processor = DialuxPDFProcessor()
        print("✅ Dialux processor created successfully")
        
        # Test text extraction patterns
        sample_text = """
        Project: Office Building Lighting Design
        
        Room: Main Office
        Area: 25.0 m²
        Average: 480 lux
        Minimum: 420 lux
        Maximum: 520 lux
        Uniformity: 0.68
        UGR: 17
        Power Density: 3.1 W/m²
        
        Room: Conference Room
        Area: 20.0 m²
        Average: 320 lux
        Minimum: 280 lux
        Maximum: 360 lux
        Uniformity: 0.75
        UGR: 19
        Power Density: 2.5 W/m²
        """
        
        print("📄 Testing text extraction...")
        
        # Test project name extraction
        project_name = processor.extract_project_name(sample_text)
        print(f"✅ Project name extracted: {project_name}")
        
        # Test room data extraction
        rooms = processor.extract_room_data(sample_text)
        print(f"✅ Extracted {len(rooms)} rooms")
        
        for room in rooms:
            print(f"   🏠 {room.name}: {room.illuminance_avg} lux, UGR: {room.ugr}")
        
        # Test summary calculation
        stats = processor.calculate_summary_stats(rooms)
        print(f"✅ Summary stats calculated:")
        print(f"   Total area: {stats['total_area']} m²")
        print(f"   Average power density: {stats['average_power_density']:.2f} W/m²")
        print(f"   Overall uniformity: {stats['overall_uniformity']:.2f}")
        print(f"   Worst UGR: {stats['worst_ugr']}")
        
        print("\n🎉 All tests passed! Dialux processor is working correctly.")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure dialux_pdf_processor.py is in the same directory")
    except Exception as e:
        print(f"❌ Error: {e}")

def show_usage():
    """Show how to use the Dialux processor"""
    print("\n📋 How to Use Dialux PDF Processor")
    print("=" * 40)
    
    print("1️⃣  Using the main system:")
    print("   python main.py dialux --file path/to/your/dialux_report.pdf")
    print()
    
    print("2️⃣  Using the standalone processor:")
    print("   python dialux_pdf_processor.py")
    print("   (Then enter the path when prompted)")
    print()
    
    print("3️⃣  What the processor does:")
    print("   • Extracts text from Dialux PDF reports")
    print("   • Identifies rooms and their lighting parameters")
    print("   • Evaluates compliance against EN 12464-1 standards")
    print("   • Provides recommendations for improvements")
    print("   • Saves evaluation results to JSON file")
    print()
    
    print("4️⃣  Supported parameters:")
    print("   • Illuminance (average, minimum, maximum)")
    print("   • Uniformity")
    print("   • UGR (Unified Glare Rating)")
    print("   • Power density")
    print("   • Room area")
    print()
    
    print("5️⃣  Output:")
    print("   • Room-by-room compliance analysis")
    print("   • Overall project compliance score")
    print("   • Specific recommendations")
    print("   • JSON file with detailed results")

def main():
    """Main function"""
    print("🚀 Dialux PDF Processor - Test & Usage Guide")
    print("=" * 50)
    
    test_dialux_processor()
    show_usage()
    
    print("\n" + "=" * 50)
    print("🎯 Ready to Process Your Dialux Reports!")
    print("=" * 50)
    print("Just run: python main.py dialux --file your_dialux_report.pdf")

if __name__ == "__main__":
    main()
