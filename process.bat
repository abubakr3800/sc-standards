@echo off
echo 🚀 AI Standards Processing System
echo ========================================

echo 📁 Checking directories...
if not exist "base" (
    echo ❌ Base directory does not exist
    pause
    exit /b 1
)

if not exist "uploads" mkdir uploads

echo 📄 Processing PDFs from base/ folder...
python auto_process.py

echo.
echo ✅ Processing completed!
echo 💡 You can now run: python main.py train
pause
