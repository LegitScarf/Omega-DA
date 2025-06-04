import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from io import StringIO, BytesIO
import base64
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Additional imports for profiling and D-Tale
from ydata_profiling import ProfileReport
import dtale
import socket

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

# Set page configuration
st.set_page_config(
    page_title="Omega - EDA Tool",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Omega styling
st.markdown("""
<style>
    /* Main app styling */
    .main {
        background-color: #ffffff;
    }
    
    .stApp {
        background-color: #ffffff;
    }
    
    /* Header styling */
    .main-header {
        font-size: 3.5rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        font-size: 1.8rem;
        color: #A23B72;
        margin: 1.5rem 0;
        font-weight: 600;
    }
    
    /* Custom boxes */
    .success-box {
        padding: 1.2rem;
        border-radius: 10px;
        background-color: #f8fff8;
        border: 2px solid #4CAF50;
        color: #2E7D2E;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .info-box {
        padding: 1.2rem;
        border-radius: 10px;
        background-color: #f0f8ff;
        border: 2px solid #2E86AB;
        color: #1a5490;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .warning-box {
        padding: 1.2rem;
        border-radius: 10px;
        background-color: #fff8f0;
        border: 2px solid #ff9800;
        color: #e65100;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        height: 3.5rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 12px;
        background-color: #ffffff;
        border: 2px solid #2E86AB;
        color: #2E86AB;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #f0f8ff;
        border-color: #A23B72;
        color: #A23B72;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(46, 134, 171, 0.3);
    }
    
    .stButton > button:active {
        transform: translateY(0px);
    }
    
    /* Download button styling */
    .stDownloadButton > button {
        background-color: #ffffff;
        border: 2px solid #4CAF50;
        color: #4CAF50;
        border-radius: 12px;
        font-weight: 600;
        height: 3rem;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        background-color: #f8fff8;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #fafafa;
    }
    
    /* Metrics styling */
    .metric-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        text-align: center;
    }
    
    /* File uploader styling */
    .stFileUploader {
        background-color: #ffffff;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border: 1px solid #e9ecef;
        border-radius: 8px;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border-radius: 8px;
        border: 1px solid #e9ecef;
    }
    
    /* Custom stat cards */
    .stat-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #2E86AB;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: bold;
        color: #A23B72;
        margin: 0;
    }
    
    .stat-label {
        font-size: 1rem;
        color: #2E86AB;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

def load_dataset(uploaded_file):
    """Load CSV dataset from uploaded file"""
    try:
        df = pd.read_csv(uploaded_file)
        return df, None
    except Exception as e:
        return None, str(e)

def generate_omega_report_html(df, filename):
    # ... existing code ...
    # (Keep your previous implementation of generate_omega_report_html here)
    # ... existing code ...
    # (No changes needed)
    # ... existing code ...
    return html_content

def display_dataset_info(df):
    # ... existing code ...
    # (Keep your previous implementation of display_dataset_info here)
    # ... existing code ...

def create_visualizations(df):
    # ... existing code ...
    # (Keep your previous implementation of create_visualizations here)
    # ... existing code ...

def main():
    # Main header with Omega branding
    st.markdown('<h1 class="main-header">🔮 OMEGA</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #6c757d; margin-bottom: 3rem;">Advanced Exploratory Data Analysis Tool</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🔮 Omega Features")
        st.markdown("""
        1. **Smart Upload** 📁 - Intelligent CSV processing
        2. **Custom EDA** 📊 - Comprehensive analysis reports  
        3. **Interactive Charts** 📈 - Dynamic visualizations
        4. **Export Ready** 💾 - Download detailed reports
        """)
        
        st.markdown("---")
        st.markdown("### 🚀 Quick Start")
        st.markdown("""
        1. Upload your CSV dataset
        2. Review the data overview
        3. Explore interactive visualizations
        4. Generate comprehensive EDA report
        5. Download your analysis
        """)
        
        st.markdown("---")
        st.markdown("### ℹ️ About Omega")
        st.markdown("""
        Omega is your intelligent companion for exploratory data analysis. 
        Built with advanced analytics to provide deep insights 
        into your datasets without external dependencies.
        """)
    
    # File uploader
    st.markdown('<h2 class="sub-header">📁 Dataset Upload</h2>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">🔮 Upload your CSV file to begin the Omega analysis journey</div>', 
               unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose your CSV file",
        type=['csv'],
        help="Upload a CSV file to perform comprehensive EDA analysis with Omega"
    )
    
    if uploaded_file is not None:
        # Load dataset
        df, error = load_dataset(uploaded_file)
        
        if error:
            st.markdown(f'<div class="warning-box">❌ Error loading dataset: {error}</div>', 
                       unsafe_allow_html=True)
            return
        
        # Display success message
        st.markdown(f'<div class="success-box">✅ Dataset "{uploaded_file.name}" successfully loaded into Omega!</div>', 
                   unsafe_allow_html=True)
        
        # Dataset information
        st.markdown('<h2 class="sub-header">📋 Dataset Overview</h2>', unsafe_allow_html=True)
        display_dataset_info(df)
        
        # Show first few rows
        with st.expander("👀 Dataset Preview (First 10 rows)", expanded=False):
            st.dataframe(df.head(10), use_container_width=True)
        
        # Show data types and info
        with st.expander("🔍 Column Details", expanded=False):
            col_info = pd.DataFrame({
                'Column': df.columns,
                'Data Type': df.dtypes.astype(str),
                'Non-Null Count': df.count(),
                'Missing Values': df.isnull().sum(),
                'Missing %': (df.isnull().sum() / len(df) * 100).round(2),
                'Unique Values': df.nunique()
            })
            st.dataframe(col_info, use_container_width=True)
        
        # Data quality summary
        with st.expander("🎯 Data Quality Summary", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📊 Column Types:**")
                numeric_count = len(df.select_dtypes(include=[np.number]).columns)
                categorical_count = len(df.select_dtypes(include=['object']).columns)
                datetime_count = len(df.select_dtypes(include=['datetime64']).columns)
                
                st.write(f"• Numeric columns: {numeric_count}")
                st.write(f"• Categorical columns: {categorical_count}")
                st.write(f"• Datetime columns: {datetime_count}")
            
            with col2:
                st.markdown("**🔍 Data Quality:**")
                duplicate_rows = df.duplicated().sum()
                complete_rows = len(df) - df.isnull().any(axis=1).sum()
                completeness = (complete_rows / len(df)) * 100
                
                st.write(f"• Complete rows: {complete_rows:,} ({completeness:.1f}%)")
                st.write(f"• Duplicate rows: {duplicate_rows:,}")
                st.write(f"• Total missing cells: {df.isnull().sum().sum():,}")
        
        st.markdown("---")
        
        # Interactive Visualizations
        create_visualizations(df)
        
        st.markdown("---")
        
        # EDA Report Generation
        st.markdown('<h2 class="sub-header">📋 Comprehensive EDA Report</h2>', unsafe_allow_html=True)
        st.markdown('<div class="info-box">🔮 Generate a detailed HTML report with all analysis results</div>', 
                   unsafe_allow_html=True)
        
        if st.button("🚀 Generate Omega EDA Report", key="generate_report"):
            with st.spinner("🔮 Omega is generating your comprehensive EDA report..."):
                try:
                    # Generate HTML report
                    html_report = generate_omega_report_html(df, uploaded_file.name)
                    
                    st.markdown('<div class="success-box">✅ Omega EDA Report generated successfully!</div>', 
                               unsafe_allow_html=True)
                    
                    # Display download button
                    st.download_button(
                        label="📥 Download Omega EDA Report (HTML)",
                        data=html_report,
                        file_name=f"omega_eda_report_{uploaded_file.name.replace('.csv', '.html')}",
                        mime="text/html"
                    )
                    
                    # Show preview
                    with st.expander("📖 Report Preview", expanded=False):
                        st.components.v1.html(html_report, height=600, scrolling=True)
                        
                except Exception as e:
                    st.markdown(f'<div class="warning-box">❌ Error generating report: {e}</div>', unsafe_allow_html=True)

        # --- ydata-profiling (ProfileReport) ---
        st.markdown('<h2 class="sub-header">🧑‍🔬 ydata-profiling Report</h2>', unsafe_allow_html=True)
        st.markdown('<div class="info-box">Generate a full profiling report using ydata-profiling (pandas-profiling successor).</div>', unsafe_allow_html=True)
        if st.button("🧑‍🔬 Generate ydata-profiling Report", key="profile_report"):
            with st.spinner("Generating ydata-profiling report..."):
                try:
                    profile = ProfileReport(df, title=f"ydata-profiling Report: {uploaded_file.name}", explorative=True)
                    profile_html = profile.to_html()
                    st.markdown('<div class="success-box">✅ ydata-profiling report generated successfully!</div>', unsafe_allow_html=True)
                    st.download_button(
                        label="📥 Download ydata-profiling Report (HTML)",
                        data=profile_html,
                        file_name=f"profile_report_{uploaded_file.name.replace('.csv', '.html')}",
                        mime="text/html"
                    )
                    with st.expander("📖 ydata-profiling Report Preview", expanded=False):
                        st.components.v1.html(profile_html, height=600, scrolling=True)
                except Exception as e:
                    st.markdown(f'<div class="warning-box">❌ Error generating ydata-profiling report: {e}</div>', unsafe_allow_html=True)

        # --- D-Tale Integration ---
        st.markdown('<h2 class="sub-header">🧑‍💻 D-Tale Interactive Exploration</h2>', unsafe_allow_html=True)
        st.markdown('<div class="info-box">Launch D-Tale for interactive DataFrame exploration in a new browser tab.</div>', unsafe_allow_html=True)
        if st.button("🧑‍💻 Launch D-Tale", key="dtale_launch"):
            try:
                port = find_free_port()
                d = dtale.show(df, port=port, open_browser=False)
                dtale_url = f"http://localhost:{port}"
                st.markdown(f'<div class="success-box">✅ D-Tale launched! <a href="{dtale_url}" target="_blank">Open D-Tale in a new tab</a></div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="warning-box">❌ Error launching D-Tale: {e}</div>', unsafe_allow_html=True)
    else:
        st.info("👈 Please upload a CSV file to get started.")

if __name__ == "__main__":
    main()
