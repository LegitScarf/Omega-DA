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
    """Generate a custom HTML EDA report"""
    
    # Basic info
    n_rows, n_cols = df.shape
    missing_cells = df.isnull().sum().sum()
    missing_percent = (missing_cells / (n_rows * n_cols)) * 100
    duplicate_rows = df.duplicated().sum()
    memory_usage = df.memory_usage(deep=True).sum() / 1024**2
    
    # Data types
    numeric_cols = list(df.select_dtypes(include=[np.number]).columns)
    categorical_cols = list(df.select_dtypes(include=['object']).columns)
    datetime_cols = list(df.select_dtypes(include=['datetime64']).columns)
    
    # Generate HTML report
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Omega EDA Report - {filename}</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background-color: #f8f9fa; }}
            .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 40px; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }}
            .header {{ text-align: center; color: #2E86AB; border-bottom: 3px solid #2E86AB; padding-bottom: 20px; margin-bottom: 40px; }}
            .section {{ margin: 30px 0; }}
            .section h2 {{ color: #A23B72; border-bottom: 2px solid #A23B72; padding-bottom: 10px; }}
            .metric-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
            .metric-card {{ background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%); padding: 20px; border-radius: 10px; text-align: center; border: 2px solid #2E86AB; }}
            .metric-value {{ font-size: 2em; font-weight: bold; color: #A23B72; }}
            .metric-label {{ color: #2E86AB; font-weight: 600; }}
            .table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            .table th, .table td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
            .table th {{ background-color: #2E86AB; color: white; }}
            .table tr:hover {{ background-color: #f5f5f5; }}
            .warning {{ background-color: #fff3cd; border: 1px solid #ffeaa7; color: #856404; padding: 15px; border-radius: 8px; }}
            .success {{ background-color: #d4edda; border: 1px solid #c3e6cb; color: #155724; padding: 15px; border-radius: 8px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔮 OMEGA EDA REPORT</h1>
                <p>Dataset: {filename}</p>
                <p>Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="section">
                <h2>📊 Dataset Overview</h2>
                <div class="metric-grid">
                    <div class="metric-card">
                        <div class="metric-value">{n_rows:,}</div>
                        <div class="metric-label">Rows</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{n_cols}</div>
                        <div class="metric-label">Columns</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{memory_usage:.1f} MB</div>
                        <div class="metric-label">Memory Usage</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{missing_percent:.1f}%</div>
                        <div class="metric-label">Missing Data</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{duplicate_rows:,}</div>
                        <div class="metric-label">Duplicate Rows</div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>🔍 Column Information</h2>
                <table class="table">
                    <thead>
                        <tr>
                            <th>Column</th>
                            <th>Data Type</th>
                            <th>Non-Null Count</th>
                            <th>Missing Count</th>
                            <th>Missing %</th>
                            <th>Unique Values</th>
                        </tr>
                    </thead>
                    <tbody>
    """
    
    # Add column information
    for col in df.columns:
        non_null = df[col].count()
        missing = df[col].isnull().sum()
        missing_pct = (missing / len(df)) * 100
        unique_vals = df[col].nunique()
        dtype = str(df[col].dtype)
        
        html_content += f"""
                        <tr>
                            <td><strong>{col}</strong></td>
                            <td>{dtype}</td>
                            <td>{non_null:,}</td>
                            <td>{missing:,}</td>
                            <td>{missing_pct:.1f}%</td>
                            <td>{unique_vals:,}</td>
                        </tr>
        """
    
    html_content += """
                    </tbody>
                </table>
            </div>
    """
    
    # Add statistics for numeric columns
    if numeric_cols:
        html_content += """
            <div class="section">
                <h2>📈 Numeric Columns Statistics</h2>
                <table class="table">
                    <thead>
                        <tr>
                            <th>Column</th>
                            <th>Mean</th>
                            <th>Std</th>
                            <th>Min</th>
                            <th>25%</th>
                            <th>50%</th>
                            <th>75%</th>
                            <th>Max</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for col in numeric_cols:
            desc = df[col].describe()
            html_content += f"""
                        <tr>
                            <td><strong>{col}</strong></td>
                            <td>{desc['mean']:.2f}</td>
                            <td>{desc['std']:.2f}</td>
                            <td>{desc['min']:.2f}</td>
                            <td>{desc['25%']:.2f}</td>
                            <td>{desc['50%']:.2f}</td>
                            <td>{desc['75%']:.2f}</td>
                            <td>{desc['max']:.2f}</td>
                        </tr>
            """
        
        html_content += """
                    </tbody>
                </table>
            </div>
        """
    
    # Add categorical columns info
    if categorical_cols:
        html_content += """
            <div class="section">
                <h2>📝 Categorical Columns</h2>
                <table class="table">
                    <thead>
                        <tr>
                            <th>Column</th>
                            <th>Unique Values</th>
                            <th>Most Frequent</th>
                            <th>Frequency</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for col in categorical_cols[:10]:  # Limit to first 10 categorical columns
            unique_count = df[col].nunique()
            if unique_count > 0:
                most_frequent = df[col].value_counts().index[0]
                frequency = df[col].value_counts().iloc[0]
                html_content += f"""
                            <tr>
                                <td><strong>{col}</strong></td>
                                <td>{unique_count:,}</td>
                                <td>{most_frequent}</td>
                                <td>{frequency:,}</td>
                            </tr>
                """
        
        html_content += """
                    </tbody>
                </table>
            </div>
        """
    
    # Data quality warnings
    html_content += """
            <div class="section">
                <h2>⚠️ Data Quality Insights</h2>
    """
    
    # Check for issues
    issues = []
    if missing_percent > 10:
        issues.append(f"High missing data: {missing_percent:.1f}% of cells are missing")
    if duplicate_rows > 0:
        issues.append(f"Found {duplicate_rows:,} duplicate rows")
    
    high_missing_cols = df.columns[df.isnull().sum() / len(df) > 0.5].tolist()
    if high_missing_cols:
        issues.append(f"Columns with >50% missing data: {', '.join(high_missing_cols)}")
    
    if issues:
        for issue in issues:
            html_content += f'<div class="warning">⚠️ {issue}</div>'
    else:
        html_content += '<div class="success">✅ No major data quality issues detected!</div>'
    
    html_content += """
            </div>
            
            <div class="section">
                <h2>🎯 Summary</h2>
                <p>This report was generated by <strong>Omega EDA Tool</strong>, providing comprehensive insights into your dataset.</p>
                <p><strong>Key Findings:</strong></p>
                <ul>
    """
    
    # Add key findings
    html_content += f"<li>Dataset contains {n_rows:,} rows and {n_cols} columns</li>"
    html_content += f"<li>{len(numeric_cols)} numeric columns and {len(categorical_cols)} categorical columns</li>"
    html_content += f"<li>Overall data completeness: {100 - missing_percent:.1f}%</li>"
    
    if duplicate_rows == 0:
        html_content += "<li>No duplicate rows found</li>"
    else:
        html_content += f"<li>{duplicate_rows:,} duplicate rows detected</li>"
    
    html_content += """
                </ul>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content

def display_dataset_info(df):
    """Display basic information about the dataset"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{df.shape[0]:,}</div>
            <div class="stat-label">Rows</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{df.shape[1]}</div>
            <div class="stat-label">Columns</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        memory_mb = df.memory_usage(deep=True).sum() / 1024**2
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{memory_mb:.1f} MB</div>
            <div class="stat-label">Memory</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        missing_count = df.isnull().sum().sum()
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{missing_count:,}</div>
            <div class="stat-label">Missing</div>
        </div>
        """, unsafe_allow_html=True)

def create_visualizations(df):
    """Create comprehensive visualizations for the dataset"""
    
    st.markdown('<h2 class="sub-header">📊 Data Visualizations</h2>', unsafe_allow_html=True)
    
    # Data type distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔢 Data Types Distribution")
        dtype_counts = df.dtypes.value_counts()
        fig = px.pie(
            values=dtype_counts.values, 
            names=dtype_counts.index.astype(str),
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
        st.subheader("🔍 Missing Values Analysis")
        missing_data = df.isnull().sum()
        missing_data = missing_data[missing_data > 0].sort_values(ascending=True)
        
        if len(missing_data) > 0:
            fig = px.bar(
                x=missing_data.values,
                y=missing_data.index,
                orientation='h',
                title="Missing Values by Column",
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
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_cols) > 0:
        st.subheader("📈 Numeric Columns Analysis")
        
        # Distribution plots
        selected_cols = st.multiselect(
            "Select numeric columns to analyze:",
            numeric_cols,
            default=numeric_cols[:3] if len(numeric_cols) >= 3 else numeric_cols
        )
        
        if selected_cols:
            # Create subplots for distributions
            n_cols = min(2, len(selected_cols))
            n_rows = (len(selected_cols) + 1) // 2
            
            fig = make_subplots(
                rows=n_rows, 
                cols=n_cols,
                subplot_titles=selected_cols,
                vertical_spacing=0.1
            )
            
            for i, col in enumerate(selected_cols):
                row = (i // n_cols) + 1
                col_pos = (i % n_cols) + 1
                
                fig.add_trace(
                    go.Histogram(x=df[col], name=col, nbinsx=30),
                    row=row, col=col_pos
                )
            
            fig.update_layout(
                height=300 * n_rows,
                title_text="Distribution of Selected Numeric Columns",
                showlegend=False,
                plot_bgcolor='white',
                paper_bgcolor='white'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Box plots
            if len(selected_cols) > 1:
                st.subheader("📦 Box Plots for Outlier Detection")
                fig = go.Figure()
                
                for col in selected_cols:
                    fig.add_trace(go.Box(y=df[col], name=col))
                
                fig.update_layout(
                    title="Box Plots - Outlier Detection",
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font_color='#2E86AB'
                )
                st.plotly_chart(fig, use_container_width=True)
    
    # Correlation analysis
    if len(numeric_cols) > 1:
        st.subheader("🔗 Correlation Analysis")
        corr_matrix = df[numeric_cols].corr()
        
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            title="Correlation Matrix",
            color_continuous_scale='RdYlBu'
        )
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font_color='#2E86AB'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Categorical columns analysis
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    if len(categorical_cols) > 0:
        st.subheader("📝 Categorical Columns Analysis")
        
        selected_cat_col = st.selectbox(
            "Select a categorical column to analyze:",
            categorical_cols
        )
        
        if selected_cat_col:
            # Value counts
            value_counts = df[selected_cat_col].value_counts().head(10)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(
                    x=value_counts.index,
                    y=value_counts.values,
                    title=f"Top 10 Values in {selected_cat_col}",
                    color=value_counts.values,
                    color_continuous_scale='Blues'
                )
                fig.update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font_color='#2E86AB'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.pie(
                    values=value_counts.values,
                    names=value_counts.index,
                    title=f"Distribution of {selected_cat_col}"
                )
                fig.update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font_color='#2E86AB'
                )
                st.plotly_chart(fig, use_container_width=True)

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
                        st.
