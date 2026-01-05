import streamlit as st
import pickle
import pandas as pd
import numpy as np
import shap
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
set_bg('src/bg_prediction_v2.png')

# --- Page Config ---
st.set_page_config(
    page_title="CarVault | Neural Prediction",
    page_icon="🚀",
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

    /* Hide specific default elements but preserve sidebar toggle */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Ensure Sidebar Toggle is always visible and premium */
    button[kind="header"] {
        color: #00d2ff !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 50% !important;
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

    /* Solidified Containers for maximum clarity */
    .form-container {
        background: rgba(30, 41, 59, 0.96); /* Almost opaque */
        backdrop-filter: blur(20px);
        padding: 3rem;
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.9);
        margin-bottom: 2rem;
    }

    h1, h2, h3 {
        color: var(--primary) !important;
        font-weight: 700 !important;
        text-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }
    /* High-contrast labels within grids */
    .stSelectbox label, .stNumberInput label {
        color: var(--primary) !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem !important;
        display: block;
        text-shadow: 0 4px 10px rgba(0,0,0,0.8);
    }

    /* Opaque Input Widgets */
    section[data-testid="stWidgetLabel"] p {
        color: #00d2ff !important;
        font-weight: 800 !important;
    }

    /* Ensure tables/dataframes are solid */
    div.stDataFrame, div.stTable {
        background: #1e293b !important;
        border-radius: 12px !important;
        padding: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    p, li, span, label {
        color: #ffffff !important;
        font-weight: 500 !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.6);
    }

    /* Input Widgets */
    div[data-baseweb="select"] > div, 
    input[type="number"] {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 12px !important;
        color: white !important;
        height: 3rem !important;
    }

    label {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
    }

    /* Premium Predict Button */
    div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(90deg, #00d2ff, #3a7bd5) !important;
        color: #fff !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        border-radius: 14px !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0, 210, 255, 0.3) !important;
    }
    
    div[data-testid="stFormSubmitButton"] > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 210, 255, 0.5) !important;
    }

    /* Explanation Box */
    .explain-box {
        background: rgba(0, 210, 255, 0.05);
        border: 1px solid rgba(0, 210, 255, 0.2);
        padding: 1.5rem;
        border-radius: 16px;
        margin-top: 2rem;
    }

