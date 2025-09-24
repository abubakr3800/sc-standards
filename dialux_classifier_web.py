#!/usr/bin/env python3
"""
Dialux Classifier Web Interface
Streamlit interface for comprehensive Dialux report classification
"""
import sys
from pathlib import Path
import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import tempfile
import shutil

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import the classifier
from dialux_classifier import DialuxReportClassifier, DialuxClassificationResult
from comprehensive_dialux_processor import ComprehensiveDialuxProcessor, ComprehensiveReport, ComprehensiveRoom

def main():
    """Main Streamlit app for Dialux classification"""
    st.set_page_config(
        page_title="Dialux Report Classifier",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🔍 Dialux Report Classifier")
    st.markdown("**Comprehensive Analysis of Dialux Reports Against Lighting Standards**")
    
    # Initialize classifier
    @st.cache_resource
    def get_classifier():
        return DialuxReportClassifier()
    
    classifier = get_classifier()
    
    # Sidebar
    st.sidebar.title("🔧 Classification Options")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload Dialux PDF Report",
        type=['pdf'],
        help="Upload a Dialux PDF report for comprehensive analysis"
    )
    
    if uploaded_file:
        st.subheader("📄 Uploaded File")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**File:** {uploaded_file.name}")
        with col2:
            st.write(f"**Size:** {uploaded_file.size / 1024:.1f} KB")
        with col3:
            if st.button("🚀 Classify Report", type="primary"):
                classify_report(uploaded_file, classifier)
    
    # Display previous results if available
    if 'classification_result' in st.session_state:
        display_results(st.session_state.classification_result)

def classify_report(uploaded_file, classifier):
    """Classify the uploaded Dialux report"""
    with st.spinner("🔍 Analyzing Dialux report..."):
        try:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                shutil.copyfileobj(uploaded_file, tmp_file)
                tmp_path = Path(tmp_file.name)
            
            # Classify the report
            result = classifier.classify_dialux_report(tmp_path)
            
            # Store result in session state
            st.session_state.classification_result = result
            
            # Clean up temp file
            tmp_path.unlink()
            
            st.success("✅ Classification completed successfully!")
            
        except Exception as e:
            st.error(f"❌ Classification failed: {e}")
            st.exception(e)

def display_results(result: DialuxClassificationResult):
    """Display comprehensive classification results"""
    
    # Header with key metrics
    st.header("📊 Classification Results")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Compliance", f"{result.overall_compliance_rate:.1%}")
    with col2:
        st.metric("Total Rooms", result.total_rooms)
    with col3:
        st.metric("Total Area", f"{result.total_area:.1f} m²")
    with col4:
        st.metric("Application Type", result.application_type)
    
    # Tabs for different views
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Overview", "🏆 Standards Match", "🏠 Room Analysis", 
        "🚨 Issues & Recommendations", "📄 Detailed Report"
    ])
    
    with tab1:
        display_overview(result)
    
    with tab2:
        display_standards_match(result)
    
    with tab3:
        display_room_analysis(result)
    
    with tab4:
        display_issues_recommendations(result)
    
    with tab5:
        display_detailed_report(result)

