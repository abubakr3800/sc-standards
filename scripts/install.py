"""
Installation script for AI Standards Training System
Handles Python version compatibility and dependency installation
"""
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    
    if version.major == 3 and version.minor >= 13:
        print("⚠️  Python 3.13+ detected. Some packages may not be available.")
        print("   Consider using Python 3.8-3.12 for best compatibility.")
    
    print("✅ Python version is compatible")
    return True

def install_package(package):
    """Install a single package with error handling"""
    try:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def install_core_packages():
    """Install core packages with version compatibility"""
    print("\n📦 Installing core packages...")
    
    # Core packages with compatible versions
    core_packages = [
        "torch>=1.13.0,<3.0.0",
        "transformers>=4.21.0",
        "sentence-transformers>=2.2.0",
        "scikit-learn>=1.1.0",
        "numpy>=1.21.0",
        "pandas>=1.5.0"
    ]
    
    for package in core_packages:
        if not install_package(package):
            print(f"⚠️  Skipping {package} due to installation failure")
    
    return True

def install_pdf_packages():
    """Install PDF processing packages"""
    print("\n📄 Installing PDF processing packages...")
    
    pdf_packages = [
        "PyPDF2>=3.0.0",
        "pdfplumber>=0.7.0",
        "pymupdf>=1.20.0",
        "pdfminer.six>=20221105"
    ]
    
    for package in pdf_packages:
        install_package(package)
    
    return True

def install_nlp_packages():
    """Install NLP packages"""
    print("\n🧠 Installing NLP packages...")
    
    nlp_packages = [
        "spacy>=3.4.0",
        "nltk>=3.7.0",
        "langdetect>=1.0.9",
        "googletrans==4.0.0rc1"
    ]
    
    for package in nlp_packages:
        install_package(package)
    
    return True

def install_web_packages():
    """Install web interface packages"""
    print("\n🌐 Installing web interface packages...")
    
    web_packages = [
        "streamlit>=1.20.0",
        "fastapi>=0.95.0",
        "uvicorn>=0.20.0"
    ]
    
    for package in web_packages:
        install_package(package)
    
    return True

def install_data_packages():
    """Install data processing packages"""
    print("\n💾 Installing data processing packages...")
    
    data_packages = [
        "sqlalchemy>=1.4.0",
        "chromadb>=0.3.0",
        "faiss-cpu>=1.7.0"
    ]
    
    for package in data_packages:
        install_package(package)
    
    return True

def install_visualization_packages():
    """Install visualization packages"""
    print("\n📊 Installing visualization packages...")
    
    viz_packages = [
        "matplotlib>=3.5.0",
        "seaborn>=0.11.0",
        "plotly>=5.10.0"
    ]
    
    for package in viz_packages:
        install_package(package)
    
    return True

def install_utility_packages():
    """Install utility packages"""
    print("\n🔧 Installing utility packages...")
    
    utility_packages = [
        "tqdm>=4.64.0",
        "python-dotenv>=0.19.0",
        "pydantic>=1.10.0",
        "loguru>=0.6.0"
    ]
    
    for package in utility_packages:
        install_package(package)
    
    return True

def install_spacy_models():
    """Install spaCy language models"""
    print("\n🗣️  Installing spaCy language models...")
    
    models = [
        "en_core_web_sm",
        "de_core_news_sm", 
        "fr_core_news_sm",
        "es_core_news_sm",
        "it_core_news_sm",
        "pt_core_news_sm",
        "nl_core_news_sm"
    ]
    
    for model in models:
        try:
            print(f"Installing {model}...")
            subprocess.check_call([sys.executable, "-m", "spacy", "download", model])
            print(f"✅ {model} installed")
        except subprocess.CalledProcessError:
            print(f"⚠️  {model} installation failed (may not be available)")
    
    return True

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = [
        "data",
        "models", 
        "uploads",
        "outputs",
        "logs",
        "base"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    return True

def verify_installation():
    """Verify that key packages are installed"""
    print("\n🔍 Verifying installation...")
    
    test_imports = [
        ("torch", "PyTorch"),
        ("transformers", "Transformers"),
        ("sentence_transformers", "Sentence Transformers"),
        ("sklearn", "Scikit-learn"),
        ("numpy", "NumPy"),
        ("pandas", "Pandas"),
        ("pdfplumber", "PDF Plumber"),
        ("fitz", "PyMuPDF"),
        ("spacy", "spaCy"),
        ("streamlit", "Streamlit"),
        ("fastapi", "FastAPI"),
        ("chromadb", "ChromaDB"),
        ("matplotlib", "Matplotlib"),
        ("plotly", "Plotly")
    ]
    
    failed_imports = []
    
    for module, name in test_imports:
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name}")
            failed_imports.append(name)
    
    if failed_imports:
        print(f"\n⚠️  Some packages failed to import: {', '.join(failed_imports)}")
        print("   You may need to install them manually or check for compatibility issues.")
    else:
        print("\n✅ All packages imported successfully!")
    
    return len(failed_imports) == 0

def main():
    """Main installation function"""
    print("🚀 AI Standards Training System - Installation")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create directories
    create_directories()
    
    # Install packages in groups
    install_core_packages()
    install_pdf_packages()
    install_nlp_packages()
    install_web_packages()
    install_data_packages()
    install_visualization_packages()
    install_utility_packages()
    
    # Install spaCy models
    install_spacy_models()
    
    # Verify installation
    success = verify_installation()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ Installation completed successfully!")
    else:
        print("⚠️  Installation completed with some issues.")
    
    print("\nNext steps:")
    print("1. Place your PDF standards files in the 'base/' folder")
    print("2. Run: python main.py process")
    print("3. Run: python main.py train")
    print("4. Run: python main.py web (for web interface)")
    print("5. Or run: python main.py demo (for complete demo)")
    
    return success

if __name__ == "__main__":
    main()
