# 🗂️ Project Organization Guide

## 📁 Recommended Project Structure

```
standards/
├── 📄 Core Files (Root Level)
│   ├── main.py                    # Main entry point
│   ├── requirements.txt           # Dependencies
│   ├── README.md                  # Project documentation
│   ├── setup.cfg                  # Setup configuration
│   └── LICENSE                    # License file
│
├── 📂 src/                        # Source code modules
│   └── ai_standards/              # Main package
│       ├── core/                  # Core functionality
│       ├── models/                # AI models
│       ├── evaluators/            # Evaluation modules
│       ├── processors/            # Processing modules
│       └── web/                   # Web interfaces
│
├── 📂 data/                       # All data files
│   ├── standards/                 # Original standards PDFs
│   ├── reports/                   # User uploaded reports
│   ├── processed/                 # Processed JSON data
│   └── studies/                   # Analysis results
│
├── 📂 tools/                      # Analysis tools
│   ├── pdf_study_analyzer.py      # PDF analysis tool
│   ├── batch_study_analyzer.py    # Batch analysis
│   ├── enhanced_chat_api.py       # Chat API
│   └── lighting_evaluators.py     # Evaluation tools
│
├── 📂 scripts/                    # Utility scripts
│   ├── start_chat_system.py       # Start chat system
│   ├── start_pdf_analyzer.py      # Start PDF analyzer
│   └── setup_*.py                 # Setup scripts
│
├── 📂 docs/                       # Documentation
│   ├── README.md                  # Main documentation
│   ├── CHAT_SYSTEM_README.md      # Chat system docs
│   └── PDF_STUDY_ANALYZER_README.md
│
├── 📂 configs/                    # Configuration files
│   └── env_template               # Environment template
│
├── 📂 outputs/                    # Output files
├── 📂 logs/                       # Log files
└── 📂 tests/                      # Test files
```

## 🚀 Quick Organization

### **Option 1: Automatic Organization**
```bash
# Preview organization (dry run)
python organize_files.py

# Actually organize files
python organize_files.py --live
```

### **Option 2: Manual Organization**
Follow the structure above and move files manually.

## 📊 Current File Status

### **✅ Well Organized:**
- `src/` - Source code modules
- `configs/` - Configuration files
- `docs/` - Documentation files
- `tests/` - Test files

### **🔄 Needs Organization:**
- **Root level files** - Many tools and scripts scattered
- **Data files** - PDFs and JSON files in multiple locations
- **Temporary files** - `out.json`, `accuracy_report.json`, etc.

### **🗑️ Files to Clean Up:**
- `out.json` (8132 lines) - Move to `data/studies/`
- `accuracy_report.json` - Move to `outputs/`
- `requirements-fixed.txt` - Temporary file
- `requirements-resolved.txt` - Temporary file
- Various `=0.14.0`, `=0.27.0` files - Temporary files

## 🎯 Organization Benefits

### **Before Organization:**
- ❌ 100+ files in root directory
- ❌ Hard to find specific tools
- ❌ Data scattered across multiple folders
- ❌ Temporary files cluttering workspace

### **After Organization:**
- ✅ Clean root directory with only essential files
- ✅ Logical grouping of related files
- ✅ Easy to find and use tools
- ✅ Clear data structure
- ✅ Professional project appearance

## 📋 File Categories

### **Core Files (Root Level)**
- `main.py` - Main entry point
- `requirements.txt` - Dependencies
- `README.md` - Project documentation
- `setup.cfg` - Setup configuration
- `LICENSE` - License file

### **Tools Directory**
- PDF analysis tools
- Chat system tools
- Evaluation tools
- Batch processing tools

### **Scripts Directory**
- Startup scripts
- Setup scripts
- Utility scripts
- Automation scripts

### **Data Directory**
- `standards/` - Original standards PDFs
- `reports/` - User uploaded reports
- `processed/` - Processed JSON data
- `studies/` - Analysis results

### **Documentation Directory**
- System documentation
- Usage guides
- API documentation
- Setup guides

## 🔧 Maintenance

### **Regular Cleanup:**
1. **Move new files** to appropriate directories
2. **Clean temporary files** regularly
3. **Update documentation** when adding new tools
4. **Keep data organized** in proper subdirectories

### **File Naming Conventions:**
- **Tools**: `*_analyzer.py`, `*_evaluator.py`
- **Scripts**: `start_*.py`, `setup_*.py`
- **Data**: `*_processed.json`, `*_analysis.json`
- **Docs**: `*_README.md`, `*_GUIDE.md`

## 🚀 Quick Start After Organization

### **1. Start Chat System:**
```bash
python scripts/start_chat_system.py
```

### **2. Analyze PDF Studies:**
```bash
python tools/pdf_study_analyzer.py
```

### **3. Batch Process Reports:**
```bash
python tools/batch_study_analyzer.py data/reports/ --recursive
```

### **4. View Documentation:**
```bash
# Open docs/README.md for main documentation
# Open docs/CHAT_SYSTEM_README.md for chat system
# Open docs/PDF_STUDY_ANALYZER_README.md for PDF analyzer
```

## 📈 Organization Results

After organization, you'll have:
- **Clean root directory** with only essential files
- **Logical file grouping** for easy navigation
- **Professional structure** suitable for sharing
- **Easy maintenance** and updates
- **Clear separation** of concerns

**Ready to organize your project? Run: `python organize_files.py --live`** 🎉
