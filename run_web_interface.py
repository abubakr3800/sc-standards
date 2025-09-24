#!/usr/bin/env python3
"""
Web Interface Entry Point for AI Standards Training System
Fixes import issues when running Streamlit directly
"""
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Now import the web interface components
from ai_standards.core.config import config
from ai_standards.core.pdf_processor import PDFProcessor
from ai_standards.models.ai_trainer import AIStandardsTrainer
from ai_standards.models.comparison_model import StandardsComparisonModel, ComparisonResult
from ai_standards.core.simple_pdf_processor import SimplePDFProcessor

import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from typing import List, Dict, Any, Optional
import tempfile
import shutil
from datetime import datetime
import io
import base64

# Initialize components
@st.cache_resource
def initialize_components():
    """Initialize AI components with caching"""
    try:
        pdf_processor = SimplePDFProcessor()
        ai_trainer = AIStandardsTrainer()
        comparison_model = StandardsComparisonModel()
        return pdf_processor, ai_trainer, comparison_model
    except Exception as e:
        st.error(f"Failed to initialize components: {e}")
        return None, None, None

def main():
    """Main Streamlit app"""
    st.set_page_config(
        page_title="AI Standards Training System",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🧠 AI Standards Training System")
    st.markdown("**Process, Train, and Compare Lighting Standards with AI**")
    
    # Initialize components
    pdf_processor, ai_trainer, comparison_model = initialize_components()
    
    if not pdf_processor:
        st.error("Failed to initialize system components. Please check the logs.")
        return
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["🏠 Home", "📄 Upload & Process", "🧠 Train Models", "🔍 Compare Standards", "📊 Analytics"]
    )
    
    if page == "🏠 Home":
        home_page()
    elif page == "📄 Upload & Process":
        upload_process_page(pdf_processor)
    elif page == "🧠 Train Models":
        train_models_page(ai_trainer)
    elif page == "🔍 Compare Standards":
        compare_standards_page(comparison_model)
    elif page == "📊 Analytics":
        analytics_page()

def home_page():
    """Home page with system overview"""
    st.header("🏠 Welcome to AI Standards Training System")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 What This System Does")
        st.markdown("""
        - **Process PDF Standards**: Extract text and structured data from lighting standards
        - **Train AI Models**: Create custom models that understand lighting requirements
        - **Compare Standards**: Analyze similarities and differences between standards
        - **Generate Insights**: Provide AI-powered recommendations for compliance
        """)
        
        st.subheader("📊 System Status")
        
        # Check processed documents
        processed_files = list(config.UPLOADS_DIR.glob("*_processed.json"))
        st.metric("Processed Documents", len(processed_files))
        
        # Check standards
        standards_files = list(config.BASE_PDFS_DIR.glob("*.pdf"))
        st.metric("Available Standards", len(standards_files))
        
        # Check models
        models_dir = config.MODELS_DIR
        model_files = list(models_dir.glob("**/*")) if models_dir.exists() else []
        st.metric("Trained Models", len([f for f in model_files if f.is_file()]))
    
    with col2:
        st.subheader("🚀 Quick Start")
        st.markdown("""
        1. **Upload PDFs**: Go to Upload & Process page
        2. **Train Models**: Use Train Models page to create AI models
        3. **Compare**: Use Compare Standards to analyze differences
        4. **View Results**: Check Analytics for detailed insights
        """)
        
        st.subheader("📚 Available Standards")
        if standards_files:
            for i, file in enumerate(standards_files[:5], 1):
                st.write(f"{i}. {file.name}")
            if len(standards_files) > 5:
                st.write(f"... and {len(standards_files) - 5} more")
        else:
            st.write("No standards found in base directory")

