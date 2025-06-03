import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
import dtale
import tempfile
import os
import base64
from io import StringIO
import threading
import time
import webbrowser
from streamlit.components.v1 import html

# Set page configuration
st.set_page_config(
    page_title="Omega",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin: 1rem 0;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        margin: 1rem 0;
    }
    .stButton > button {
        width: 100%;
        height: 3rem;
        font-size: 1.2rem;
        font-weight: bold;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def load_dataset(uploaded_file):
    """Load CSV dataset from uploaded file"""
    try:
        # Read CSV file
        df = pd.read_csv(uploaded_file)
        return df, None
    except Exception as e:
        return None, str(e)

def generate_profile_report(df, title="Automated EDA Report"):
    """Generate ydata-profiling report"""
    try:
        with st.spinner("Generating comprehensive EDA report... This may take a few minutes."):
            # Create profile report with optimized settings for web display
            profile = ProfileReport(
                df, 
                title=title,
                explorative=True,
                minimal=False,
                interactions=None,  # Disable interactions for faster processing
                correlations={
                    "auto": {"calculate": True, "warn_high_correlations": True},
                    "pearson": {"calculate": True, "warn_high_correlations": True},
                    "spearman": {"calculate": True, "warn_high_correlations": True},
                    "kendall": {"calculate": False},  # Disable for faster processing
                    "phi_k": {"calculate": False},
                    "cramers": {"calculate": False},
                }
            )
            return profile, None
    except Exception as e:
        return None, str(e)

def display_profile_report(profile):
    """Display the profile report in Streamlit"""
    try:
        # Convert report to HTML
        report_html = profile.to_html()
        
        # Display the report
        st.components.v1.html(report_html, height=800, scrolling=True)
        
        # Provide download option
        st.download_button(
            label="📥 Download EDA Report (HTML)",
            data=report_html,
            file_name="eda_report.html",
            mime="text/html"
        )
        
        return True
    except Exception as e:
        st.error(f"Error displaying report: {str(e)}")
        return False

def launch_dtale(df):
    """Launch D-Tale for interactive analysis"""
    try:
        # Create D-Tale instance
        dtale_instance = dtale.show(df, open_browser=False)
        dtale_url = f"http://localhost:{dtale_instance.port}"
        
        return dtale_instance, dtale_url, None
    except Exception as e:
        return None, None, str(e)

def display_dataset_info(df):
    """Display basic information about the dataset"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Rows", df.shape[0])
    with col2:
        st.metric("Columns", df.shape[1])
    with col3:
        st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    with col4:
        st.metric("Missing Values", df.isnull().sum().sum())

def main():
    # Main header
    st.markdown('<h1 class="main-header">📊 Interactive EDA Tool</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🛠️ Tool Features")
        st.markdown("""
        1. **Upload CSV File** 📁
        2. **Automated EDA** with ydata-profiling 📈
        3. **Interactive Analysis** with D-Tale 🔍
        4. **Download Reports** 💾
        """)
        
        st.markdown("---")
        st.markdown("### 📋 Instructions")
        st.markdown("""
        1. Upload your CSV file using the file uploader
        2. Review dataset information
        3. Generate automated EDA report
        4. Optionally launch D-Tale for custom analysis
        """)
    
    # File uploader
    st.markdown('<h2 class="sub-header">📁 Upload Your Dataset</h2>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        help="Upload a CSV file to perform automated EDA analysis"
    )
    
    if uploaded_file is not None:
        # Load dataset
        df, error = load_dataset(uploaded_file)
        
        if error:
            st.error(f"❌ Error loading dataset: {error}")
            return
        
        # Display success message
        st.markdown(f'<div class="success-box">✅ Dataset "{uploaded_file.name}" loaded successfully!</div>', 
                   unsafe_allow_html=True)
        
        # Dataset information
        st.markdown('<h2 class="sub-header">📋 Dataset Overview</h2>', unsafe_allow_html=True)
        display_dataset_info(df)
        
        # Show first few rows
        with st.expander("👀 Preview Dataset (First 10 rows)", expanded=False):
            st.dataframe(df.head(10), use_container_width=True)
        
        # Show data types
        with st.expander("🔍 Column Information", expanded=False):
            col_info = pd.DataFrame({
                'Column': df.columns,
                'Data Type': df.dtypes,
                'Non-Null Count': df.count(),
                'Missing Values': df.isnull().sum(),
                'Missing %': (df.isnull().sum() / len(df) * 100).round(2)
            })
            st.dataframe(col_info, use_container_width=True)
        
        st.markdown("---")
        
        # EDA Section
        st.markdown('<h2 class="sub-header">📊 Automated EDA Report</h2>', unsafe_allow_html=True)
        st.markdown('<div class="info-box">🤖 Generate a comprehensive automated EDA report using ydata-profiling</div>', 
                   unsafe_allow_html=True)
        
        if st.button("🚀 Generate EDA Report", key="generate_eda"):
            # Generate profile report
            profile, error = generate_profile_report(df, f"EDA Report - {uploaded_file.name}")
            
            if error:
                st.error(f"❌ Error generating report: {error}")
            else:
                st.success("✅ EDA Report generated successfully!")
                
                # Display the report
                st.markdown("### 📈 Interactive EDA Report")
                display_profile_report(profile)
                
                # Store profile in session state for potential reuse
                st.session_state['profile_report'] = profile
        
        st.markdown("---")
        
        # D-Tale Section
        st.markdown('<h2 class="sub-header">🔍 Advanced Interactive Analysis</h2>', unsafe_allow_html=True)
        st.markdown('<div class="info-box">🎛️ Launch D-Tale for advanced interactive data exploration and visualization</div>', 
                   unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("🎛️ Launch D-Tale Analysis", key="launch_dtale"):
                with st.spinner("Launching D-Tale interactive analysis..."):
                    dtale_instance, dtale_url, error = launch_dtale(df)
                    
                    if error:
                        st.error(f"❌ Error launching D-Tale: {error}")
                    else:
                        st.success("✅ D-Tale launched successfully!")
                        st.markdown(f'<div class="success-box">🌐 D-Tale is running at: <a href="{dtale_url}" target="_blank">{dtale_url}</a></div>', 
                                   unsafe_allow_html=True)
                        
                        # Embed D-Tale in an iframe (optional)
                        st.markdown("### 🎛️ D-Tale Interactive Interface")
                        st.markdown("Click the link above to open D-Tale in a new tab, or use the embedded version below:")
                        
                        # Note: D-Tale embedding might not work in all deployments due to security restrictions
                        try:
                            st.components.v1.iframe(dtale_url, height=600, scrolling=True)
                        except:
                            st.info("💡 If the embedded version doesn't work, please use the direct link above.")
                        
                        # Store instance in session state
                        st.session_state['dtale_instance'] = dtale_instance
                        st.session_state['dtale_url'] = dtale_url
        
        with col2:
            if 'dtale_instance' in st.session_state:
                if st.button("🛑 Stop D-Tale Server", key="stop_dtale"):
                    try:
                        st.session_state['dtale_instance'].kill()
                        del st.session_state['dtale_instance']
                        del st.session_state['dtale_url']
                        st.success("✅ D-Tale server stopped successfully!")
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"❌ Error stopping D-Tale: {str(e)}")
        
        # Additional features
        st.markdown("---")
        st.markdown('<h2 class="sub-header">💾 Export Options</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Download processed dataset
            csv_buffer = StringIO()
            df.to_csv(csv_buffer, index=False)
            st.download_button(
                label="📥 Download Processed Dataset (CSV)",
                data=csv_buffer.getvalue(),
                file_name=f"processed_{uploaded_file.name}",
                mime="text/csv"
            )
        
        with col2:
            # Download dataset info
            if st.button("📋 Generate Dataset Summary Report"):
                summary_report = f"""
# Dataset Summary Report
**File:** {uploaded_file.name}
**Generated:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

## Basic Information
- **Rows:** {df.shape[0]:,}
- **Columns:** {df.shape[1]:,}
- **Memory Usage:** {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB
- **Missing Values:** {df.isnull().sum().sum():,}

## Column Details
{df.dtypes.to_frame('Data Type').to_markdown()}

## Missing Values by Column
{df.isnull().sum().to_frame('Missing Count').to_markdown()}

## Basic Statistics
{df.describe().to_markdown()}
                """
                
                st.download_button(
                    label="📥 Download Summary Report (Markdown)",
                    data=summary_report,
                    file_name=f"summary_{uploaded_file.name.replace('.csv', '.md')}",
                    mime="text/markdown"
                )
    
    else:
        # Welcome message when no file is uploaded
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background-color: #f8f9fa; border-radius: 1rem; margin: 2rem 0;">
            <h2>🚀 Welcome to the Interactive EDA Tool!</h2>
            <p style="font-size: 1.2rem; color: #6c757d;">
                Upload a CSV file to get started with automated exploratory data analysis
            </p>
            <p>
                📊 <strong>ydata-profiling</strong> for comprehensive automated EDA<br>
                🎛️ <strong>D-Tale</strong> for interactive data exploration
            </p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
