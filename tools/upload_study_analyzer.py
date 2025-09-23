"""
Upload Study Analyzer
Simple interface to upload and analyze PDF lighting studies
"""
import streamlit as st
import json
from pathlib import Path
from pdf_study_analyzer import PDFStudyAnalyzer
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configure Streamlit page
st.set_page_config(
    page_title="PDF Study Analyzer",
    page_icon="📊",
    layout="wide"
)

def main():
    """Main Streamlit app for PDF study analysis"""
    st.title("📊 PDF Lighting Study Analyzer")
    st.markdown("Upload your lighting study PDF and get comprehensive analysis with compliance checking!")
    
    # Initialize analyzer
    analyzer = PDFStudyAnalyzer()
    
    # Sidebar for file upload
    with st.sidebar:
        st.header("📁 Upload PDF Study")
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type="pdf",
            help="Upload your lighting study PDF for analysis"
        )
        
        if uploaded_file is not None:
            # Save uploaded file
            uploads_dir = Path("uploads")
            uploads_dir.mkdir(exist_ok=True)
            
            file_path = uploads_dir / uploaded_file.name
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            
            # Analyze button
            if st.button("🔍 Analyze Study", type="primary"):
                with st.spinner("Analyzing PDF study..."):
                    try:
                        result = analyzer.analyze_pdf_study(file_path)
                        st.session_state['analysis_result'] = result
                        st.success("✅ Analysis completed!")
                    except Exception as e:
                        st.error(f"❌ Analysis failed: {e}")
    
    # Main content area
    if 'analysis_result' in st.session_state:
        result = st.session_state['analysis_result']
        
        # Display summary
        st.header("📋 Analysis Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Rooms Analyzed",
                result['summary']['total_rooms_analyzed']
            )
        
        with col2:
            st.metric(
                "Parameters Found",
                sum(result['summary']['parameters_found'].values())
            )
        
        with col3:
            compliance = result['summary']['overall_compliance']
            compliance_color = "🟢" if compliance == "compliant" else "🔴" if compliance == "non_compliant" else "🟡"
            st.metric(
                "Overall Compliance",
                f"{compliance_color} {compliance.title()}"
            )
        
        with col4:
            st.metric(
                "Analysis Date",
                result['analysis_date'][:10]
            )
        
        # Display key findings
        st.header("🔍 Key Findings")
        for finding in result['summary']['key_findings']:
            st.write(f"• {finding}")
        
        # Display recommendations
        st.header("💡 Recommendations")
        for rec in result['summary']['recommendations']:
            st.write(f"• {rec}")
        
        # Room analysis
        if result['room_data']:
            st.header("🏢 Room Analysis")
            
            # Create room data table
            room_data = []
            for room in result['room_data']:
                room_info = {
                    'Room': room['name'],
                    'Illuminance (lux)': room.get('illuminance', {}).get('value', 'N/A'),
                    'UGR': room.get('ugr', {}).get('value', 'N/A'),
                    'CRI': room.get('cri', {}).get('value', 'N/A'),
                    'Uniformity': room.get('uniformity', {}).get('value', 'N/A')
                }
                room_data.append(room_info)
            
            if room_data:
                df = pd.DataFrame(room_data)
                st.dataframe(df, use_container_width=True)
                
                # Create visualizations
                col1, col2 = st.columns(2)
                
                with col1:
                    # Illuminance chart
                    illuminance_data = [r.get('illuminance', {}).get('value') for r in result['room_data'] if r.get('illuminance')]
                    if illuminance_data:
                        fig = px.bar(
                            x=[r['name'] for r in result['room_data'] if r.get('illuminance')],
                            y=illuminance_data,
                            title="Room Illuminance Levels",
                            labels={'x': 'Room', 'y': 'Illuminance (lux)'}
                        )
                        fig.add_hline(y=500, line_dash="dash", line_color="green", annotation_text="Recommended (500 lux)")
                        fig.add_hline(y=300, line_dash="dash", line_color="orange", annotation_text="Minimum (300 lux)")
                        st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # UGR chart
                    ugr_data = [r.get('ugr', {}).get('value') for r in result['room_data'] if r.get('ugr')]
                    if ugr_data:
                        fig = px.bar(
                            x=[r['name'] for r in result['room_data'] if r.get('ugr')],
                            y=ugr_data,
                            title="Room UGR Levels",
                            labels={'x': 'Room', 'y': 'UGR'}
                        )
                        fig.add_hline(y=19, line_dash="dash", line_color="red", annotation_text="Maximum (19)")
                        st.plotly_chart(fig, use_container_width=True)
        
        # Compliance analysis
        if result['compliance_analysis']['room_compliance']:
            st.header("✅ Compliance Analysis")
            
            compliance_data = []
            for room_comp in result['compliance_analysis']['room_compliance']:
                compliance_info = {
                    'Room': room_comp['room_name'],
                    'Status': room_comp['status'].title(),
                    'Issues': len(room_comp['issues']),
                    'Recommendations': len(room_comp['recommendations'])
                }
                compliance_data.append(compliance_info)
            
            if compliance_data:
                df = pd.DataFrame(compliance_data)
                st.dataframe(df, use_container_width=True)
                
                # Show detailed compliance for each room
                for room_comp in result['compliance_analysis']['room_compliance']:
                    with st.expander(f"📋 {room_comp['room_name']} - {room_comp['status'].title()}"):
                        if room_comp['issues']:
                            st.write("**Issues:**")
                            for issue in room_comp['issues']:
                                st.write(f"❌ {issue}")
                        
                        if room_comp['recommendations']:
                            st.write("**Recommendations:**")
                            for rec in room_comp['recommendations']:
                                st.write(f"✅ {rec}")
        
        # Extracted data
        st.header("📊 Extracted Data")
        
        for param_type, values in result['extracted_data'].items():
            if values:
                with st.expander(f"🔍 {param_type.title()} ({len(values)} values found)"):
                    for i, value in enumerate(values):
                        st.write(f"**Value {i+1}:** {value['value']}")
                        st.write(f"**Confidence:** {value['confidence']:.2f}")
                        st.write(f"**Context:** {value['context'][:200]}...")
                        st.write("---")
        
        # Download results
        st.header("💾 Download Results")
        
        # Create JSON download
        json_str = json.dumps(result, indent=2, ensure_ascii=False)
        st.download_button(
            label="📥 Download Analysis Results (JSON)",
            data=json_str,
            file_name=f"{result['file_name']}_analysis.json",
            mime="application/json"
        )
        
        # Create summary report
        summary_report = f"""
# Lighting Study Analysis Report

## File: {result['file_name']}
## Analysis Date: {result['analysis_date']}

## Summary
- **Rooms Analyzed:** {result['summary']['total_rooms_analyzed']}
- **Overall Compliance:** {result['summary']['overall_compliance']}
- **Parameters Found:** {sum(result['summary']['parameters_found'].values())}

## Key Findings
{chr(10).join([f"- {finding}" for finding in result['summary']['key_findings']])}

## Recommendations
{chr(10).join([f"- {rec}" for rec in result['summary']['recommendations']])}

## Room Analysis
"""
        
        for room in result['room_data']:
            summary_report += f"\n### {room['name']}\n"
            if room.get('illuminance'):
                summary_report += f"- Illuminance: {room['illuminance']['value']} lux\n"
            if room.get('ugr'):
                summary_report += f"- UGR: {room['ugr']['value']}\n"
            if room.get('cri'):
                summary_report += f"- CRI: {room['cri']['value']}\n"
        
        st.download_button(
            label="📄 Download Summary Report (Markdown)",
            data=summary_report,
            file_name=f"{result['file_name']}_summary.md",
            mime="text/markdown"
        )
    
    else:
        # Welcome message
        st.header("🎯 Welcome to PDF Study Analyzer")
        st.markdown("""
        This tool helps you analyze lighting studies from PDF files with high accuracy.
        
        **Features:**
        - 🔍 **Comprehensive Data Extraction** - Extracts illuminance, UGR, CRI, uniformity, and power density
        - 🏢 **Room-Specific Analysis** - Analyzes each room individually
        - ✅ **Compliance Checking** - Compares against EN 12464-1:2021 standards
        - 📊 **Visual Analytics** - Charts and graphs for easy understanding
        - 💾 **Export Results** - Download analysis in JSON or Markdown format
        
        **How to use:**
        1. Upload your PDF lighting study using the sidebar
        2. Click "Analyze Study" to start the analysis
        3. Review the results, compliance status, and recommendations
        4. Download the analysis results for your records
        
        **Supported Parameters:**
        - Illuminance (lux)
        - UGR (Unified Glare Rating)
        - CRI (Color Rendering Index)
        - Uniformity
        - Power Density (W/m²)
        """)
        
        # Show example analysis
        st.header("📋 Example Analysis")
        
        # Check if there are any existing analyses
        studies_dir = Path("studies")
        if studies_dir.exists():
            analysis_files = list(studies_dir.glob("*_analysis.json"))
            if analysis_files:
                st.write("**Recent Analyses:**")
                for analysis_file in analysis_files[-3:]:  # Show last 3
                    st.write(f"• {analysis_file.stem}")

if __name__ == "__main__":
    main()
