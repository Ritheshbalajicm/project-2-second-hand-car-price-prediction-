# File: pages/1_📊_EDA_Dashboard.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

import base64

# Function to get base64 of image for CSS
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_bg(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Set the cinematic background
set_bg('src/bg_eda_v2.png')

# --- Page Configuration ---
st.set_page_config(
    page_title="CarVault | Diagnostic Analytics",
    page_icon="📊",
    layout="wide"
)

# --- Custom CSS for 10/10 Premium UI ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;900&display=swap');

    :root {
        --primary: #00d2ff;
        --secondary: #92fe9d;
        --bg-dark: #0f172a;
        --glass: rgba(255, 255, 255, 0.05);
        --glass-border: rgba(255, 255, 255, 0.1);
        --text-glow: 0 0 15px rgba(0, 210, 255, 0.5);
    }

    .stApp {
        font-family: 'Outfit', sans-serif;
        color: #ffffff;
    }

    /* Hyper-dark Cinematic Overlay for extreme readability */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: radial-gradient(circle at center, rgba(15, 23, 42, 0.95), rgba(2, 6, 23, 0.98));
        backdrop-filter: blur(8px);
        z-index: -1;
    }

    /* Ambient Background Animation */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: url('https://www.transparenttextures.com/patterns/carbon-fibre.png');
        opacity: 0.05;
        z-index: -1;
    }

    /* Sidebar Glassmorphism */
    section[data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid var(--glass-border);
    }
    
    section[data-testid="stSidebar"] * {
        color: #cbd5e1 !important;
    }

    /* Solidified Glass Cards for maximum contrast */
    .form-container {
        background: rgba(30, 41, 59, 0.96); /* Almost opaque */
        backdrop-filter: blur(20px);
        padding: 2.5rem;
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.9);
        margin-bottom: 2rem;
    }

    h1, h2, h3 {
        color: var(--primary) !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
        text-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }

    p, li, span, label {
        color: #ffffff !important;
        font-weight: 500 !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.6);
    }

    /* High-contrast Table and Dataframe Styling */
    div.stDataFrame, div.stTable, [data-testid="stTable"] {
        background: #1e293b !important;
        border: 1px solid rgba(0, 210, 255, 0.4) !important;
        border-radius: 16px !important;
        padding: 10px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
    }
    
    [data-testid="stTable"] th {
        background-color: #0f172a !important;
        color: #00d2ff !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stTable"] td {
        color: #ffffff !important;
    }

    /* Selectbox styling */
    div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 12px !important;
        color: white !important;
    }

    /* Radio button styling */
    div[data-testid="stWidgetLabel"] p {
        color: #94a3b8 !important;
        font-weight: 600 !important;
    }

</style>
""", unsafe_allow_html=True)

# --- Cache data loading ---
@st.cache_data
def load_data(data_path):
    try:
        return pd.read_csv(data_path)
    except Exception:
        return None

# --- Plot helpers ---
@st.cache_data
def cached_univariate_plot(df, feature):
    buf = io.BytesIO()
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6))
    if pd.api.types.is_numeric_dtype(df[feature]):
        sns.histplot(df[feature], kde=True, bins=30, color='#00d2ff', ax=ax)
    else:
        df[feature].value_counts().head(15).plot(kind="bar", color='#00d2ff', ax=ax)
    
    ax.set_title(f"Distribution of {feature}", color='white', fontsize=18, pad=20)
    ax.set_facecolor('#1e293b') # Solid dark background for plot
    fig.patch.set_facecolor('#1e293b') # Solid dark background for figure
    plt.tight_layout()
    plt.savefig(buf, format="png", transparent=False) # No transparency for clarity
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode("utf-8")

@st.cache_data
def cached_bivariate_plot(df, x_feature, y_feature):
    buf = io.BytesIO()
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x=x_feature, y=y_feature, alpha=0.8, color='#92fe9d', ax=ax)
    ax.set_title(f"{x_feature} vs {y_feature}", color='white', fontsize=18, pad=20)
    ax.set_facecolor('#1e293b')
    fig.patch.set_facecolor('#1e293b')
    plt.tight_layout()
    plt.savefig(buf, format="png", transparent=False)
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode("utf-8")

@st.cache_data
def cached_heatmap(df):
    buf = io.BytesIO()
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(12, 10))
    corr = df.corr(numeric_only=True)
    sns.heatmap(corr, annot=True, cmap="mako", fmt=".2f", cbar=True, ax=ax, annot_kws={"size": 12, "weight": "bold"})
    ax.set_title("Correlation Correlation Matrix", color='white', fontsize=18, pad=20)
    ax.set_facecolor('#1e293b')
    fig.patch.set_facecolor('#1e293b')
    plt.tight_layout()
    plt.savefig(buf, format="png", transparent=False)
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode("utf-8")

# --- Load dataset ---
df = load_data("src/cars24_cleaned.csv")

st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>📊 Diagnostic Analytics Dashboard</h1>", unsafe_allow_html=True)

if df is None:
    st.error("⚠️ **System Error:** Data Engine Offline. Please verify dataset integrity.")
    st.stop()

# --- Sidebar ---
st.sidebar.markdown("<h2 style='text-align: center; color: #00d2ff;'>EDA Controls</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")
analysis_type = st.sidebar.radio(
    "Analytical Dimension",
    ["Feature Distribution", "Bivariate Relationship", "Correlation Intelligence"]
)

# --- Main Section ---
st.markdown('<div class="form-container">', unsafe_allow_html=True)

if analysis_type == "Feature Distribution":
    st.subheader("Feature Distribution Analysis")
    feature = st.selectbox("Select Target Dimension", df.columns)

    img_base64 = cached_univariate_plot(df, feature)
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; margin-top: 2rem;">
            <img src="data:image/png;base64,{img_base64}" 
                 alt="Distribution of {feature}" style="max-width: 100%; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,210,255,0.2);">
        </div>
        """,
        unsafe_allow_html=True
    )

elif analysis_type == "Bivariate Relationship":
    st.subheader("Bivariate Cross-Analysis")
    col1, col2 = st.columns(2)
    with col1:
        x_feature = st.selectbox("X-axis Dimension", df.columns, index=0)
    with col2:
        y_feature = st.selectbox("Y-axis Dimension", df.columns, index=1)

    img_base64 = cached_bivariate_plot(df, x_feature, y_feature)
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; margin-top: 2rem;">
            <img src="data:image/png;base64,{img_base64}" 
                 alt="{x_feature} vs {y_feature}" style="max-width: 100%; border-radius: 12px; box-shadow: 0 4px 20px rgba(146,254,157,0.2);">
        </div>
        """,
        unsafe_allow_html=True
    )

elif analysis_type == "Correlation Intelligence":
    st.subheader("Multi-Feature Correlation Matrix")

    img_base64 = cached_heatmap(df)
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; margin-top: 2rem;">
            <img src="data:image/png;base64,{img_base64}" 
                 alt="Correlation Heatmap" style="max-width: 100%; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,210,255,0.1);">
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown('</div>', unsafe_allow_html=True)

