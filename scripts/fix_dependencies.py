"""
Fix dependency conflicts for AI Standards Training System
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
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def fix_dependency_conflicts():
    """Fix dependency conflicts by upgrading/downgrading packages"""
    print("🔧 Fixing dependency conflicts...")
    print("=" * 50)
    
    # Step 1: Uninstall conflicting packages
    print("Step 1: Uninstalling conflicting packages")
    packages_to_remove = ["httpx", "httpcore", "h11", "chromadb", "googletrans"]
    
    for package in packages_to_remove:
        run_command(f"pip uninstall {package} -y", f"Uninstalling {package}")
    
    # Step 2: Install compatible versions
    print("\nStep 2: Installing compatible versions")
    
    # Install httpx first with correct version
    if not run_command("pip install httpx>=0.27.0", "Installing httpx>=0.27.0"):
        return False
    
    # Install httpcore
    if not run_command("pip install httpcore>=1.0.0", "Installing httpcore>=1.0.0"):
        return False
    
    # Install h11
    if not run_command("pip install h11>=0.14.0", "Installing h11>=0.14.0"):
        return False
    
    # Install compatible ChromaDB version
    if not run_command("pip install 'chromadb>=0.3.0,<1.1.0'", "Installing compatible ChromaDB"):
        return False
    
    # Install compatible googletrans
    if not run_command("pip install googletrans==3.1.0a0", "Installing compatible googletrans"):
        return False
    
    # Step 3: Install remaining requirements
    print("\nStep 3: Installing remaining requirements")
    if not run_command("pip install -r requirements-fixed.txt", "Installing fixed requirements"):
        return False
    
    return True

def verify_installation():
    """Verify that all packages are installed correctly"""
    print("\n🔍 Verifying installation...")
    
    test_imports = [
        ("httpx", "httpx"),
        ("httpcore", "httpcore"),
        ("h11", "h11"),
        ("chromadb", "ChromaDB"),
        ("googletrans", "googletrans"),
        ("torch", "PyTorch"),
        ("transformers", "Transformers"),
        ("sentence_transformers", "Sentence Transformers"),
        ("streamlit", "Streamlit"),
        ("fastapi", "FastAPI")
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

def main():
    """Main function"""
    print("🚀 AI Standards Training System - Dependency Conflict Fixer")
    print("=" * 60)
    
    try:
        # Fix dependencies
        if fix_dependency_conflicts():
            print("\n✅ Dependency conflicts fixed successfully!")
            
            # Verify installation
            if verify_installation():
                print("\n🎉 All dependencies are working correctly!")
                print("\nYou can now run:")
                print("  python main.py process")
                print("  python main.py train")
                print("  python main.py web")
            else:
                print("\n⚠️  Some packages may still have issues. Please check the errors above.")
        else:
            print("\n❌ Failed to fix dependency conflicts. Please check the errors above.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⚠️  Fix cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
