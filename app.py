import os
import streamlit as st
from openai import OpenAI
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import base64
from PIL import Image
import io
import tempfile

# Configure Streamlit page
st.set_page_config(
    page_title="Omega - AI Data Analyst",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for sleek white background design
st.markdown("""
<style>
    /* Main background */
    .main {
        background-color: #ffffff;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Custom header styling */
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        font-family: 'Arial', sans-serif;
    }
    
    .main-header p {
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.9;
        font-family: 'Arial', sans-serif;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        font-family: 'Arial', sans-serif;
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        color: #1976d2;
    }
    
    .assistant-message {
        background-color: #f1f8e9;
        border-left: 4px solid #4caf50;
        color: #388e3c;
    }
    
    .error-message {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
        color: #d32f2f;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background-color: #ffffff;
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        color: #333333;
        font-family: 'Arial', sans-serif;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        font-family: 'Arial', sans-serif;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    /* File uploader styling */
    .uploadedFile {
        background-color: #f8f9fa;
        border: 2px dashed #667eea;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        color: #333333;
        font-family: 'Arial', sans-serif;
    }
    
    /* Metrics styling */
    .metric-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        text-align: center;
        color: #333333;
        font-family: 'Arial', sans-serif;
    }
    
    /* Loading animation */
    .loading {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }
    
    .spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #667eea;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Text styling */
    .stMarkdown {
        color: #333333;
        font-family: 'Arial', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #333333;
        font-family: 'Arial', sans-serif;
    }
    
    p {
        color: #555555;
        font-family: 'Arial', sans-serif;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# Initialize OpenAI client
@st.cache_resource
def init_openai():
    api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("⚠️ OpenAI API key not found. Please set it in Streamlit secrets or environment variables.")
        st.stop()
    return OpenAI(api_key=api_key)

def query_agent(data, query, client):
    """Query Checker Agent - verifies if requested columns exist in dataset"""
    system_prompt = """
Role:
You are a Query Checker Agent. Your sole job is to verify if the user's request involves columns
that are present in the dataset provided.

Behavior:
- Read the user query and identify column names that may be mentioned
- Match those with the dataset's column headers
- If ALL required columns exist in the dataset, return: yes
- If ANY column is missing, return: no

Constraints:
- Your response must be exactly one word: yes or no
- No extra text, no explanation
"""
    
    dataset_info = f"Dataset columns: {list(data.columns)}\nSample data:\n{data.head().to_string()}"
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Dataset:\n{dataset_info}\n\nUser Prompt:\n{query}"}
        ]
    )
    return response.choices[0].message.content.strip().lower()

def coder_agent(data, query, client):
    """Coder Agent - generates matplotlib visualization code"""
    system_prompt = """
Role:
You are an advanced visualization agent that writes Python code using matplotlib
to generate insightful visualizations.

Constraints:
- Do not include plt.show() in the code
- End with: fig.savefig('plot.png', dpi=300, bbox_inches='tight'); plt.close()
- Use matplotlib and pandas only
- The data is available as pandas DataFrame named 'data'
- Always create a figure with: fig, ax = plt.subplots(figsize=(10, 6))
- Return ONLY executable Python code, no markdown formatting

Format:
Return only raw Python code with proper error handling.
"""

    dataset_info = f"Dataset columns: {list(data.columns)}\nDataset shape: {data.shape}\nSample data:\n{data.head().to_string()}"
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Dataset:\n{dataset_info}\n\nUser Prompt:\n{query}"}
        ]
    )
    
    code = response.choices[0].message.content.strip()
    
    # Clean code
    if code.startswith("```python"):
        code = code[9:]
    if code.startswith("```"):
        code = code[3:]
    if code.endswith("```"):
        code = code[:-3]
    
    return code.strip()

def insights_agent(image_bytes, query, client):
    """Insights Agent - generates insights from visualization"""
    try:
        encoded_image = base64.b64encode(image_bytes).decode('utf-8')
        image_data_url = f"data:image/png;base64,{encoded_image}"
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text", 
                            "text": f"Analyze this visualization created for: '{query}'. Provide detailed insights about patterns, trends, and key findings. Structure your response with clear headings and bullet points."
                        },
                        {
                            "type": "image_url", 
                            "image_url": {"url": image_data_url}
                        }
                    ]
                }
            ],
            max_tokens=800
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error generating insights: {str(e)}"

def process_query(data, query, client):
    """Central controller for processing user queries"""
    try:
        # Step 1: Validate query
        with st.spinner("🔍 Validating your query..."):
            is_valid = query_agent(data, query, client)
        
        if is_valid == "no":
            return "❌ The attributes you're looking for are not present in the dataset. Please check the available columns and try again.", None
        
        # Step 2: Generate visualization
        with st.spinner("📊 Creating your visualization..."):
            code = coder_agent(data, query, client)
            
            # Execute code in temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                plot_path = os.path.join(temp_dir, 'plot.png')
                
                # Execute the generated code
                exec_globals = {
                    'data': data, 
                    'plt': plt, 
                    'pd': pd, 
                    'np': np,
                    'os': os
                }
                
                # Modify code to save in temp directory
                modified_code = code.replace("'plot.png'", f"'{plot_path}'")
                exec(modified_code, exec_globals)
                
                # Read the generated plot
                if os.path.exists(plot_path):
                    with open(plot_path, 'rb') as f:
                        image_bytes = f.read()
                else:
                    return "❌ Failed to generate visualization.", None
        
        # Step 3: Generate insights
        with st.spinner("🧠 Analyzing insights..."):
            insights = insights_agent(image_bytes, query, client)
        
        return insights, image_bytes
        
    except Exception as e:
        return f"❌ Error processing query: {str(e)}", None

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 Omega</h1>
        <p>Multi-Agentic System for Intelligent Data Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize OpenAI client
    client = init_openai()
    
    # Sidebar for file upload and dataset info
    with st.sidebar:
        st.markdown("### 📁 Upload Your Dataset")
        uploaded_file = st.file_uploader(
            "Choose a CSV or Excel file",
            type=['csv', 'xlsx', 'xls'],
            help="Upload your dataset to start analyzing"
        )
        
        if uploaded_file:
            try:
                # Load data
                if uploaded_file.name.endswith('.csv'):
                    data = pd.read_csv(uploaded_file)
                else:
                    data = pd.read_excel(uploaded_file)
                
                st.success(f"✅ Dataset loaded successfully!")
                
                # Dataset overview
                st.markdown("### 📊 Dataset Overview")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-container">
                        <h4>Rows</h4>
                        <h2>{data.shape[0]:,}</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-container">
                        <h4>Columns</h4>
                        <h2>{data.shape[1]}</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Column information
                st.markdown("### 📋 Available Columns")
                for col in data.columns:
                    st.markdown(f"• **{col}** ({data[col].dtype})")
                
                # Sample data
                with st.expander("👀 Preview Data"):
                    st.dataframe(data.head(), use_container_width=True)
                
            except Exception as e:
                st.error(f"❌ Error loading dataset: {str(e)}")
                data = None
        else:
            data = None
            st.info("👆 Please upload a dataset to get started")
    
    # Main chat interface
    if data is not None:
        st.markdown("### 💬 Chat with Your Data")
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "assistant", 
                    "content": "Hello! I'm Omega, your AI data analyst. I can help you visualize and analyze your data. What would you like to explore?",
                    "type": "text"
                }
            ]
        
        # Display chat history
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>You:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                if message["type"] == "text":
                    st.markdown(f"""
                    <div class="chat-message assistant-message">
                        <strong>Omega:</strong> {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
                elif message["type"] == "visualization":
                    st.markdown(f"""
                    <div class="chat-message assistant-message">
                        <strong>Omega:</strong> Here's your visualization and analysis:
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.image(message["image"], caption="Generated Visualization", use_column_width=True)
                    with col2:
                        st.markdown(message["insights"])
        
        # Chat input
        user_query = st.chat_input("Ask me anything about your data...")
        
        if user_query:
            # Add user message
            st.session_state.messages.append({
                "role": "user", 
                "content": user_query,
                "type": "text"
            })
            
            # Process query
            insights, image_bytes = process_query(data, user_query, client)
            
            if image_bytes:
                # Add visualization message
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Here's your visualization and analysis:",
                    "type": "visualization",
                    "image": image_bytes,
                    "insights": insights
                })
            else:
                # Add text response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": insights,
                    "type": "text"
                })
            
            st.rerun()
    
    else:
        # Welcome screen
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: #666;">
            <h2>Welcome to Omega! 🚀</h2>
            <p style="font-size: 1.2rem; margin-bottom: 2rem;">
                Your intelligent companion for data analysis and visualization
            </p>
            <div style="background: #f8f9fa; padding: 2rem; border-radius: 12px; margin: 2rem 0;">
                <h3 style="color: #333; margin-bottom: 1rem;">How it works:</h3>
                <div style="text-align: left; max-width: 600px; margin: 0 auto;">
                    <p><strong>1. Upload:</strong> Share your CSV or Excel dataset</p>
                    <p><strong>2. Chat:</strong> Ask questions about your data in natural language</p>
                    <p><strong>3. Visualize:</strong> Get intelligent charts and insights instantly</p>
                    <p><strong>4. Analyze:</strong> Receive detailed analysis and recommendations</p>
                </div>
            </div>
            <p style="color: #888;">Start by uploading a dataset in the sidebar! 👈</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
