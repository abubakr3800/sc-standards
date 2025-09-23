"""
Resolve dependency conflicts for AI Standards Training System
Uses alternative packages to avoid conflicts
"""
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def resolve_dependencies():
    """Resolve dependency conflicts using alternative packages"""
    print("🔧 Resolving dependency conflicts...")
    print("=" * 50)
    
    # Step 1: Uninstall problematic packages
    print("Step 1: Uninstalling problematic packages")
    packages_to_remove = ["googletrans", "httpx", "httpcore", "h11"]
    
    for package in packages_to_remove:
        run_command(f"pip uninstall {package} -y", f"Uninstalling {package}")
    
    # Step 2: Install resolved requirements
    print("\nStep 2: Installing resolved requirements")
    if not run_command("pip install -r requirements-resolved.txt", "Installing resolved requirements"):
        return False
    
    return True

def verify_installation():
    """Verify that all packages are installed correctly"""
    print("\n🔍 Verifying installation...")
    
    test_imports = [
        ("deep_translator", "deep-translator"),
        ("httpx", "httpx"),
        ("chromadb", "ChromaDB"),
        ("torch", "PyTorch"),
        ("transformers", "Transformers"),
        ("sentence_transformers", "Sentence Transformers"),
        ("streamlit", "Streamlit"),
        ("fastapi", "FastAPI"),
        ("pdfplumber", "PDF Plumber"),
        ("spacy", "spaCy")
    ]
    
    failed_imports = []
    
    for module, name in test_imports:
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError as e:
            print(f"❌ {name}: {e}")
            failed_imports.append(name)
    
    if failed_imports:
        print(f"\n⚠️  Some packages failed to import: {', '.join(failed_imports)}")
        return False
    else:
        print("\n✅ All packages imported successfully!")
        return True

def test_translation():
    """Test the new translation functionality"""
    print("\n🧪 Testing translation functionality...")
    
    try:
        from deep_translator import GoogleTranslator
        
        # Test translation
        translator = GoogleTranslator(source='auto', target='en')
        test_text = "Bonjour le monde"
        result = translator.translate(test_text)
        
        print(f"✅ Translation test successful: '{test_text}' -> '{result}'")
        return True
        
    except Exception as e:
        print(f"❌ Translation test failed: {e}")
        return False

def main():
    """Main function"""
    print("🚀 AI Standards Training System - Dependency Resolver")
    print("=" * 60)
    
    try:
        # Resolve dependencies
        if resolve_dependencies():
            print("\n✅ Dependencies resolved successfully!")
            
            # Verify installation
            if verify_installation():
                print("\n✅ All packages are working correctly!")
                
                # Test translation
                if test_translation():
                    print("\n🎉 Translation functionality is working!")
                    print("\nYou can now run:")
                    print("  python main.py process")
                    print("  python main.py train")
                    print("  python main.py web")
                else:
                    print("\n⚠️  Translation may not work properly.")
            else:
                print("\n⚠️  Some packages may still have issues.")
        else:
            print("\n❌ Failed to resolve dependencies.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⚠️  Resolution cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
