"""
Quick File Organization
Simple script to organize the most important files
"""
import shutil
from pathlib import Path
import json

def main():
    """Quick organization of key files"""
    print("🗂️  QUICK FILE ORGANIZATION")
    print("=" * 40)
    
    # Create key directories
    directories = [
        "tools",
        "scripts", 
        "evaluators",
        "processors",
        "web",
        "temp"
    ]
    
    print("📁 Creating directories...")
    for dir_name in directories:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"  ✅ {dir_name}/")
    
    # Move key files
    file_moves = {
        # Tools
        "pdf_study_analyzer.py": "tools/",
        "batch_study_analyzer.py": "tools/",
        "analyze_study.py": "tools/",
        "upload_study_analyzer.py": "tools/",
        "enhanced_chat_api.py": "tools/",
        "chat_api.py": "tools/",
        "chat_web_interface.py": "tools/",
        
        # Scripts
        "start_chat_system.py": "scripts/",
        "start_pdf_analyzer.py": "scripts/",
        "run_accuracy_improvements.py": "scripts/",
        "improve_accuracy.py": "scripts/",
        "add_more_standards_data.py": "scripts/",
        "auto_process.py": "scripts/",
        
        # Evaluators
        "simple_lighting_evaluator.py": "evaluators/",
        "realistic_lighting_evaluator.py": "evaluators/",
        "evaluate_lighting_report.py": "evaluators/",
        "batch_pdf_evaluator.py": "evaluators/",
        "quick_batch_evaluator.py": "evaluators/",
        "quick_realistic_evaluator.py": "evaluators/",
        "demo_lighting_evaluation.py": "evaluators/",
        "demo_simple_evaluator.py": "evaluators/",
        
        # Processors
        "dialux_pdf_processor.py": "processors/",
        "enhanced_dialux_processor.py": "processors/",
        "create_sample_processed.py": "processors/",
        
        # Web
        "chat_web.html": "web/",
        
        # Temp files
        "out.json": "temp/",
        "accuracy_report.json": "temp/",
        "requirements-fixed.txt": "temp/",
        "requirements-resolved.txt": "temp/",
        "-p": "temp/",
        "=0.14.0": "temp/",
        "=0.27.0": "temp/",
        "=1.0.0": "temp/"
    }
    
    print("\n📦 Moving files...")
    moved_count = 0
    for file_name, target_dir in file_moves.items():
        source_path = Path(file_name)
        target_path = Path(target_dir) / file_name
        
        if source_path.exists():
            try:
                shutil.move(str(source_path), str(target_path))
                print(f"  ✅ {file_name} → {target_dir}")
                moved_count += 1
            except Exception as e:
                print(f"  ❌ {file_name}: {e}")
        else:
            print(f"  ⚠️  {file_name} not found")
    
    # Organize data files
    print("\n📊 Organizing data files...")
    
    # Create data subdirectories
    data_dirs = ["data/standards", "data/reports", "data/processed", "data/studies"]
    for dir_name in data_dirs:
        Path(dir_name).mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {dir_name}/")
    
    # Move standards PDFs
    base_dir = Path("base")
    if base_dir.exists():
        for pdf_file in base_dir.glob("*.pdf"):
            target_path = Path("data/standards") / pdf_file.name
            shutil.move(str(pdf_file), str(target_path))
            print(f"  ✅ {pdf_file.name} → data/standards/")
    
    # Move report PDFs
    data_dir = Path("data")
    if data_dir.exists():
        for pdf_file in data_dir.glob("*.pdf"):
            target_path = Path("data/reports") / pdf_file.name
            shutil.move(str(pdf_file), str(target_path))
            print(f"  ✅ {pdf_file.name} → data/reports/")
    
    # Move processed data
    uploads_dir = Path("uploads")
    if uploads_dir.exists():
        for json_file in uploads_dir.glob("*.json"):
            target_path = Path("data/processed") / json_file.name
            shutil.move(str(json_file), str(target_path))
            print(f"  ✅ {json_file.name} → data/processed/")
    
    # Move study results
    studies_dir = Path("studies")
    if studies_dir.exists():
        for json_file in studies_dir.glob("*.json"):
            target_path = Path("data/studies") / json_file.name
            shutil.move(str(json_file), str(target_path))
            print(f"  ✅ {json_file.name} → data/studies/")
    
    print(f"\n🎉 Organization completed!")
    print(f"📊 Moved {moved_count} files")
    print("\n📁 New structure:")
    print("  tools/ - Analysis tools")
    print("  scripts/ - Utility scripts")
    print("  evaluators/ - Evaluation tools")
    print("  processors/ - Processing tools")
    print("  web/ - Web interface files")
    print("  data/ - All data files organized")
    print("  temp/ - Temporary files")

if __name__ == "__main__":
    main()
