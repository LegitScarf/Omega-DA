import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
import tempfile
import os
from io import StringIO
import base64

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
</style>
""", unsafe_allow_html=True)

def load_dataset(uploaded_file):
    """Load CSV dataset from uploaded file"""
    try:
        df = pd.read_csv(uploaded_file)
        return df, None
    except Exception as e:
        return None, str(e)

def generate_profile_report(df, title="Omega EDA Report"):
    """Generate ydata-profiling report with optimized settings for cloud deployment"""
    try:
        with st.spinner("🔮 Omega is analyzing your data... This may take a few minutes."):
            # Optimized profile settings for cloud deployment
            profile = ProfileReport(
                df, 
                title=title,
                minimal=True,  # Use minimal mode for faster processing
                explorative=False,  # Disable explorative mode
                interactions=None,  # Disable interactions
                correlations={
                    "auto": {"calculate": True},
                    "pearson": {"calculate": True},
                    "spearman": {"calculate": False},  # Disable for speed
                    "kendall": {"calculate": False},
                    "phi_k": {"calculate": False},
                    "cramers": {"calculate": False},
                },
                missing_diagrams={
                    "bar": True,
                    "matrix": False,  # Disable for speed
                    "heatmap": False,
                },
                duplicates={"head": 0},  # Disable duplicate analysis
                samples={"head": 5, "tail": 5}  # Limit samples
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
            label="📥 Download Omega EDA Report (HTML)",
            data=report_html,
            file_name="omega_eda_report.html",
            mime="text/html"
        )
        
        return True
    except Exception as e:
        st.error(f"Error displaying report: {str(e)}")
        return False

def display_dataset_info(df):
    """Display basic information about the dataset"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-container">
            <h3 style="color: #2E86AB; margin: 0;">Rows</h3>
            <h2 style="color: #A23B72; margin: 0;">{:,}</h2>
        </div>
        """.format(df.shape[0]), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-container">
            <h3 style="color: #2E86AB; margin: 0;">Columns</h3>
            <h2 style="color: #A23B72; margin: 0;">{}</h2>
        </div>
        """.format(df.shape[1]), unsafe_allow_html=True)
    
    with col3:
        memory_mb = df.memory_usage(deep=True).sum() / 1024**2
        st.markdown("""
        <div class="metric-container">
            <h3 style="color: #2E86AB; margin: 0;">Memory</h3>
            <h2 style="color: #A23B72; margin: 0;">{:.1f} MB</h2>
        </div>
        """.format(memory_mb), unsafe_allow_html=True)
    
    with col4:
        missing_count = df.isnull().sum().sum()
        st.markdown("""
        <div class="metric-container">
            <h3 style="color: #2E86AB; margin: 0;">Missing</h3>
            <h2 style="color: #A23B72; margin: 0;">{:,}</h2>
        </div>
        """.format(missing_count), unsafe_allow_html=True)

