"""
Run Accuracy Improvements
Simple script to run all accuracy improvements
"""
import subprocess
import sys
from pathlib import Path

def main():
    """Run accuracy improvements"""
    print("🚀 RUNNING ACCURACY IMPROVEMENTS")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("❌ Please run this script from the project root directory")
        return
    
    # Run the accuracy improvement script
    try:
        subprocess.run([sys.executable, "improve_accuracy.py"], check=True)
        print("\n✅ ACCURACY IMPROVEMENTS COMPLETED!")
        print("=" * 50)
        print("🚀 Now you can use the enhanced chat system:")
        print("   • python enhanced_chat_api.py")
        print("   • python start_chat_system.py")
        print("   • python test_chat_api.py")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running accuracy improvements: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
