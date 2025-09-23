"""
Environment setup script for AI Standards Training System
Creates .env file and sets up environment
"""
import os
from pathlib import Path
import secrets

def create_env_file():
    """Create .env file from template"""
    env_template_path = Path("env_template")
    env_path = Path(".env")
    
    if env_path.exists():
        print("⚠️  .env file already exists")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("Keeping existing .env file")
            return
    
    if not env_template_path.exists():
        print("❌ env_template file not found")
        return
    
    # Read template
    with open(env_template_path, 'r') as f:
        content = f.read()
    
    # Generate secret key
    secret_key = secrets.token_urlsafe(32)
    content = content.replace("your_secret_key_here_change_this_in_production", secret_key)
    
    # Write .env file
    with open(env_path, 'w') as f:
        f.write(content)
    
    print("✅ .env file created successfully")
    print(f"   Generated secret key: {secret_key[:8]}...")

def create_directories():
    """Create necessary directories"""
    directories = [
        "data",
        "models",
        "uploads", 
        "outputs",
        "logs",
        "base"
    ]
    
    print("📁 Creating directories...")
    for directory in directories:
        dir_path = Path(directory)
        dir_path.mkdir(exist_ok=True)
        print(f"   ✅ {directory}/")
    
    # Create .gitkeep files to preserve empty directories
    for directory in directories:
        gitkeep_path = Path(directory) / ".gitkeep"
        if not gitkeep_path.exists():
            gitkeep_path.touch()

def setup_gitignore():
    """Setup .gitignore file"""
    gitignore_path = Path(".gitignore")
    if gitignore_path.exists():
        print("✅ .gitignore already exists")
    else:
        print("❌ .gitignore not found - please create it manually")

def main():
    """Main setup function"""
    print("🚀 Setting up AI Standards Training System Environment")
    print("=" * 60)
    
    # Create directories
    create_directories()
    
    # Create .env file
    create_env_file()
    
    # Check .gitignore
    setup_gitignore()
    
    print("\n" + "=" * 60)
    print("✅ Environment setup completed!")
    print("\nNext steps:")
    print("1. Review and modify .env file if needed")
    print("2. Place your PDF files in the base/ folder")
    print("3. Run: py install.py")
    print("4. Run: py main.py process")
    print("5. Run: py main.py train")

if __name__ == "__main__":
    main()

