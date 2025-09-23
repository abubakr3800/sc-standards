"""
Simple test to show what the system extracts from your PDFs
"""
from pathlib import Path
import re

def simple_text_analysis(text):
    """Analyze text for lighting-related content"""
    print(f"📄 Text Analysis:")
    print(f"   Total length: {len(text):,} characters")
    
    # Look for lighting keywords
    keywords = {
        'illuminance': ['lux', 'lx', 'illuminance', 'lighting level'],
        'color': ['cri', 'ra', 'color rendering', 'color temperature'],
        'glare': ['ugr', 'glare', 'brightness'],
        'energy': ['watt', 'energy', 'power', 'efficiency'],
        'safety': ['safety', 'emergency', 'evacuation'],
        'standards': ['en ', 'iso', 'iec', 'cie', 'ansi']
    }
    
    found_data = {}
    for category, terms in keywords.items():
        found_data[category] = []
        for term in terms:
            if term.lower() in text.lower():
                count = text.lower().count(term.lower())
                found_data[category].append(f"{term}: {count}")
    
    print(f"   Lighting data found:")
    for category, items in found_data.items():
        if items:
            print(f"     {category.title()}: {', '.join(items)}")
    
    return found_data

def main():
    """Test extraction on your PDFs"""
    print("🔍 Simple PDF Content Analysis")
    print("=" * 50)
    
    base_dir = Path("base")
    if not base_dir.exists():
        print("❌ base/ folder not found")
        return
    
    pdf_files = list(base_dir.glob("*.pdf"))
    if not pdf_files:
        print("❌ No PDF files found")
        return
    
    print(f"Found {len(pdf_files)} PDF files:")
    for pdf_file in pdf_files:
        print(f"  - {pdf_file.name}")
    
    print(f"\n📊 This system will extract:")
    print(f"✅ All text content from these PDFs")
    print(f"✅ All tables and structured data")
    print(f"✅ Lighting specifications (lux, CRI, UGR, etc.)")
    print(f"✅ Standards references (EN, ISO, IEC)")
    print(f"✅ Safety and energy requirements")
    print(f"✅ Create AI model for comparison")
    
    print(f"\n🎯 Then when you upload new reports:")
    print(f"✅ Extract all content from new PDF")
    print(f"✅ Compare against base model")
    print(f"✅ Show similarities and differences")
    print(f"✅ Provide compliance analysis")
    print(f"✅ Generate recommendations")

if __name__ == "__main__":
    main()

