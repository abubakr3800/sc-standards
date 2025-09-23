"""
Start PDF Study Analyzer
Start the PDF study analyzer system
"""
import subprocess
import sys
import webbrowser
import time
from pathlib import Path

def main():
    """Start the PDF study analyzer system"""
    print("🚀 STARTING PDF STUDY ANALYZER")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("pdf_study_analyzer.py").exists():
        print("❌ Please run this script from the project root directory")
        return
    
    print("📊 PDF Study Analyzer System")
    print("=" * 50)
    print("Choose an option:")
    print("1. 🌐 Web Interface (Streamlit)")
    print("2. 🔍 Analyze Single PDF (Command Line)")
    print("3. 📁 Batch Analyze Folder (Command Line)")
    print("4. 🧪 Test with Existing PDFs")
    print("5. ❌ Exit")
    print()
    
    choice = input("Enter your choice (1-5): ").strip()
    
    if choice == "1":
        start_web_interface()
    elif choice == "2":
        analyze_single_pdf()
    elif choice == "3":
        batch_analyze_folder()
    elif choice == "4":
        test_with_existing_pdfs()
    elif choice == "5":
        print("👋 Goodbye!")
        return
    else:
        print("❌ Invalid choice. Please try again.")
        main()

def start_web_interface():
    """Start the Streamlit web interface"""
    print("🌐 Starting web interface...")
    try:
        subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "upload_study_analyzer.py",
            "--server.port", "8502",
            "--server.headless", "true"
        ])
        
        time.sleep(3)
        print("✅ Web interface started on http://localhost:8502")
        print("🌐 Opening browser...")
        webbrowser.open("http://localhost:8502")
        
    except Exception as e:
        print(f"❌ Error starting web interface: {e}")

def analyze_single_pdf():
    """Analyze a single PDF file"""
    print("🔍 Single PDF Analysis")
    print("=" * 30)
    
    pdf_path = input("Enter path to PDF file: ").strip()
    if not pdf_path:
        print("❌ No file path provided")
        return
    
    output_format = input("Output format (summary/json) [summary]: ").strip() or "summary"
    
    try:
        subprocess.run([
            sys.executable, "analyze_study.py", pdf_path, "--format", output_format
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error analyzing PDF: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def batch_analyze_folder():
    """Batch analyze a folder of PDFs"""
    print("📁 Batch PDF Analysis")
    print("=" * 30)
    
    folder_path = input("Enter path to folder containing PDFs: ").strip()
    if not folder_path:
        print("❌ No folder path provided")
        return
    
    recursive = input("Search subdirectories? (y/n) [n]: ").strip().lower() == 'y'
    
    output_file = input("Output file path (optional): ").strip()
    
    try:
        cmd = [sys.executable, "batch_study_analyzer.py", folder_path]
        if recursive:
            cmd.append("--recursive")
        if output_file:
            cmd.extend(["--output", output_file])
        
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in batch analysis: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def test_with_existing_pdfs():
    """Test with existing PDFs in the base folder"""
    print("🧪 Testing with Existing PDFs")
    print("=" * 30)
    
    base_dir = Path("base")
    if not base_dir.exists():
        print("❌ base/ directory not found")
        return
    
    pdf_files = list(base_dir.glob("*.pdf"))
    if not pdf_files:
        print("❌ No PDF files found in base/ directory")
        return
    
    print(f"📁 Found {len(pdf_files)} PDF files in base/ directory")
    print("Files:")
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"  {i}. {pdf_file.name}")
    
    print("\n🔍 Analyzing all PDFs...")
    try:
        subprocess.run([
            sys.executable, "batch_study_analyzer.py", "base", "--format", "summary"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in batch analysis: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