</style>
""", unsafe_allow_html=True)


# --- Caching and Resource Loading ---
@st.cache_resource
def load_model_and_explainer(model_path):
    try:
        with open(model_path, 'rb') as file:
            pipeline = pickle.load(file)
        
        preprocessor = pipeline.named_steps['preprocessor']
        model = pipeline.named_steps['regressor']
        explainer = shap.TreeExplainer(model)
        
        return pipeline, preprocessor, explainer
    except Exception:
        return None, None, None

@st.cache_data
def load_data(data_path):
    try:
        return pd.read_csv(data_path)
    except Exception:
        return None

# Load resources
pipeline, preprocessor, explainer = load_model_and_explainer('src/car_price_predictor.pkl')
df = load_data('src/cars24_cleaned.csv')

# --- App UI ---
st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>🚀 Neural Engine Predictor</h1>", unsafe_allow_html=True)

if pipeline is None or df is None:
    st.error("⚠️ **System Error:** Neural Core Offline. Please verify model and dataset integrity.")
    st.stop()

# --- Prediction Interface ---
st.markdown('<div class="form-container" style="background: rgba(15, 23, 42, 0.98); border: 2px solid rgba(0, 210, 255, 0.3);">', unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #00d2ff; font-size: 2.5rem; margin-bottom: 2rem;'>📝 Asset Specification Portal</h2>", unsafe_allow_html=True)

# Grid Layout for Inputs
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div style="background: rgba(0,0,0,0.3); padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 1.5rem;">', unsafe_allow_html=True)
    brand = st.selectbox("🏎️ Asset Brand", sorted(df['Brand'].dropna().unique()))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div style="background: rgba(0,0,0,0.3); padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 1.5rem;">', unsafe_allow_html=True)
    model = st.selectbox("📂 Model Series", sorted(df[df['Brand'] == brand]['Model_Only'].unique()))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div style="background: rgba(0,0,0,0.3); padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 1.5rem;">', unsafe_allow_html=True)
    transmission = st.selectbox("⚙️ Transmission Module", sorted(df['Transmission Type'].unique()))
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div style="background: rgba(0,0,0,0.3); padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 1.5rem;">', unsafe_allow_html=True)
    fuel = st.selectbox("🔋 Energy Source", sorted(df['Fuel Type'].unique()))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div style="background: rgba(0,0,0,0.3); padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 1.5rem;">', unsafe_allow_html=True)
    year = st.number_input("📅 Vintage (Year)", min_value=2010, max_value=2024, value=2018)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div style="background: rgba(0,0,0,0.3); padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 1.5rem;">', unsafe_allow_html=True)
    km = st.number_input("🛣️ Total Usage (KM)", min_value=100, max_value=500000, value=50000, step=1000)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="background: rgba(0,0,0,0.3); padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 2rem;">', unsafe_allow_html=True)
owner = st.selectbox("👤 Ownership Heritage", sorted(df['Ownership'].unique()))
st.markdown('</div>', unsafe_allow_html=True)

submitted = st.button("🚀 Execute Prediction Analysis", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)


# --- Prediction Output ---
if submitted:
    current_year = 2025 
    car_age = current_year - year
    
    input_data = pd.DataFrame({
        'KM Driven': [km],
        'Fuel Type': [fuel],
        'Transmission Type': [transmission],
        'Ownership': [owner],
        'Brand': [brand],
        'Model_Only': [model],
        'Car Age': [car_age]
    })
    
    predicted_price = pipeline.predict(input_data)[0]
    
    st.markdown("""
        <div style='text-align: center; margin-top: 3rem;'>
            <h2 style='color: #94a3b8; font-size: 1.5rem; letter-spacing: 2px;'>VALUATION ESTIMATE</h2>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, rgba(0,210,255,0.2) 0%, rgba(146,254,157,0.2) 100%);
                    padding: 3rem; border-radius: 24px; border: 1px solid var(--primary);
                    text-align: center; margin-top: 1rem; box-shadow: 0 0 30px rgba(0,210,255,0.2);">
            <p style="font-size: 4rem; font-weight: 900; color: white; margin: 0; text-shadow: 0 0 20px rgba(0,210,255,0.5);">
                ₹ {predicted_price:.2f} <span style='font-size: 1.5rem; color: #94a3b8;'>Lakhs</span>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- SHAP Interpretation ---
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown("<h2 style='margin-top: 0rem;'>🧠 Neural Interpretability (SHAP)</h2>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="explain-box" style="margin-top: 1rem;">
            <p style="color: #cbd5e1; font-size: 1.1rem; line-height: 1.6; margin: 0;">
                The <b>CarVault Neural Engine</b> deconstructs the valuation into atomic influence factors. 
                <span style="color: #ff4b4b; font-weight: bold;">Red vectors</span> indicate features increasing the value, 
                while <span style="color: #00d2ff; font-weight: bold;">Blue vectors</span> represent depreciation pressures.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # SHAP Logic
    input_transformed = preprocessor.transform(input_data)
    if hasattr(input_transformed, "toarray"):
        input_transformed = input_transformed.toarray()
    input_transformed = input_transformed.astype(float)

    try:
        feature_names = preprocessor.get_feature_names_out()
    except Exception:
        num_features = list(preprocessor.named_transformers_['num'].feature_names_in_)
        ohe_transformer = preprocessor.named_transformers_['cat']
        cat_features_original = list(ohe_transformer.feature_names_in_)
        cat_features_generated = []
        for i, categories in enumerate(ohe_transformer.categories_):
            original_feature_name = cat_features_original[i]
            for category in categories:
                cat_features_generated.append(f"{original_feature_name}_{category}")
        feature_names = num_features + cat_features_generated
    
    shap_values = explainer.shap_values(input_transformed)
    input_transformed_df = pd.DataFrame(input_transformed, columns=feature_names)

    force_plot = shap.force_plot(
        explainer.expected_value,
        shap_values[0, :],
        input_transformed_df.iloc[0],
        matplotlib=False,
        text_rotation=0,
        plot_cmap=["#00d2ff", "#ff4b4b"]
    )
    
    shap_html = f"<div style='background: white; border-radius: 12px; padding: 20px; margin-top: 2rem;'>{shap.getjs()}{force_plot.html()}</div>"
    st.components.v1.html(shap_html, height=200, scrolling=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


