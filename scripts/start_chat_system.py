"""
Start Chat System
Starts both the API server and web interface
"""
import subprocess
import time
import webbrowser
import os
import sys
from pathlib import Path

def start_api_server():
    """Start the FastAPI server"""
    print("🚀 Starting API server...")
    try:
        # Start the API server in the background
        process = subprocess.Popen([
            sys.executable, "chat_api.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for the server to start
        time.sleep(3)
        
        # Check if the server is running
        import requests
        try:
            response = requests.get("http://localhost:8000/")
            if response.status_code == 200:
                print("✅ API server started successfully on http://localhost:8000")
                return process
            else:
                print("❌ API server failed to start")
                return None
        except:
            print("❌ API server failed to start")
            return None
            
    except Exception as e:
        print(f"❌ Error starting API server: {e}")
        return None

def start_web_interface():
    """Start the Streamlit web interface"""
    print("🌐 Starting web interface...")
    try:
        # Start Streamlit
        subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "chat_web_interface.py",
            "--server.port", "8501",
            "--server.headless", "true"
        ])
        
        time.sleep(3)
        print("✅ Web interface started on http://localhost:8501")
        return True
        
    except Exception as e:
        print(f"❌ Error starting web interface: {e}")
        return False

def open_browser():
    """Open browser to the web interface"""
    print("🌐 Opening browser...")
    try:
        webbrowser.open("http://localhost:8501")
        print("✅ Browser opened to web interface")
    except Exception as e:
        print(f"❌ Error opening browser: {e}")

def main():
    """Main function"""
    print("=" * 60)
    print("💡 LIGHTING STANDARDS CHAT SYSTEM")
    print("=" * 60)
    
    # Check if required files exist
    required_files = ["chat_api.py", "chat_web_interface.py", "chat_web.html"]
    missing_files = [f for f in required_files if not Path(f).exists()]
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return
    
    # Start API server
    api_process = start_api_server()
    if not api_process:
        print("❌ Failed to start API server. Exiting.")
        return
    
    # Start web interface
    if not start_web_interface():
        print("❌ Failed to start web interface. Exiting.")
        return
    
    print("\n" + "=" * 60)
    print("🎉 CHAT SYSTEM STARTED SUCCESSFULLY!")
    print("=" * 60)
    print("📱 Web Interface: http://localhost:8501")
    print("🔗 API Endpoint: http://localhost:8000")
    print("📄 HTML Interface: Open chat_web.html in your browser")
    print("\n💡 You can now:")
    print("   • Ask questions about lighting standards")
    print("   • Get instant answers with confidence scores")
    print("   • View sources and recommendations")
    print("   • Use quick question buttons")
    print("\n🛑 Press Ctrl+C to stop the system")
    print("=" * 60)
    
    # Open browser
    open_browser()
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping chat system...")
        if api_process:
            api_process.terminate()
        print("✅ Chat system stopped")

if __name__ == "__main__":
    main()
