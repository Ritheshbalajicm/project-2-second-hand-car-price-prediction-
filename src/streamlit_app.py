import streamlit as st
import pandas as pd
import os

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

# Set the cinematic background (using hero car for main page)
set_bg('src/hero_car.png')

# --- Page Configuration ---
st.set_page_config(
    page_title="CarVault | Premium Price Prediction",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
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

    /* Hyper-dark Cinematic Overlay for maximum clarity */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: radial-gradient(circle at center, rgba(15, 23, 42, 0.92), rgba(2, 6, 23, 0.98));
        backdrop-filter: blur(5px);
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

    /* Premium Solidified Cards for maximum readability */
    .content-card {
        background: rgba(30, 41, 59, 0.95); /* Near solid dark background */
        backdrop-filter: blur(20px);
        padding: 2.5rem;
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.8);
        margin-bottom: 2rem;
        transition: all 0.3s ease;
    }
    
    .content-card:hover {
        transform: translateY(-5px);
        border: 1px solid rgba(0, 210, 255, 0.3);
    }

    /* Premium Header */
    .hero-container {
        text-align: center;
        padding: 4rem 1rem;
        background: linear-gradient(135deg, rgba(0,210,255,0.1) 0%, rgba(146,254,157,0.1) 100%);
        border-radius: 32px;
        margin-bottom: 3rem;
        border: 1px solid var(--glass-border);
    }

    .hero-container h1 {
        font-size: 4.5rem !important;
        font-weight: 900 !important;
        background: linear-gradient(to right, #00d2ff, #92fe9d);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1.5rem !important;
        letter-spacing: -1px;
        text-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }

    .hero-container p {
        font-size: 1.4rem;
        color: #ffffff !important;
        font-weight: 500 !important;
        max-width: 850px;
        margin: 0 auto;
        text-shadow: 0 2px 4px rgba(0,0,0,0.8);
    }

    /* Technology Tags */
    .tech-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 1rem;
        margin-top: 2rem;
    }

    /* Opaque Tech Items */
    .tech-item {
        background: rgba(15, 23, 42, 0.8);
        padding: 1rem;
        border-radius: 16px;
        text-align: center;
        border: 1px solid var(--glass-border);
        transition: all 0.3s ease;
    }

    .tech-item:hover {
        background: rgba(0, 210, 255, 0.1);
        border-color: var(--primary);
        box-shadow: var(--text-glow);
    }

    /* Animated Metrics */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 20px !important;
        padding: 1.5rem !important;
    }

    div[data-testid="stMetric"] label {
        color: #94a3b8 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    div[data-testid="stMetricValue"] {
        color: #00d2ff !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
    }

    /* Hide specific default elements but preserve sidebar toggle */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Ensure Sidebar Toggle is always visible and premium */
    button[kind="header"] {
        color: #00d2ff !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 50% !important;
    }

    /* General Typography enhancements */
    h1, h2, h3 {
        color: var(--primary) !important;
        text-shadow: 0 4px 10px rgba(0,0,0,0.6) !important;
    }

    p, li, span, label {
        color: #ffffff !important;
        line-height: 1.6;
        font-weight: 500 !important;
        text-shadow: 0 2px 5px rgba(0,0,0,0.8) !important;
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

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: var(--bg-dark); }
    ::-webkit-scrollbar-thumb { background: #334155; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #475569; }

</style>
""", unsafe_allow_html=True)

# --- Load Data ---
@st.cache_data
def load_data(data_path):
    try:
        return pd.read_csv(data_path)
    except Exception:
        return None

df = load_data("src/cars24_cleaned.csv")

# --- Hero Section ---
st.markdown("""
<div class="hero-container">
    <h1>CarVault Intelligence</h1>
    <p>Harnessing the power of Advanced Machine Learning to bring institutional-grade transparency to the used car marketplace.</p>
</div>
""", unsafe_allow_html=True)

# --- Layout ---
col_main, col_side = st.columns([2, 1])

with col_main:
    # --- Objective ---
    st.markdown("""
    <div class="content-card">
        <h2 style='color: #00d2ff; margin-bottom: 1.5rem;'>🎯 Executive Summary</h2>
        <p style='font-size: 1.1rem; line-height: 1.7; color: #cbd5e1;'>
            In an industry plagued by <b>price ambiguity</b>, CarVault stands as a beacon of data-driven truth. 
            By processing thousands of vehicle listings, our Neural-Engine identifies the intrinsic value 
            of any car based on its unique DNA—heritage, usage, and physiological state.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --- Project Workflow ---
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("<h2 style='color: #00d2ff; margin-bottom: 1.5rem;'>⚙️ Architectural Workflow</h2>", unsafe_allow_html=True)
    
    # Workflow Image with high-end styling
    st.image("src/workflow.png", use_container_width=True)
    
    st.markdown("""
    <div style='margin-top: 2rem;'>
        <div style='display: flex; align-items: flex-start; margin-bottom: 1rem;'>
            <div style='background: #00d2ff; color: #000; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 1rem; flex-shrink: 0;'>1</div>
            <p><b>Data Ingestion:</b> High-velocity sourcing and rigorous purification of raw automotive datasets.</p>
        </div>
        <div style='display: flex; align-items: flex-start; margin-bottom: 1rem;'>
            <div style='background: #00d2ff; color: #000; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 1rem; flex-shrink: 0;'>2</div>
            <p><b>Feature Synthesis:</b> Engineering abstract relationships between car age, mileage, and depreciation curves.</p>
        </div>
        <div style='display: flex; align-items: flex-start; margin-bottom: 1rem;'>
            <div style='background: #00d2ff; color: #000; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 1rem; flex-shrink: 0;'>3</div>
            <p><b>Neural Training:</b> Deployment of Random Forest Regressors optimized for minimal RMSE variance.</p>
        </div>
        <div style='display: flex; align-items: flex-start;'>
            <div style='background: #00d2ff; color: #000; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 1rem; flex-shrink: 0;'>4</div>
            <p><b>Explainable AI:</b> Integrating SHAP-engine to deconstruct every prediction into visual influence factors.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_side:
    # --- Tech Stack ---
    st.markdown("""
    <div class="content-card">
        <h3 style='color: #00d2ff; font-size: 1.2rem;'>🛠️ Tech Ecosystem</h3>
        <div class="tech-grid">
            <div class="tech-item">🐍 Python</div>
            <div class="tech-item">🤖 Scikit-Learn</div>
            <div class="tech-item">📊 Pandas</div>
            <div class="tech-item">🚀 Streamlit</div>
            <div class="tech-item">🧠 SHAP</div>
            <div class="tech-item">✨ CSS3</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Dataset Analytics ---
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='color: #00d2ff; font-size: 1.2rem;'>💾 Core Dataset</h3>", unsafe_allow_html=True)
    if df is not None:
        st.metric("Analyzed Assets", f"{len(df):,}")
        st.metric("Global Brands", df["Brand"].nunique())
    else:
        st.error("Data Engine Offline")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- About Me ---
    st.markdown(f"""
    <div class="content-card">
        <h3 style='color: #00d2ff; font-size: 1.2rem;'>👨‍💻 Architect</h3>
        <p style='color: #94a3b8; font-size: 0.9rem; line-height: 1.6;'>
            <b>Rithesh Balaji CM</b><br>
            Specializing in End-to-End Data Products & AI Solutions.
        </p>
        <div style='display: flex; flex-direction: column; gap: 0.5rem; margin-top: 1rem;'>
            <a href="https://linkedin.com/in/ritheshbalajicm" style='color: #00d2ff; text-decoration: none;'>🔗 LinkedIn</a>
            <a href="https://github.com/ritheshbalajicm" style='color: #00d2ff; text-decoration: none;'>🐙 GitHub</a>
            <a href="https://rithesh-portfolio.netlify.app/" style='color: #00d2ff; text-decoration: none;'>🌐 Portfolio</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.markdown("<h2 style='text-align: center; color: #00d2ff;'>CarVault Control</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.info("Navigate between the core modules using the menu above.")