def display_overview(result: DialuxClassificationResult):
    """Display overview information"""
    st.subheader("📋 Project Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Project Information:**")
        st.write(f"- **Report Name:** {result.report_name}")
        st.write(f"- **Project Name:** {result.project_name}")
        st.write(f"- **Application Type:** {result.application_type}")
        st.write(f"- **Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    with col2:
        st.write("**Compliance Summary:**")
        st.write(f"- **Overall Compliance:** {result.overall_compliance_rate:.1%}")
        st.write(f"- **Best Standard Match:** {result.overall_standard_match}")
        st.write(f"- **Total Rooms Analyzed:** {result.total_rooms}")
        st.write(f"- **Total Area:** {result.total_area:.1f} m²")
    
    # Compliance visualization
    st.subheader("📈 Compliance Visualization")
    
    # Room compliance chart
    room_data = []
    for room in result.room_analyses:
        room_data.append({
            'Room': room.room_name,
            'Compliance': room.overall_compliance * 100,
            'Status': room.compliance_status,
            'Area': room.area
        })
    
    if room_data:
        df_rooms = pd.DataFrame(room_data)
        
        # Color mapping for compliance status
        color_map = {'Compliant': 'green', 'Warning': 'orange', 'Non-Compliant': 'red'}
        df_rooms['Color'] = df_rooms['Status'].map(color_map)
        
        fig = px.bar(
            df_rooms, 
            x='Room', 
            y='Compliance',
            color='Status',
            title='Room-by-Room Compliance Rate',
            color_discrete_map=color_map
        )
        fig.update_layout(yaxis_title='Compliance Rate (%)')
        st.plotly_chart(fig, use_container_width=True)

def display_standards_match(result: DialuxClassificationResult):
    """Display standards matching results"""
    st.subheader("🏆 Standards Matching")
    
    if result.standards_matches:
        st.write("**Top Matching Standards:**")
        
        for i, match in enumerate(result.standards_matches[:3], 1):
            with st.expander(f"{i}. {match.standard_name} (Similarity: {match.similarity_score:.3f})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Standard Type:** {match.standard_type}")
                    st.write(f"**Similarity Score:** {match.similarity_score:.3f}")
                    st.write(f"**Compliance Rate:** {match.compliance_rate:.1%}")
                
                with col2:
                    if match.matched_parameters:
                        st.write("**Matched Parameters:**")
                        for param in match.matched_parameters:
                            st.write(f"  ✅ {param}")
                    
                    if match.missing_parameters:
                        st.write("**Missing Parameters:**")
                        for param in match.missing_parameters:
                            st.write(f"  ❌ {param}")
        
        # Standards comparison chart
        standards_data = []
        for match in result.standards_matches:
            standards_data.append({
                'Standard': match.standard_name,
                'Similarity': match.similarity_score * 100,
                'Type': match.standard_type
            })
        
        df_standards = pd.DataFrame(standards_data)
        fig = px.bar(
            df_standards,
            x='Standard',
            y='Similarity',
            color='Type',
            title='Standards Similarity Comparison'
        )
        fig.update_layout(yaxis_title='Similarity Score (%)')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No matching standards found")

def display_room_analysis(result: DialuxClassificationResult):
    """Display detailed room analysis"""
    st.subheader("🏠 Room-by-Room Analysis")
    
    for room in result.room_analyses:
        with st.expander(f"🏠 {room.room_name} ({room.room_type}) - {room.compliance_status}"):
            
            # Room overview
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Area", f"{room.area:.1f} m²")
            with col2:
                st.metric("Compliance", f"{room.overall_compliance:.1%}")
            with col3:
                status_color = "🟢" if room.compliance_status == "Compliant" else "🟡" if room.compliance_status == "Warning" else "🔴"
                st.metric("Status", f"{status_color} {room.compliance_status}")
            
            # Parameters table
            if room.parameters:
                st.write("**Lighting Parameters:**")
                
                param_data = []
                for param in room.parameters:
                    status_icon = "✅" if param.compliance_status == "Compliant" else "⚠️" if param.compliance_status == "Warning" else "❌"
                    param_data.append({
                        'Parameter': param.name.replace('_', ' ').title(),
                        'Value': f"{param.value} {param.unit}",
                        'Standard': f"{param.standard_value} {param.unit}",
                        'Status': f"{status_icon} {param.compliance_status}",
                        'Importance': param.importance
                    })
                
                df_params = pd.DataFrame(param_data)
                st.dataframe(df_params, use_container_width=True)
            
            # Missing parameters
            if room.missing_parameters:
                st.write("**Missing Parameters:**")
                for param in room.missing_parameters:
                    st.write(f"  ❌ {param.replace('_', ' ').title()}")
            
            # Recommendations
            if room.recommendations:
                st.write("**Recommendations:**")
                for rec in room.recommendations:
                    st.write(f"  💡 {rec}")

def display_issues_recommendations(result: DialuxClassificationResult):
    """Display critical issues and recommendations"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚨 Critical Issues")
        if result.critical_issues:
            for i, issue in enumerate(result.critical_issues, 1):
                st.error(f"{i}. {issue}")
        else:
            st.success("✅ No critical issues found!")
    
    with col2:
        st.subheader("💡 Recommendations")
        if result.recommendations:
            for i, rec in enumerate(result.recommendations, 1):
                st.info(f"{i}. {rec}")
        else:
            st.success("✅ All recommendations implemented!")

def display_detailed_report(result: DialuxClassificationResult):
    """Display the detailed text report"""
    st.subheader("📄 Detailed Analysis Report")
    
    # Download button
    st.download_button(
        label="📥 Download Detailed Report",
        data=result.detailed_report,
        file_name=f"dialux_analysis_{result.report_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain"
    )
    
    # Display report
    st.text_area("Report Content", result.detailed_report, height=600)
    
    # JSON export
    st.subheader("📊 Export Data")
    
    # Convert result to JSON
    result_dict = {
        'report_name': result.report_name,
        'project_name': result.project_name,
        'total_rooms': result.total_rooms,
        'total_area': result.total_area,
        'overall_compliance_rate': result.overall_compliance_rate,
        'overall_standard_match': result.overall_standard_match,
        'application_type': result.application_type,
        'critical_issues': result.critical_issues,
        'recommendations': result.recommendations,
        'room_analyses': [
            {
                'room_name': room.room_name,
                'room_type': room.room_type,
                'area': room.area,
                'overall_compliance': room.overall_compliance,
                'compliance_status': room.compliance_status,
                'parameters': [
                    {
                        'name': param.name,
                        'value': param.value,
                        'unit': param.unit,
                        'standard_value': param.standard_value,
                        'compliance_status': param.compliance_status,
                        'importance': param.importance
                    } for param in room.parameters
                ],
                'missing_parameters': room.missing_parameters,
                'recommendations': room.recommendations
            } for room in result.room_analyses
        ],
        'standards_matches': [
            {
                'standard_name': match.standard_name,
                'standard_type': match.standard_type,
                'similarity_score': match.similarity_score,
                'compliance_rate': match.compliance_rate,
                'matched_parameters': match.matched_parameters,
                'missing_parameters': match.missing_parameters,
                'non_compliant_parameters': match.non_compliant_parameters
            } for match in result.standards_matches
        ]
    }
    
    json_data = json.dumps(result_dict, indent=2, default=str)
    
    st.download_button(
        label="📥 Download JSON Data",
        data=json_data,
        file_name=f"dialux_analysis_{result.report_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )

if __name__ == "__main__":
    main()
