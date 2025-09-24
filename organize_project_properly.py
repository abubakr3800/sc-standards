"""
Proper Project Organization
Organizes files and folders correctly with proper structure
"""
import shutil
import os
from pathlib import Path
import json
from datetime import datetime

class ProperProjectOrganizer:
    """Properly organizes the project with correct structure"""
    
    def __init__(self):
        self.root_dir = Path(".")
        
        # Create proper directory structure
        self.directories = {
            "processing": "src/ai_standards/processing/",
            "tests": "tests/",
            "temp_cleanup": "temp_cleanup/"
        }
        
        # Files to move to processing directory
        self.processing_files = [
            "improve_standards_extraction.py",
            "process_pdfs.py", 
            "process_standards.py",
            "enhanced_dialux_extractor.py"
        ]
        
        # Test files to organize
        self.test_files = [
            "test_batch_analyzer.py",
            "test_chat_api.py", 
            "test_dialux_processor.py",
            "test_system.py",
            "accuracy_test.py",
            "simple_test.py"
        ]
        
        # Files to remove (temporary/duplicate)
        self.files_to_remove = [
            "debug_detailed.py",
            "debug_processing.py",
            "demo_usage.py",
            "process.bat",
            "organize_files.py",
            "quick_organize.py",
            "filter_essential_files.py",
            "ESSENTIAL_FILES_GUIDE.md",
            "essential_filtering_summary.json",
            "PROJECT_ORGANIZATION.md",
            "USAGE_GUIDE.md",
            "ACCURACY_IMPROVEMENT_GUIDE.md",
            "CHAT_SYSTEM_README.md",
            "PDF_STUDY_ANALYZER_README.md",
            "temp/",
            "__pycache__/",
            "-p",
            "=0.14.0",
            "=0.27.0", 
            "=1.0.0",
            "requirements-fixed.txt",
            "requirements-resolved.txt",
            "accuracy_report.json",
            "out.json"
        ]
        
        # Directories to clean up
        self.dirs_to_clean = [
            "examples/",
            "web/",
            "studies/",
            "uploads/"
        ]
    
    def organize_project(self, dry_run: bool = True):
        """Organize the project properly"""
        print("🗂️  PROPER PROJECT ORGANIZATION")
        print("=" * 50)
        
        if dry_run:
            print("🔍 DRY RUN MODE - No files will be moved")
        else:
            print("🚀 LIVE MODE - Files will be moved")
        
        print()
        
        # Create directories
        self._create_directories(dry_run)
        
        # Move processing files
        self._move_processing_files(dry_run)
        
        # Organize test files
        self._organize_test_files(dry_run)
        
        # Clean up unnecessary files
        self._cleanup_files(dry_run)
        
        # Clean up directories
        self._cleanup_directories(dry_run)
        
        # Update Makefile to use py instead of python
        self._update_makefile(dry_run)
        
        # Generate organization report
        self._generate_report()
        
        print("\n✅ Project organization completed!")
        if dry_run:
            print("💡 Run with --live to actually organize files")
    
    def _create_directories(self, dry_run: bool):
        """Create proper directory structure"""
        print("📁 Creating proper directory structure...")
        
        for dir_name, dir_path in self.directories.items():
            full_path = self.root_dir / dir_path
            if not dry_run:
                full_path.mkdir(parents=True, exist_ok=True)
            print(f"  📂 {dir_path}")
    
    def _move_processing_files(self, dry_run: bool):
        """Move processing files to proper location"""
        print("\n🔄 Moving processing files...")
        
        processing_dir = self.root_dir / "src/ai_standards/processing"
        
        for file_name in self.processing_files:
            source_path = self.root_dir / file_name
            target_path = processing_dir / file_name
            
            if source_path.exists():
                if not dry_run:
                    shutil.move(str(source_path), str(target_path))
                print(f"  📄 {file_name} → src/ai_standards/processing/")
            else:
                print(f"  ⚠️  {file_name} not found")
    
    def _organize_test_files(self, dry_run: bool):
        """Organize test files properly"""
        print("\n🧪 Organizing test files...")
        
        tests_dir = self.root_dir / "tests"
        
        for file_name in self.test_files:
            source_path = self.root_dir / file_name
            target_path = tests_dir / file_name
            
            if source_path.exists():
                if not dry_run:
                    shutil.move(str(source_path), str(target_path))
                print(f"  📄 {file_name} → tests/")
            else:
                print(f"  ⚠️  {file_name} not found")
    
    def _cleanup_files(self, dry_run: bool):
        """Clean up unnecessary files"""
        print("\n🗑️  Cleaning up unnecessary files...")
        
        removed_count = 0
        for file_pattern in self.files_to_remove:
            if file_pattern.endswith("/"):
                # Directory
                dir_path = self.root_dir / file_pattern.rstrip("/")
                if dir_path.exists():
                    if not dry_run:
                        shutil.rmtree(dir_path)
                    print(f"  🗂️  Removed: {file_pattern}")
                    removed_count += 1
            else:
                # File
                file_path = self.root_dir / file_pattern
                if file_path.exists():
                    if not dry_run:
                        file_path.unlink()
                    print(f"  📄 Removed: {file_pattern}")
                    removed_count += 1
        
        print(f"  📊 Removed {removed_count} files/directories")
    
    def _cleanup_directories(self, dry_run: bool):
        """Clean up empty directories"""
        print("\n🧹 Cleaning up empty directories...")
        
        for dir_name in self.dirs_to_clean:
            dir_path = self.root_dir / dir_name.rstrip("/")
            if dir_path.exists():
                if not dry_run:
                    shutil.rmtree(dir_path)
                print(f"  🗂️  Cleaned: {dir_name}")
    
    def _update_makefile(self, dry_run: bool):
        """Update Makefile to use py instead of python"""
        print("\n⚙️  Updating Makefile to use 'py' instead of 'python'...")
        
        makefile_path = self.root_dir / "Makefile"
        if makefile_path.exists():
            if not dry_run:
                # Read current Makefile
                with open(makefile_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace python with py
                updated_content = content.replace('python ', 'py ')
                updated_content = updated_content.replace('python3 ', 'py ')
                
                # Write updated Makefile
                with open(makefile_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
            
            print("  ✅ Makefile updated to use 'py' command")
        else:
            print("  ⚠️  Makefile not found")
    
    def _generate_report(self):
        """Generate organization report"""
        report = {
            "organization_date": datetime.now().isoformat(),
            "directories_created": list(self.directories.values()),
            "processing_files_moved": self.processing_files,
            "test_files_organized": self.test_files,
            "files_removed": self.files_to_remove,
            "directories_cleaned": self.dirs_to_clean,
            "makefile_updated": "Changed 'python' to 'py'",
            "final_structure": {
                "src/ai_standards/processing/": "Processing files for base PDFs and database creation",
                "tests/": "All test files organized",
                "src/ai_standards/": "Core source code",
                "tools/": "Main analysis tools",
                "evaluators/": "Lighting evaluation tools",
                "scripts/": "Utility scripts",
                "data/": "Data storage",
                "structure/": "Documentation"
            }
        }
        
        report_path = self.root_dir / "organization_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n📋 Organization report saved to: {report_path}")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Properly organize project files")
    parser.add_argument("--live", action="store_true", help="Actually organize files (default is dry run)")
    
    args = parser.parse_args()
    
    organizer = ProperProjectOrganizer()
    organizer.organize_project(dry_run=not args.live)

if __name__ == "__main__":
    main()
