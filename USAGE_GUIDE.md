# 🚀 AI Standards System - Usage Guide

## 📋 How to Use the Trained System

### 1. **Web Interface (Recommended)**

Start the web interface for easy interaction:

```bash
make web
# or
python main.py web
```

Then open your browser to: **http://localhost:8501**

**Features:**
- 📄 Upload new PDF standards
- 🔍 Search through existing standards
- 📊 Compare two standards side-by-side
- 📈 View similarity scores and recommendations
- 📋 Export comparison results

### 2. **API Interface**

Start the REST API for integration:

```bash
make run-api
# or
python main.py api
```

API will be available at: **http://localhost:8000**

**Key Endpoints:**
- `POST /compare` - Compare two standards
- `GET /search` - Search standards by query
- `POST /upload` - Upload new PDF for processing
- `GET /standards` - List all processed standards

### 3. **Command Line Interface**

#### Compare Standards:
```bash
make compare --standard-a "prEN 12464-1" --standard-b "BREEAM"
# or
python main.py compare --standard-a "prEN 12464-1" --standard-b "BREEAM"
```

#### Process New PDFs:
```bash
make auto-process
# or
python auto_process.py
```

#### Train/Retrain Models:
```bash
make train
# or
python main.py train
```

### 4. **Programmatic Usage**

```python
from ai_standards.models.comparison_model import StandardsComparisonModel

# Initialize the model
model = StandardsComparisonModel()

# Compare two standards
result = model.compare_standards(doc1, doc2)

# Get results
print(f"Similarity: {result.overall_similarity:.2%}")
print(f"Matching categories: {result.matching_categories}")
print(f"Differences: {result.differences}")
print(f"Recommendations: {result.recommendations}")

# Search standards
results = model.search_standards("illuminance requirements", top_k=5)
for doc, score in results:
    print(f"{doc['file_name']}: {score:.3f}")
```

## 🧪 Testing System Accuracy

### 1. **Run Accuracy Tests**

```bash
python accuracy_test.py
```

This will test:
- ✅ Basic functionality
- ✅ Comparison accuracy
- ✅ Search accuracy
- ✅ Document processing

### 2. **Run Comprehensive Tests**

```bash
python test_system.py
```

This will test:
- 🔍 Standards comparison
- 🔎 Semantic search
- 🏷️ Category classification
- 📊 Overall system performance

### 3. **Manual Testing**

#### Test 1: Compare Known Standards
```python
# Load two processed documents
with open('uploads/prEN 12464-1_processed.json', 'r') as f:
    doc1 = json.load(f)

with open('uploads/BREEAM_processed.json', 'r') as f:
    doc2 = json.load(f)

# Compare them
result = model.compare_standards(doc1, doc2)
print(f"Similarity: {result.overall_similarity:.2%}")
```

#### Test 2: Search for Specific Terms
```python
# Search for lighting requirements
results = model.search_standards("illuminance 500 lux", top_k=3)
for doc, score in results:
    print(f"{doc['file_name']}: {score:.3f}")
```

#### Test 3: Test Category Detection
```python
# Test if system correctly identifies categories
text = "Office work requires 500 lux illuminance"
categories = model.classify_categories(text)
print(f"Detected categories: {categories}")
# Should include: ['illuminance']
```

## 📊 Evaluating Accuracy

### **What to Look For:**

1. **Similarity Scores** (0-100%)
   - 80-100%: Very similar standards
   - 60-79%: Moderately similar
   - 40-59%: Some similarities
   - 0-39%: Very different

2. **Category Matching**
   - Should correctly identify: illuminance, color_rendering, glare_control, energy_efficiency
   - Should match related standards (e.g., EN 12464-1 and BREEAM both have lighting requirements)

3. **Search Results**
   - Should return relevant documents for lighting-related queries
   - Higher scores for more relevant matches

4. **Recommendations**
   - Should provide actionable insights
   - Should identify key differences between standards

### **Expected Results:**

For your current standards:
- **EN 12464-1** vs **BREEAM**: Should show 60-80% similarity (both lighting standards)
- **Search "illuminance"**: Should return both documents with high scores
- **Search "energy efficiency"**: Should return both documents
- **Categories**: Should detect illuminance, energy_efficiency, glare_control

## 🔧 Troubleshooting

### **If Training Fails:**
```bash
# Check if processed documents exist
ls uploads/*_processed.json

# If not, process PDFs first
make auto-process

# Then retrain
make train
```

### **If Comparison Fails:**
```bash
# Check if models exist
ls models/

# If not, train models first
make train
```

### **If Search Returns No Results:**
```bash
# Check if vector database exists
ls data/

# If not, retrain models
make train
```

## 🎯 Best Practices

1. **Regular Updates**: Process new PDFs and retrain models regularly
2. **Quality PDFs**: Use high-quality, text-based PDFs (not scanned images)
3. **Consistent Naming**: Use descriptive names for your PDF files
4. **Backup Data**: Keep backups of your processed documents and models
5. **Monitor Performance**: Run accuracy tests after major updates

## 📈 Performance Metrics

### **Good Performance Indicators:**
- ✅ Similarity scores between 0.6-0.9 for related standards
- ✅ Search returns relevant results in top 3
- ✅ Category classification accuracy > 80%
- ✅ Processing time < 30 seconds per PDF

### **Red Flags:**
- ❌ All similarity scores are 0 or 1
- ❌ Search returns no results for common terms
- ❌ Category classification accuracy < 50%
- ❌ Processing fails for standard PDFs

## 🚀 Next Steps

1. **Start with Web Interface**: `make web`
2. **Upload Test PDFs**: Add more standards to `base/` folder
3. **Process and Train**: `make auto-process && make train`
4. **Test Accuracy**: `python accuracy_test.py`
5. **Use for Real Work**: Compare your actual standards!

---

**Need Help?** Check the logs in the `logs/` directory or run `python test_system.py` for detailed diagnostics.
