"""
Create sample processed documents for training
"""
import json
from pathlib import Path

def create_sample_processed_docs():
    """Create sample processed documents"""
    
    # Create uploads directory if it doesn't exist
    uploads_dir = Path("uploads")
    uploads_dir.mkdir(exist_ok=True)
    
    # Sample processed document structure
    sample_doc = {
        "file_path": "base/prEN 12464-1.pdf",
        "file_name": "prEN 12464-1.pdf",
        "language": "en",
        "text_content": """
        European Standard EN 12464-1:2021
        Light and lighting - Lighting of work places - Part 1: Indoor work places
        
        This European Standard specifies lighting requirements for indoor work places.
        
        Key Requirements:
        - Illuminance levels for different tasks
        - Color rendering index (CRI) requirements
        - Unified glare rating (UGR) limits
        - Energy efficiency considerations
        
        Illuminance Requirements:
        - General office work: 500 lux
        - Detailed drawing work: 1000 lux
        - Conference rooms: 300 lux
        - Reception areas: 200 lux
        
        Color Rendering:
        - Minimum CRI: 80
        - Recommended CRI: 90 for color-critical tasks
        
        Glare Control:
        - Maximum UGR: 19 for office work
        - Maximum UGR: 16 for computer work
        
        Energy Efficiency:
        - Use of LED lighting recommended
        - Automatic lighting controls
        - Daylight integration
        """,
        "tables": [
            {
                "title": "Illuminance Requirements",
                "data": [
                    ["Task", "Illuminance (lux)", "UGR Limit"],
                    ["General office work", "500", "19"],
                    ["Detailed drawing work", "1000", "16"],
                    ["Conference rooms", "300", "22"],
                    ["Reception areas", "200", "25"]
                ]
            }
        ],
        "metadata": {
            "standard_type": "European Standard",
            "standard_number": "EN 12464-1:2021",
            "title": "Light and lighting - Lighting of work places - Part 1: Indoor work places",
            "categories": ["illuminance", "color_rendering", "glare_control", "energy_efficiency"],
            "keywords": ["lighting", "workplace", "illuminance", "CRI", "UGR", "energy"]
        },
        "processing_info": {
            "processed_at": "2025-01-23T15:00:00Z",
            "processing_method": "manual_sample",
            "confidence_score": 0.95
        }
    }
    
    # Create second sample document
    sample_doc2 = {
        "file_path": "base/ODLI20150723_001-UPD-en_AA-Lighting-for-BREEAM-in-offices.pdf",
        "file_name": "ODLI20150723_001-UPD-en_AA-Lighting-for-BREEAM-in-offices.pdf",
        "language": "en",
        "text_content": """
        Lighting for BREEAM in Offices
        Updated guidance for lighting design in office buildings
        
        BREEAM Requirements:
        - Sustainable lighting design
        - Energy efficiency compliance
        - Environmental impact reduction
        - User comfort and wellbeing
        
        Lighting Design Principles:
        - Maximize daylight utilization
        - Minimize artificial lighting needs
        - Use energy-efficient light sources
        - Implement smart lighting controls
        
        Performance Criteria:
        - Lighting power density limits
        - Daylight factor requirements
        - Glare control measures
        - Color temperature considerations
        
        Energy Efficiency:
        - LED lighting systems
        - Occupancy sensors
        - Daylight dimming controls
        - Task lighting integration
        
        Environmental Impact:
        - Reduced carbon footprint
        - Lower energy consumption
        - Sustainable materials
        - Lifecycle assessment
        """,
        "tables": [
            {
                "title": "BREEAM Lighting Criteria",
                "data": [
                    ["Criteria", "Requirement", "Points"],
                    ["Lighting Power Density", "< 3.5 W/m²", "2"],
                    ["Daylight Factor", "> 2%", "1"],
                    ["Glare Control", "UGR < 19", "1"],
                    ["Energy Efficiency", "LED + Controls", "2"]
                ]
            }
        ],
        "metadata": {
            "standard_type": "BREEAM Guidance",
            "standard_number": "ODLI20150723_001",
            "title": "Lighting for BREEAM in Offices",
            "categories": ["breeam", "sustainability", "energy_efficiency", "daylight"],
            "keywords": ["breeam", "lighting", "sustainability", "energy", "daylight", "office"]
        },
        "processing_info": {
            "processed_at": "2025-01-23T15:00:00Z",
            "processing_method": "manual_sample",
            "confidence_score": 0.95
        }
    }
    
    # Save the processed documents
    doc1_path = uploads_dir / "prEN 12464-1_processed.json"
    doc2_path = uploads_dir / "ODLI20150723_001-UPD-en_AA-Lighting-for-BREEAM-in-offices_processed.json"
    
    with open(doc1_path, 'w', encoding='utf-8') as f:
        json.dump(sample_doc, f, indent=2, ensure_ascii=False)
    
    with open(doc2_path, 'w', encoding='utf-8') as f:
        json.dump(sample_doc2, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Created sample processed documents:")
    print(f"  - {doc1_path.name}")
    print(f"  - {doc2_path.name}")
    
    return [doc1_path, doc2_path]

if __name__ == "__main__":
    create_sample_processed_docs()