def upload_process_page(pdf_processor):
    """Upload and process PDFs page"""
    st.header("📄 Upload & Process PDFs")
    
    # File upload
    uploaded_files = st.file_uploader(
        "Choose PDF files to process",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload one or more PDF files to process"
    )
    
    if uploaded_files:
        st.subheader("📋 Uploaded Files")
        
        # Display uploaded files
        for i, file in enumerate(uploaded_files):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{file.name}**")
            with col2:
                st.write(f"{file.size / 1024:.1f} KB")
            with col3:
                if st.button(f"Process", key=f"process_{i}"):
                    process_single_file(file, pdf_processor)
        
        # Process all files
        if st.button("🚀 Process All Files", type="primary"):
            process_all_files(uploaded_files, pdf_processor)
    
    # Show processed documents
    st.subheader("📊 Processed Documents")
    processed_files = list(config.UPLOADS_DIR.glob("*_processed.json"))
    
    if processed_files:
        for file_path in processed_files:
            with st.expander(f"📄 {file_path.stem}"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Language:** {data.get('language', 'Unknown')}")
                        st.write(f"**Text Length:** {len(data.get('text', ''))}")
                    with col2:
                        st.write(f"**Tables:** {len(data.get('tables', []))}")
                        st.write(f"**Chunks:** {len(data.get('chunks', []))}")
                    
                    # Show preview
                    text_preview = data.get('text', '')[:500]
                    if text_preview:
                        st.text_area("Text Preview", text_preview, height=100)
                        
                except Exception as e:
                    st.error(f"Error reading file: {e}")
    else:
        st.info("No processed documents found. Upload and process some PDFs first.")

def process_single_file(uploaded_file, pdf_processor):
    """Process a single uploaded file"""
    with st.spinner(f"Processing {uploaded_file.name}..."):
        try:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                shutil.copyfileobj(uploaded_file, tmp_file)
                tmp_path = Path(tmp_file.name)
            
            # Process the file
            result = pdf_processor.process_pdf(tmp_path, "en")
            
            if result:
                # Save result
                output_path = config.UPLOADS_DIR / f"{uploaded_file.name}_processed.json"
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, default=str)
                
                st.success(f"✅ Successfully processed {uploaded_file.name}")
                st.json({
                    "language": result.get('language', 'Unknown'),
                    "text_length": len(result.get('text', '')),
                    "tables_found": len(result.get('tables', [])),
                    "chunks_created": len(result.get('chunks', []))
                })
            else:
                st.error(f"❌ Failed to process {uploaded_file.name}")
            
            # Clean up temp file
            tmp_path.unlink()
            
        except Exception as e:
            st.error(f"❌ Error processing {uploaded_file.name}: {e}")

def process_all_files(uploaded_files, pdf_processor):
    """Process all uploaded files"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    successful = 0
    failed = 0
    
    for i, file in enumerate(uploaded_files):
        status_text.text(f"Processing {file.name}...")
        progress_bar.progress((i + 1) / len(uploaded_files))
        
        try:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                shutil.copyfileobj(file, tmp_file)
                tmp_path = Path(tmp_file.name)
            
            # Process the file
            result = pdf_processor.process_pdf(tmp_path, "en")
            
            if result:
                # Save result
                output_path = config.UPLOADS_DIR / f"{file.name}_processed.json"
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, default=str)
                successful += 1
            else:
                failed += 1
            
            # Clean up temp file
            tmp_path.unlink()
            
        except Exception as e:
            st.error(f"Error processing {file.name}: {e}")
            failed += 1
    
    progress_bar.progress(1.0)
    status_text.text("Processing completed!")
    
    st.success(f"✅ Successfully processed {successful} files")
    if failed > 0:
        st.warning(f"⚠️ Failed to process {failed} files")

def train_models_page(ai_trainer):
    """Train AI models page"""
    st.header("🧠 Train AI Models")
    
    # Check for processed documents
    processed_files = list(config.UPLOADS_DIR.glob("*_processed.json"))
    
    if not processed_files:
        st.warning("No processed documents found. Please upload and process PDFs first.")
        return
    
    st.info(f"Found {len(processed_files)} processed documents")
    
    # Training options
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Training Configuration")
        num_epochs = st.slider("Number of Epochs", 1, 10, 3)
        batch_size = st.selectbox("Batch Size", [8, 16, 32], index=1)
        learning_rate = st.selectbox("Learning Rate", [1e-5, 2e-5, 5e-5], index=1)
    
    with col2:
        st.subheader("Model Options")
        train_classification = st.checkbox("Train Classification Model", value=True)
        train_embeddings = st.checkbox("Fine-tune Embedding Model", value=True)
        store_embeddings = st.checkbox("Store Embeddings in Vector DB", value=True)
    
    # Start training
    if st.button("🚀 Start Training", type="primary"):
        start_training(processed_files, {
            "num_epochs": num_epochs,
            "batch_size": batch_size,
            "learning_rate": learning_rate,
            "train_classification": train_classification,
            "train_embeddings": train_embeddings,
            "store_embeddings": store_embeddings
        }, ai_trainer)

def start_training(processed_files, training_config, ai_trainer):
    """Start model training"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("Loading processed documents...")
        progress_bar.progress(0.1)
        
        # Load processed documents
        processed_documents = []
        for file_path in processed_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                doc_data = json.load(f)
                processed_documents.append(doc_data)
        
        status_text.text("Creating training data...")
        progress_bar.progress(0.3)
        
        # Create training data
        training_data = ai_trainer.create_training_data(processed_documents)
        
        status_text.text("Training classification model...")
        progress_bar.progress(0.5)
        
        # Train classification model
        if training_config["train_classification"]:
            classification_results = ai_trainer.train_classification_model(training_data)
            st.success("✅ Classification model trained successfully")
        
        status_text.text("Fine-tuning embedding model...")
        progress_bar.progress(0.7)
        
        # Train embedding model
        if training_config["train_embeddings"]:
            embedding_results = ai_trainer.train_embedding_model(training_data)
            st.success("✅ Embedding model fine-tuned successfully")
        
        status_text.text("Storing embeddings...")
        progress_bar.progress(0.9)
        
        # Store embeddings
        if training_config["store_embeddings"]:
            storage_results = ai_trainer.store_embeddings(training_data)
            st.success("✅ Embeddings stored in vector database")
        
        progress_bar.progress(1.0)
        status_text.text("Training completed successfully!")
        
        # Display results
        st.subheader("📊 Training Results")
        
        if training_config["train_classification"]:
            st.write("**Classification Model:**")
            st.write(f"- Accuracy: {classification_results['accuracy']:.4f}")
            st.write(f"- Training Samples: {classification_results['training_samples']}")
            st.write(f"- Test Samples: {classification_results['test_samples']}")
        
        st.write("**Training Data:**")
        st.write(f"- Total Samples: {len(training_data['texts'])}")
        st.write(f"- Categories: {len(set(training_data['labels']))}")
        
    except Exception as e:
        st.error(f"❌ Training failed: {e}")

