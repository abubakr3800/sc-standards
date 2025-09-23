"""
Web Interface for AI Standards Training System
Provides Streamlit and FastAPI interfaces for the system
"""
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
import json
import tempfile
import shutil
from datetime import datetime

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from loguru import logger

from ..core.config import config
from ..core.pdf_processor import PDFProcessor
from ..models.ai_trainer import AIStandardsTrainer
from ..models.comparison_model import StandardsComparisonModel, ComparisonResult

# Initialize components
pdf_processor = PDFProcessor()
ai_trainer = AIStandardsTrainer()
comparison_model = StandardsComparisonModel()

# Streamlit Interface
def create_streamlit_app():
    """Create Streamlit web interface"""
    
    st.set_page_config(
        page_title="AI Standards Training System",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🤖 AI Standards Training & Comparison System")
    st.markdown("Upload lighting standards PDFs, train AI models, and compare standards across different regions and languages.")
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["📄 Upload & Process", "🧠 Train Models", "🔍 Compare Standards", "📊 Analytics", "⚙️ Settings"]
    )
    
    if page == "📄 Upload & Process":
        upload_and_process_page()
    elif page == "🧠 Train Models":
        train_models_page()
    elif page == "🔍 Compare Standards":
        compare_standards_page()
    elif page == "📊 Analytics":
        analytics_page()
    elif page == "⚙️ Settings":
        settings_page()

def upload_and_process_page():
    """Upload and process PDFs page"""
    st.header("📄 Upload & Process Standards")
    
    # File upload
    uploaded_files = st.file_uploader(
        "Upload PDF standards files",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload multiple PDF files in any language"
    )
    
    if uploaded_files:
        st.success(f"Uploaded {len(uploaded_files)} files")
        
        # Processing options
        col1, col2 = st.columns(2)
        
        with col1:
            target_language = st.selectbox(
                "Target Language for Translation",
                ["en", "de", "fr", "es", "it", "pt", "nl", "sv", "no", "da", "fi"],
                index=0
            )
        
        with col2:
            extraction_method = st.selectbox(
                "PDF Extraction Method",
                ["pdfplumber", "pymupdf", "pdfminer"],
                index=0
            )
        
        # Process files
        if st.button("🚀 Process Files", type="primary"):
            process_uploaded_files(uploaded_files, target_language, extraction_method)

