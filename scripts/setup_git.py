"""
Git repository setup script for AI Standards Training System
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
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def setup_git_repository():
    """Setup Git repository with proper configuration"""
    print("🚀 Setting up Git repository for AI Standards Training System")
    print("=" * 60)
    
    # Check if git is installed
    if not run_command("git --version", "Checking Git installation"):
        print("❌ Git is not installed. Please install Git first.")
        return False
    
    # Initialize git repository if not already initialized
    if not Path(".git").exists():
        if not run_command("git init", "Initializing Git repository"):
            return False
    else:
        print("✅ Git repository already initialized")
    
    # Add remote origin
    remote_url = "https://github.com/abubakr3800/sc-standards.git"
    if not run_command(f"git remote add origin {remote_url}", "Adding remote origin"):
        # Try to update existing remote
        run_command(f"git remote set-url origin {remote_url}", "Updating remote origin")
    
    # Configure git user (if not already configured)
    run_command('git config user.name "Short Circuit Company"', "Setting Git user name")
    run_command('git config user.email "Scc@shortcircuitcompany.com"', "Setting Git user email")
    
    # Add all files
    if not run_command("git add .", "Adding all files to Git"):
        return False
    
    # Create initial commit
    if not run_command('git commit -m "Initial commit: AI Standards Training System"', "Creating initial commit"):
        return False
    
    print("\n" + "=" * 60)
    print("✅ Git repository setup completed!")
    print("\nNext steps:")
    print("1. Push to GitHub: git push -u origin main")
    print("2. Or push to master: git push -u origin master")
    print("3. Set up GitHub Actions for CI/CD")
    print("4. Configure branch protection rules")
    
    return True

def main():
    """Main function"""
    try:
        success = setup_git_repository()
        if success:
            print("\n🎉 Git repository is ready!")
        else:
            print("\n❌ Git setup failed. Please check the errors above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️  Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