def compare_standards_page(comparison_model):
    """Compare standards page"""
    st.header("🔍 Compare Standards")
    
    # File selection
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Standard A")
        standard_a_files = list(config.UPLOADS_DIR.glob("*.pdf")) + list(config.BASE_PDFS_DIR.glob("*.pdf"))
        if standard_a_files:
            standard_a = st.selectbox("Select Standard A", [f.name for f in standard_a_files])
            standard_a_path = next(f for f in standard_a_files if f.name == standard_a)
        else:
            st.warning("No PDF files found")
            return
    
    with col2:
        st.subheader("Standard B")
        standard_b_files = list(config.UPLOADS_DIR.glob("*.pdf")) + list(config.BASE_PDFS_DIR.glob("*.pdf"))
        if standard_b_files:
            standard_b = st.selectbox("Select Standard B", [f.name for f in standard_b_files])
            standard_b_path = next(f for f in standard_b_files if f.name == standard_b)
        else:
            st.warning("No PDF files found")
            return
    
    # Compare button
    if st.button("🔍 Compare Standards", type="primary"):
        if standard_a_path and standard_b_path:
            compare_standards(standard_a_path, standard_b_path, comparison_model)

def compare_standards(standard_a_path, standard_b_path, comparison_model):
    """Compare two standards"""
    with st.spinner("Comparing standards..."):
        try:
            result = comparison_model.compare_standards(standard_a_path, standard_b_path)
            
            if result:
                st.success("✅ Comparison completed!")
                
                # Display results
                st.subheader("📊 Comparison Results")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Overall Similarity", f"{result.similarity_score:.3f}")
                with col2:
                    st.metric("Compliance Status", result.compliance_status)
                with col3:
                    st.metric("Standard A", standard_a_path.name)
                
                # Category scores
                st.subheader("📈 Category Scores")
                
                category_data = []
                for category, score in result.category_scores.items():
                    category_data.append({
                        "Category": category.replace("_", " ").title(),
                        "Score": score
                    })
                
                df = pd.DataFrame(category_data)
                fig = px.bar(df, x="Category", y="Score", title="Category Similarity Scores")
                st.plotly_chart(fig, use_container_width=True)
                
                # Key differences
                if result.differences:
                    st.subheader("🔍 Key Differences")
                    for diff in result.differences:
                        st.write(f"- {diff}")
                
                # Recommendations
                if result.recommendations:
                    st.subheader("💡 Recommendations")
                    for rec in result.recommendations:
                        st.write(f"- {rec}")
                        
            else:
                st.error("❌ Comparison failed")
                
        except Exception as e:
            st.error(f"❌ Error during comparison: {e}")

def analytics_page():
    """Analytics page"""
    st.header("📊 Analytics")
    
    # System statistics
    st.subheader("📈 System Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        processed_files = list(config.UPLOADS_DIR.glob("*_processed.json"))
        st.metric("Processed Documents", len(processed_files))
    
    with col2:
        standards_files = list(config.BASE_PDFS_DIR.glob("*.pdf"))
        st.metric("Available Standards", len(standards_files))
    
    with col3:
        models_dir = config.MODELS_DIR
        model_files = list(models_dir.glob("**/*")) if models_dir.exists() else []
        st.metric("Trained Models", len([f for f in model_files if f.is_file()]))
    
    with col4:
        total_size = sum(f.stat().st_size for f in processed_files) / (1024 * 1024)
        st.metric("Data Size (MB)", f"{total_size:.1f}")
    
    # Recent activity
    st.subheader("🕒 Recent Activity")
    
    if processed_files:
        # Sort by modification time
        recent_files = sorted(processed_files, key=lambda x: x.stat().st_mtime, reverse=True)[:5]
        
        for file_path in recent_files:
            mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
            st.write(f"📄 {file_path.stem} - {mod_time.strftime('%Y-%m-%d %H:%M')}")
    else:
        st.info("No recent activity")

if __name__ == "__main__":
    main()