def create_basic_visualizations(df):
    """Create basic visualizations for the dataset"""
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        import plotly.express as px
        import plotly.graph_objects as go
        
        # Set the style
        plt.style.use('default')
        sns.set_palette("husl")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Data Types Distribution")
            dtype_counts = df.dtypes.value_counts()
            fig = px.pie(
                values=dtype_counts.values, 
                names=dtype_counts.index,
                title="Distribution of Data Types",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font_color='#2E86AB'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🔍 Missing Values by Column")
            missing_data = df.isnull().sum()
            missing_data = missing_data[missing_data > 0].sort_values(ascending=True)
            
            if len(missing_data) > 0:
                fig = px.bar(
                    x=missing_data.values,
                    y=missing_data.index,
                    orientation='h',
                    title="Missing Values Count",
                    color=missing_data.values,
                    color_continuous_scale='Reds'
                )
                fig.update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font_color='#2E86AB'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.success("🎉 No missing values found!")
        
        # Numeric columns analysis
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            st.subheader("📈 Numeric Columns Distribution")
            selected_col = st.selectbox("Select a numeric column to visualize:", numeric_cols)
            
            if selected_col:
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = px.histogram(
                        df, 
                        x=selected_col, 
                        title=f"Distribution of {selected_col}",
                        color_discrete_sequence=['#2E86AB']
                    )
                    fig.update_layout(
                        plot_bgcolor='white',
                        paper_bgcolor='white',
                        font_color='#2E86AB'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    fig = px.box(
                        df, 
                        y=selected_col, 
                        title=f"Box Plot of {selected_col}",
                        color_discrete_sequence=['#A23B72']
                    )
                    fig.update_layout(
                        plot_bgcolor='white',
                        paper_bgcolor='white',
                        font_color='#2E86AB'
                    )
                    st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.warning(f"Could not generate visualizations: {str(e)}")

def main():
    # Main header with Omega branding
    st.markdown('<h1 class="main-header">🔮 OMEGA</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #6c757d; margin-bottom: 3rem;">Advanced Exploratory Data Analysis Tool</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🔮 Omega Features")
        st.markdown("""
        1. **Smart Upload** 📁 - Intelligent CSV processing
        2. **Auto Analysis** 📊 - Comprehensive EDA reports  
        3. **Visual Insights** 📈 - Interactive charts
        4. **Export Ready** 💾 - Download your reports
        """)
        
        st.markdown("---")
        st.markdown("### 🚀 Quick Start")
        st.markdown("""
        1. Upload your CSV dataset
        2. Review the data overview
        3. Generate your EDA report
        4. Explore visualizations
        5. Download results
        """)
        
        st.markdown("---")
        st.markdown("### ℹ️ About Omega")
        st.markdown("""
        Omega is your intelligent companion for exploratory data analysis. 
        Built with cutting-edge tools to provide comprehensive insights 
        into your datasets.
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
                'Missing %': (df.isnull().sum() / len(df) * 100).round(2)
            })
            st.dataframe(col_info, use_container_width=True)
        
        st.markdown("---")
        
        # Quick Visualizations
        st.markdown('<h2 class="sub-header">📊 Quick Insights</h2>', unsafe_allow_html=True)
        create_basic_visualizations(df)
        
        st.markdown("---")
        
        # EDA Section
        st.markdown('<h2 class="sub-header">🔮 Omega EDA Report</h2>', unsafe_allow_html=True)
        st.markdown('<div class="info-box">🤖 Generate a comprehensive automated EDA report powered by Omega intelligence</div>', 
                   unsafe_allow_html=True)
        
        if st.button("🚀 Generate Omega EDA Report", key="generate_eda"):
            # Generate profile report
            profile, error = generate_profile_report(df, f"Omega EDA Report - {uploaded_file.name}")
            
            if error:
                st.markdown(f'<div class="warning-box">❌ Error generating report: {error}</div>', 
                           unsafe_allow_html=True)
            else:
                st.markdown('<div class="success-box">✅ Omega EDA Report generated successfully!</div>', 
                           unsafe_allow_html=True)
                
                # Display the report
                st.markdown("### 📈 Interactive Omega EDA Report")
                display_profile_report(profile)
                
                # Store profile in session state
                st.session_state['profile_report'] = profile
        
        st.markdown("---")
        
        # Export section
        st.markdown('<h2 class="sub-header">💾 Export & Download</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Download processed dataset
            csv_buffer = StringIO()
            df.to_csv(csv_buffer, index=False)
            st.download_button(
                label="📥 Download Dataset (CSV)",
                data=csv_buffer.getvalue(),
                file_name=f"omega_processed_{uploaded_file.name}",
                mime="text/csv"
            )
        
        with col2:
            # Generate and download summary report
            if st.button("📋 Generate Summary Report"):
                summary_report = f"""# Omega Dataset Analysis Summary

**Dataset:** {uploaded_file.name}  
**Generated by:** Omega EDA Tool  
**Timestamp:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 Dataset Overview
- **Total Rows:** {df.shape[0]:,}
- **Total Columns:** {df.shape[1]:,}
- **Memory Usage:** {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB
- **Missing Values:** {df.isnull().sum().sum():,}

## 📋 Column Information
{col_info.to_markdown(index=False)}

## 📈 Basic Statistics
{df.describe().to_markdown()}

## 🔍 Data Quality Summary
- **Complete Columns:** {(df.isnull().sum() == 0).sum()}
- **Columns with Missing Data:** {(df.isnull().sum() > 0).sum()}
- **Numeric Columns:** {len(df.select_dtypes(include=['number']).columns)}
- **Text Columns:** {len(df.select_dtypes(include=['object']).columns)}

---
*Generated by Omega - Advanced EDA Tool*
"""
                
                st.download_button(
                    label="📥 Download Summary (Markdown)",
                    data=summary_report,
                    file_name=f"omega_summary_{uploaded_file.name.replace('.csv', '.md')}",
                    mime="text/markdown"
                )
    
    else:
        # Welcome message
        st.markdown("""
        <div style="text-align: center; padding: 4rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 20px; margin: 2rem 0; border: 2px solid #2E86AB;">
            <h2 style="color: #2E86AB; margin-bottom: 1rem;">🚀 Welcome to Omega!</h2>
            <p style="font-size: 1.3rem; color: #6c757d; margin-bottom: 2rem;">
                Your intelligent companion for exploratory data analysis
            </p>
            <div style="background-color: white; padding: 2rem; border-radius: 15px; margin: 1rem 0;">
                <p style="color: #2E86AB; font-size: 1.1rem; margin: 0;">
                    🔮 <strong>Advanced Analytics</strong> • 📊 <strong>Beautiful Reports</strong> • 🚀 <strong>Lightning Fast</strong>
                </p>
            </div>
            <p style="color: #A23B72; font-size: 1rem; margin-top: 1rem;">
                Upload your CSV file above to begin your data exploration journey
            </p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
