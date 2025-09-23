"""
Demo script showing table and text extraction capabilities
"""
import pdfplumber
from pathlib import Path
import pandas as pd

def extract_tables_and_text(pdf_path):
    """Extract all tables and text from a PDF"""
    print(f"📄 Processing: {pdf_path.name}")
    print("=" * 50)
    
    all_text = ""
    all_tables = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            print(f"\n📖 Page {page_num}:")
            
            # Extract text
            page_text = page.extract_text()
            if page_text:
                all_text += page_text + "\n"
                print(f"✅ Text extracted: {len(page_text)} characters")
            
            # Extract tables
            tables = page.extract_tables()
            if tables:
                print(f"✅ Tables found: {len(tables)}")
                for i, table in enumerate(tables):
                    if table and len(table) > 1:  # Valid table with headers
                        print(f"   Table {i+1}: {len(table)} rows x {len(table[0])} columns")
                        all_tables.append({
                            'page': page_num,
                            'table_num': i+1,
                            'data': table,
                            'rows': len(table),
                            'cols': len(table[0]) if table else 0
                        })
            else:
                print("   No tables found")
    
    return all_text, all_tables

def analyze_extracted_data(text, tables):
    """Analyze the extracted data"""
    print(f"\n📊 EXTRACTION SUMMARY:")
    print(f"Total text length: {len(text):,} characters")
    print(f"Total tables found: {len(tables)}")
    
    if tables:
        print(f"\n📋 TABLE DETAILS:")
        for table_info in tables:
            print(f"Page {table_info['page']}, Table {table_info['table_num']}:")
            print(f"  Size: {table_info['rows']} rows × {table_info['cols']} columns")
            
            # Show first few rows
            if table_info['data']:
                print("  Sample data:")
                for i, row in enumerate(table_info['data'][:3]):  # First 3 rows
                    print(f"    Row {i+1}: {row}")
                if len(table_info['data']) > 3:
                    print(f"    ... and {len(table_info['data'])-3} more rows")
    
    # Look for lighting-specific data
    print(f"\n💡 LIGHTING DATA DETECTED:")
    lighting_keywords = ['lux', 'lx', 'illuminance', 'CRI', 'UGR', 'lumen', 'watt', 'energy']
    found_keywords = []
    
    for keyword in lighting_keywords:
        if keyword.lower() in text.lower():
            count = text.lower().count(keyword.lower())
            found_keywords.append(f"{keyword}: {count} occurrences")
    
    if found_keywords:
        for keyword_info in found_keywords:
            print(f"  ✅ {keyword_info}")
    else:
        print("  ⚠️  No obvious lighting keywords found")

def main():
    """Demo the extraction capabilities"""
    print("🔍 PDF Table & Text Extraction Demo")
    print("=" * 60)
    
    # Check for PDFs in base folder
    base_dir = Path("base")
    if not base_dir.exists():
        print("❌ base/ folder not found")
        return
    
    pdf_files = list(base_dir.glob("*.pdf"))
    if not pdf_files:
        print("❌ No PDF files found in base/ folder")
        return
    
    print(f"Found {len(pdf_files)} PDF files in base/ folder")
    
    for pdf_file in pdf_files:
        try:
            text, tables = extract_tables_and_text(pdf_file)
            analyze_extracted_data(text, tables)
            print("\n" + "="*60 + "\n")
        except Exception as e:
            print(f"❌ Error processing {pdf_file.name}: {e}")

if __name__ == "__main__":
    main()

