"""
File Organization Script
Organizes all project files into a clean, professional structure
"""
import shutil
from pathlib import Path
import json
from datetime import datetime

class FileOrganizer:
    """Organizes project files into a clean structure"""
    
    def __init__(self):
        self.root_dir = Path(".")
        self.organized_structure = {
            "core": {
                "description": "Core system files",
                "files": [
                    "main.py",
                    "requirements.txt",
                    "setup.cfg",
                    "pyproject.toml",
                    "Dockerfile",
                    "docker-compose.yml",
                    "LICENSE",
                    "README.md"
                ]
            },
            "src": {
                "description": "Source code modules",
                "keep_existing": True
            },
            "data": {
                "description": "Data files and PDFs",
                "subdirs": {
                    "standards": "Original standards PDFs",
                    "reports": "User uploaded reports",
                    "processed": "Processed JSON data",
                    "studies": "Analysis results"
                }
            },
            "tools": {
                "description": "Analysis and processing tools",
                "files": [
                    "pdf_study_analyzer.py",
                    "batch_study_analyzer.py",
                    "analyze_study.py",
                    "upload_study_analyzer.py",
                    "enhanced_chat_api.py",
                    "chat_api.py",
                    "chat_web_interface.py",
                    "simple_lighting_evaluator.py",
                    "realistic_lighting_evaluator.py"
                ]
            },
            "scripts": {
                "description": "Utility and setup scripts",
                "files": [
                    "start_chat_system.py",
                    "start_pdf_analyzer.py",
                    "run_accuracy_improvements.py",
                    "improve_accuracy.py",
                    "add_more_standards_data.py",
                    "improve_standards_extraction.py",
                    "auto_process.py",
                    "process_pdfs.py",
                    "process_standards.py"
                ]
            },
            "evaluators": {
                "description": "Lighting evaluation tools",
                "files": [
                    "evaluate_lighting_report.py",
                    "batch_pdf_evaluator.py",
                    "quick_batch_evaluator.py",
                    "quick_realistic_evaluator.py",
                    "demo_lighting_evaluation.py",
                    "demo_simple_evaluator.py"
                ]
            },
            "processors": {
                "description": "Specialized processors",
                "files": [
                    "dialux_pdf_processor.py",
                    "enhanced_dialux_processor.py",
                    "create_sample_processed.py"
                ]
            },
            "tests": {
                "description": "Test files and examples",
                "files": [
                    "test_batch_analyzer.py",
                    "test_chat_api.py",
                    "test_dialux_processor.py",
                    "test_system.py",
                    "simple_test.py",
                    "accuracy_test.py"
                ]
            },
            "web": {
                "description": "Web interface files",
                "files": [
                    "chat_web.html"
                ]
            },
            "docs": {
                "description": "Documentation",
                "files": [
                    "CHAT_SYSTEM_README.md",
                    "PDF_STUDY_ANALYZER_README.md",
                    "ACCURACY_IMPROVEMENT_GUIDE.md",
                    "USAGE_GUIDE.md"
                ]
            },
            "configs": {
                "description": "Configuration files",
                "keep_existing": True
            },
            "outputs": {
                "description": "Output and results",
                "keep_existing": True
            },
            "logs": {
                "description": "Log files",
                "keep_existing": True
            },
            "temp": {
                "description": "Temporary files to clean up",
                "files": [
                    "out.json",
                    "accuracy_report.json",
                    "requirements-fixed.txt",
                    "requirements-resolved.txt",
                    "-p",
                    "=0.14.0",
                    "=0.27.0",
                    "=1.0.0",
                    "process.bat"
                ]
            }
        }
    
    def organize_files(self, dry_run: bool = True):
        """Organize files according to the structure"""
        print("🗂️  FILE ORGANIZATION")
        print("=" * 50)
        
        if dry_run:
            print("🔍 DRY RUN MODE - No files will be moved")
        else:
            print("🚀 LIVE MODE - Files will be moved")
        
        print()
        
        # Create directory structure
        self._create_directories(dry_run)
        
        # Move files to appropriate directories
        self._move_files(dry_run)
        
        # Clean up temporary files
        self._cleanup_temp_files(dry_run)
        
        # Organize data files
        self._organize_data_files(dry_run)
        
        # Create organization report
        self._create_organization_report()
        
        print("\n✅ File organization completed!")
        if dry_run:
            print("💡 Run with --live to actually move files")
    
    def _create_directories(self, dry_run: bool):
        """Create directory structure"""
        print("📁 Creating directory structure...")
        
        for dir_name, config in self.organized_structure.items():
            if config.get("keep_existing", False):
                continue
            
            dir_path = self.root_dir / dir_name
            if not dry_run:
                dir_path.mkdir(exist_ok=True)
            
            print(f"  📂 {dir_name}/ - {config['description']}")
            
            # Create subdirectories
            if "subdirs" in config:
                for subdir_name, subdir_desc in config["subdirs"].items():
                    subdir_path = dir_path / subdir_name
                    if not dry_run:
                        subdir_path.mkdir(exist_ok=True)
                    print(f"    📁 {subdir_name}/ - {subdir_desc}")
    
    def _move_files(self, dry_run: bool):
        """Move files to appropriate directories"""
        print("\n📦 Moving files...")
        
        for dir_name, config in self.organized_structure.items():
            if config.get("keep_existing", False):
                continue
            
            if "files" not in config:
                continue
            
            target_dir = self.root_dir / dir_name
            
            for file_name in config["files"]:
                source_path = self.root_dir / file_name
                target_path = target_dir / file_name
                
                if source_path.exists():
                    if not dry_run:
                        shutil.move(str(source_path), str(target_path))
                    print(f"  📄 {file_name} → {dir_name}/")
                else:
                    print(f"  ⚠️  {file_name} not found")
    
    def _cleanup_temp_files(self, dry_run: bool):
        """Clean up temporary and unnecessary files"""
        print("\n🧹 Cleaning up temporary files...")
        
        temp_files = self.organized_structure["temp"]["files"]
        
        for file_name in temp_files:
            file_path = self.root_dir / file_name
            if file_path.exists():
                if not dry_run:
                    if file_path.is_file():
                        file_path.unlink()
                    elif file_path.is_dir():
                        shutil.rmtree(file_path)
                print(f"  🗑️  Removed: {file_name}")
    
    def _organize_data_files(self, dry_run: bool):
        """Organize data files into proper structure"""
        print("\n📊 Organizing data files...")
        
        # Move standards PDFs
        base_dir = self.root_dir / "base"
        if base_dir.exists():
            standards_dir = self.root_dir / "data" / "standards"
            if not dry_run:
                standards_dir.mkdir(exist_ok=True)
            
            for pdf_file in base_dir.glob("*.pdf"):
                target_path = standards_dir / pdf_file.name
                if not dry_run:
                    shutil.move(str(pdf_file), str(target_path))
                print(f"  📄 {pdf_file.name} → data/standards/")
        
        # Move report PDFs
        data_dir = self.root_dir / "data"
        if data_dir.exists():
            reports_dir = self.root_dir / "data" / "reports"
            if not dry_run:
                reports_dir.mkdir(exist_ok=True)
            
            for pdf_file in data_dir.glob("*.pdf"):
                target_path = reports_dir / pdf_file.name
                if not dry_run:
                    shutil.move(str(pdf_file), str(target_path))
                print(f"  📄 {pdf_file.name} → data/reports/")
        
        # Move processed data
        uploads_dir = self.root_dir / "uploads"
        if uploads_dir.exists():
            processed_dir = self.root_dir / "data" / "processed"
            if not dry_run:
                processed_dir.mkdir(exist_ok=True)
            
            for json_file in uploads_dir.glob("*.json"):
                target_path = processed_dir / json_file.name
                if not dry_run:
                    shutil.move(str(json_file), str(target_path))
                print(f"  📄 {json_file.name} → data/processed/")
        
        # Move study results
        studies_dir = self.root_dir / "studies"
        if studies_dir.exists():
            target_studies_dir = self.root_dir / "data" / "studies"
            if not dry_run:
                target_studies_dir.mkdir(exist_ok=True)
            
            for json_file in studies_dir.glob("*.json"):
                target_path = target_studies_dir / json_file.name
                if not dry_run:
                    shutil.move(str(json_file), str(target_path))
                print(f"  📄 {json_file.name} → data/studies/")
    
    def _create_organization_report(self):
        """Create organization report"""
        report = {
            "organization_date": datetime.now().isoformat(),
            "structure": self.organized_structure,
            "recommendations": [
                "Keep core files in root directory for easy access",
                "Use tools/ directory for analysis tools",
                "Store all data in data/ directory with subdirectories",
                "Keep documentation in docs/ directory",
                "Use scripts/ for utility scripts",
                "Clean up temporary files regularly"
            ]
        }
        
        report_path = self.root_dir / "organization_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n📋 Organization report saved to: {report_path}")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Organize project files")
    parser.add_argument("--live", action="store_true", help="Actually move files (default is dry run)")
    
    args = parser.parse_args()
    
    organizer = FileOrganizer()
    organizer.organize_files(dry_run=not args.live)

if __name__ == "__main__":
    main()