def process_uploaded_files(uploaded_files, target_language, extraction_method):
    """Process uploaded PDF files"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    processed_documents = []
    
    for i, uploaded_file in enumerate(uploaded_files):
        status_text.text(f"Processing {uploaded_file.name}...")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = Path(tmp_file.name)
        
        try:
            # Process PDF
            processed_doc = pdf_processor.process_pdf(tmp_path, target_language)
            processed_doc['original_filename'] = uploaded_file.name
            processed_documents.append(processed_doc)
            
            st.success(f"✅ Processed {uploaded_file.name}")
            
        except Exception as e:
            st.error(f"❌ Failed to process {uploaded_file.name}: {e}")
        
        finally:
            # Clean up temporary file
            tmp_path.unlink()
        
        progress_bar.progress((i + 1) / len(uploaded_files))
    
    status_text.text("Processing complete!")
    
    # Display results
    if processed_documents:
        display_processing_results(processed_documents)

def display_processing_results(processed_documents):
    """Display processing results"""
    st.subheader("📋 Processing Results")
    
    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Documents Processed", len(processed_documents))
    
    with col2:
        total_chunks = sum(len(doc['chunks']) for doc in processed_documents)
        st.metric("Total Text Chunks", total_chunks)
    
    with col3:
        languages = set(doc['detected_language'] for doc in processed_documents)
        st.metric("Languages Detected", len(languages))
    
    with col4:
        total_text_length = sum(len(doc['processed_text']) for doc in processed_documents)
        st.metric("Total Text Length", f"{total_text_length:,} chars")
    
    # Detailed results
    for i, doc in enumerate(processed_documents):
        with st.expander(f"📄 {doc['original_filename']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Metadata:**")
                st.write(f"- Language: {doc['detected_language']}")
                st.write(f"- Extraction Method: {doc['extraction_method']}")
                st.write(f"- Text Length: {len(doc['processed_text']):,} characters")
                st.write(f"- Number of Chunks: {len(doc['chunks'])}")
            
            with col2:
                st.write("**Structured Data:**")
                structured_data = doc['structured_data']
                for key, values in structured_data.items():
                    if values:
                        st.write(f"- {key.replace('_', ' ').title()}: {len(values)} items")
            
            # Show text preview
            st.write("**Text Preview:**")
            preview_text = doc['processed_text'][:500] + "..." if len(doc['processed_text']) > 500 else doc['processed_text']
            st.text_area("", preview_text, height=100, key=f"preview_{i}")

def train_models_page():
    """Train AI models page"""
    st.header("🧠 Train AI Models")
    
    # Check for processed documents
    processed_files = list(config.UPLOADS_DIR.glob("*.json"))
    
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
        })

def start_training(processed_files, training_config):
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
        logger.error(f"Training failed: {e}")

def compare_standards_page():
    """Compare standards page"""
    st.header("🔍 Compare Standards")
    
    # File selection
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Select Standard A")
        standard_a_files = list(config.UPLOADS_DIR.glob("*.pdf"))
        if standard_a_files:
            standard_a = st.selectbox("Choose Standard A", [f.name for f in standard_a_files])
        else:
            st.warning("No PDF files found. Please upload files first.")
            return
    
    with col2:
        st.subheader("Select Standard B")
        standard_b_files = [f for f in standard_a_files if f.name != standard_a]
        if standard_b_files:
            standard_b = st.selectbox("Choose Standard B", [f.name for f in standard_b_files])
        else:
            st.warning("No other PDF files found for comparison.")
            return
    
    # Comparison options
    st.subheader("Comparison Options")
    col1, col2 = st.columns(2)
    
    with col1:
        similarity_threshold = st.slider("Similarity Threshold", 0.0, 1.0, 0.7, 0.05)
    
    with col2:
        include_recommendations = st.checkbox("Generate Recommendations", value=True)
    
    # Perform comparison
    if st.button("🔍 Compare Standards", type="primary"):
        perform_comparison(standard_a, standard_b, similarity_threshold, include_recommendations)

def perform_comparison(standard_a_name, standard_b_name, threshold, include_recommendations):
    """Perform standards comparison"""
    try:
        standard_a_path = config.UPLOADS_DIR / standard_a_name
        standard_b_path = config.UPLOADS_DIR / standard_b_name
        
        # Perform comparison
        comparison_result = comparison_model.compare_standards(standard_a_path, standard_b_path)
        
        # Display results
        st.subheader("📊 Comparison Results")
        
        # Overall similarity
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Overall Similarity", f"{comparison_result.similarity_score:.3f}")
        
        with col2:
            st.metric("Compliance Status", comparison_result.compliance_status)
        
        with col3:
            status_color = "🟢" if comparison_result.compliance_status == "Compliant" else "🟡" if "Partially" in comparison_result.compliance_status else "🔴"
            st.metric("Status", status_color)
        
        # Category scores
        st.subheader("📈 Category Similarity Scores")
        
        category_df = pd.DataFrame([
            {"Category": cat.replace("_", " ").title(), "Score": score}
            for cat, score in comparison_result.category_scores.items()
        ])
        
        fig = px.bar(category_df, x="Category", y="Score", 
                    title="Similarity Scores by Category",
                    color="Score", color_continuous_scale="RdYlGn")
        fig.update_layout(yaxis_range=[0, 1])
        st.plotly_chart(fig, use_container_width=True)
        
        # Differences
        if comparison_result.differences:
            st.subheader("⚠️ Key Differences")
            for diff in comparison_result.differences:
                st.write(f"- {diff}")
        
        # Recommendations
        if include_recommendations and comparison_result.recommendations:
            st.subheader("💡 Recommendations")
            for rec in comparison_result.recommendations:
                st.write(f"- {rec}")
        
        # Detailed comparison
        with st.expander("📋 Detailed Comparison"):
            st.json({
                "standard_a": comparison_result.standard_a,
                "standard_b": comparison_result.standard_b,
                "similarity_score": comparison_result.similarity_score,
                "category_scores": comparison_result.category_scores,
                "compliance_status": comparison_result.compliance_status
            })
        
    except Exception as e:
        st.error(f"❌ Comparison failed: {e}")
        logger.error(f"Comparison failed: {e}")

def analytics_page():
    """Analytics page"""
    st.header("📊 Analytics Dashboard")
    
    # Check for training results
    results_files = list(config.OUTPUTS_DIR.glob("training_results_*.json"))
    
    if not results_files:
        st.warning("No training results found. Please train models first.")
        return
    
    # Load latest results
    latest_results_file = max(results_files, key=lambda x: x.stat().st_mtime)
    
    with open(latest_results_file, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    st.subheader("📈 Training Performance")
    
    # Model performance metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if "classification_training" in results and "accuracy" in results["classification_training"]:
            accuracy = results["classification_training"]["accuracy"]
            st.metric("Classification Accuracy", f"{accuracy:.4f}")
    
    with col2:
        if "training_data_creation" in results:
            samples = results["training_data_creation"]["samples"]
            st.metric("Training Samples", samples)
    
    with col3:
        if "embedding_storage" in results and "stored_count" in results["embedding_storage"]:
            stored = results["embedding_storage"]["stored_count"]
            st.metric("Stored Embeddings", stored)
    
    # Processing statistics
    st.subheader("📄 Document Processing Statistics")
    
    if "pdf_processing" in results:
        processing_stats = results["pdf_processing"]
        successful = sum(1 for status in processing_stats.values() if status == "success")
        total = len(processing_stats)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Successfully Processed", f"{successful}/{total}")
        
        with col2:
            success_rate = (successful / total) * 100 if total > 0 else 0
            st.metric("Success Rate", f"{success_rate:.1f}%")
    
    # Model architecture info
    st.subheader("🏗️ Model Architecture")
    
    model_info = {
        "Embedding Model": config.AI_MODELS["embedding_model"],
        "Classification Model": config.AI_MODELS["classification_model"],
        "Max Sequence Length": config.AI_MODELS["max_sequence_length"],
        "Batch Size": config.AI_MODELS["batch_size"],
        "Learning Rate": config.AI_MODELS["learning_rate"]
    }
    
    for key, value in model_info.items():
        st.write(f"**{key}:** {value}")

def settings_page():
    """Settings page"""
    st.header("⚙️ System Settings")
    
    # Configuration display
    st.subheader("Current Configuration")
    
    with st.expander("PDF Processing Settings"):
        st.json(config.PDF_PROCESSING)
    
    with st.expander("AI Model Settings"):
        st.json(config.AI_MODELS)
    
    with st.expander("Comparison Settings"):
        st.json(config.COMPARISON)
    
    # System information
    st.subheader("System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Directories:**")
        st.write(f"- Data: {config.DATA_DIR}")
        st.write(f"- Models: {config.MODELS_DIR}")
        st.write(f"- Uploads: {config.UPLOADS_DIR}")
        st.write(f"- Outputs: {config.OUTPUTS_DIR}")
    
    with col2:
        st.write("**Database:**")
        st.write(f"- Path: {config.DATABASE['path']}")
        st.write(f"- Vector DB: {config.DATABASE['vector_db_path']}")
    
    # Reset options
    st.subheader("System Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🗑️ Clear Uploads", type="secondary"):
            clear_directory(config.UPLOADS_DIR)
            st.success("Uploads cleared!")
    
    with col2:
        if st.button("🗑️ Clear Outputs", type="secondary"):
            clear_directory(config.OUTPUTS_DIR)
            st.success("Outputs cleared!")
    
    with col3:
        if st.button("🗑️ Clear Models", type="secondary"):
            clear_directory(config.MODELS_DIR)
            st.success("Models cleared!")

def clear_directory(directory: Path):
    """Clear directory contents"""
    if directory.exists():
        for item in directory.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)

# FastAPI Interface
app = FastAPI(title="AI Standards Training API", version="1.0.0")

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload and process a PDF file"""
    try:
        # Save uploaded file
        file_path = config.UPLOADS_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process PDF
        processed_doc = pdf_processor.process_pdf(file_path)
        
        # Save processed data
        output_path = config.UPLOADS_DIR / f"{file_path.stem}_processed.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(processed_doc, f, indent=2, default=str)
        
        return JSONResponse({
            "status": "success",
            "filename": file.filename,
            "processed_data": processed_doc
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/train")
async def train_models():
    """Train AI models"""
    try:
        # Find processed documents
        processed_files = list(config.UPLOADS_DIR.glob("*_processed.json"))
        
        if not processed_files:
            raise HTTPException(status_code=400, detail="No processed documents found")
        
        # Load processed documents
        processed_documents = []
        for file_path in processed_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                doc_data = json.load(f)
                processed_documents.append(doc_data)
        
        # Train models
        results = ai_trainer.train_complete_pipeline([Path(doc['file_path']) for doc in processed_documents])
        
        return JSONResponse(results)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/compare")
async def compare_standards(standard_a: str, standard_b: str):
    """Compare two standards"""
    try:
        standard_a_path = config.UPLOADS_DIR / standard_a
        standard_b_path = config.UPLOADS_DIR / standard_b
        
        if not standard_a_path.exists() or not standard_b_path.exists():
            raise HTTPException(status_code=404, detail="Standard files not found")
        
        comparison_result = comparison_model.compare_standards(standard_a_path, standard_b_path)
        
        return JSONResponse({
            "standard_a": comparison_result.standard_a,
            "standard_b": comparison_result.standard_b,
            "similarity_score": comparison_result.similarity_score,
            "category_scores": comparison_result.category_scores,
            "differences": comparison_result.differences,
            "recommendations": comparison_result.recommendations,
            "compliance_status": comparison_result.compliance_status
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/standards")
async def list_standards():
    """List available standards"""
    try:
        pdf_files = list(config.UPLOADS_DIR.glob("*.pdf"))
        return JSONResponse([f.name for f in pdf_files])
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Root endpoint with API documentation"""
    return HTMLResponse("""
    <html>
        <head>
            <title>AI Standards Training API</title>
        </head>
        <body>
            <h1>AI Standards Training API</h1>
            <p>API for processing, training, and comparing lighting standards</p>
            <h2>Endpoints:</h2>
            <ul>
                <li>POST /upload - Upload and process PDF files</li>
                <li>POST /train - Train AI models</li>
                <li>POST /compare - Compare two standards</li>
                <li>GET /standards - List available standards</li>
            </ul>
            <p>For detailed API documentation, visit <a href="/docs">/docs</a></p>
        </body>
    </html>
    """)

def run_streamlit():
    """Run Streamlit interface"""
    create_streamlit_app()

def run_fastapi():
    """Run FastAPI server"""
    uvicorn.run(app, host=config.API["host"], port=config.API["port"])

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        run_fastapi()
    else:
        run_streamlit()
