import streamlit as st
import google.generativeai as genai
from tavily import TavilyClient
import plotly.express as px
import pandas as pd

# --- 1. THE EXACT UI CLONE ENGINE ---
st.set_page_config(page_title="The Truth fr", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Inter:wght@300;400;700&display=swap');

    /* Background Setup */
    .stApp {
        background: radial-gradient(circle at 50% -20%, #2a0052, #050505);
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }

    /* Main Website Title */
    .main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: clamp(40px, 8vw, 80px);
        font-weight: 900;
        text-align: center;
        background: linear-gradient(180deg, #ffffff 0%, #bc13fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(188, 19, 254, 0.5);
        letter-spacing: -2px;
        margin-top: 50px;
    }

    /* Glassmorphism Card Wrapper */
    .glass-container {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 30px;
        padding: 50px;
        margin: 40px auto;
        max-width: 900px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    }

    /* Floating Dev Tag (Khajit Krishna) */
    .dev-badge {
        position: fixed;
        bottom: 20px;
        right: 30px;
        background: rgba(188, 19, 254, 0.15);
        border: 1px solid rgba(188, 19, 254, 0.3);
        padding: 8px 15px;
        border-radius: 50px;
        color: #bc13fe;
        font-family: 'Orbitron', sans-serif;
        font-size: 12px;
        letter-spacing: 1px;
        z-index: 9999;
    }

    /* Neon Button */
    .stButton>button {
        background: #bc13fe !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 15px 30px !important;
        font-family: 'Orbitron', sans-serif !important;
        transition: 0.4s ease !important;
        text-transform: uppercase;
        width: 100%;
    }
    .stButton>button:hover {
        box-shadow: 0 0 25px #bc13fe !important;
        transform: translateY(-2px);
    }

    /* Sidebar Fixes */
    [data-testid="stSidebar"] {
        background: rgba(0, 0, 0, 0.8) !important;
        border-right: 1px solid rgba(188, 19, 254, 0.2);
    }
    </style>

    <div class="main-title">THE TRUTH FR</div>
    <div class="dev-badge">DEV: KHAJIT KRISHNA</div>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR & NAVIGATION ---
with st.sidebar:
    st.markdown("<h2 style='color:#bc13fe; font-family:Orbitron;'>TERMINAL</h2>", unsafe_allow_html=True)
    menu = st.radio("SENSORS", ["FACT CHECKER", "TRENDING", "DATABASE"])
    st.write("---")
    st.caption("Khajit Krishna Identity Confirmed")

# --- 3. LOGIC ---
if menu == "FACT CHECKER":
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    
    claim = st.text_input("ENTER CLAIM FOR VERIFICATION:", placeholder="Paste link or text here...")
    
    if st.button("RUN SCANNERS"):
        if claim:
            try:
                # Key retrieval
                gem_key = st.secrets["GEMINI_API_KEY"]
                tav_key = st.secrets["TAVILY_API_KEY"]

                with st.spinner("INITIATING AI SEARCH..."):
                    tavily = TavilyClient(api_key=tav_key)
                    search = tavily.search(query=claim, search_depth="advanced")
                    
                    genai.configure(api_key=gem_key)
                    model = genai.GenerativeModel('gemini-2.0-flash')
                    
                    prompt = f"Analyze: {claim}\nSources: {search['results']}\nVerdict: True/False/Mixed. Sharp slang explanation. Confidence score."
                    response = model.generate_content(prompt)

                    # Display Grid
                    col1, col2 = st.columns([3, 2])
                    with col1:
                        st.markdown(f"### ANALYSIS\n{response.text}")
                    with col2:
                        fig = px.pie(values=[92, 8], names=['TRUTH', 'NOISE'], hole=0.7,
                                    color_discrete_sequence=['#bc13fe', '#00f2ff'])
                        fig.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
                        st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                if "429" in str(e):
                    st.error("🚨 QUOTA DEPLETED. Wait 60s or check Google AI Studio Billing.")
                else:
                    st.error(f"Error: {e}")
        else:
            st.info("Scanner awaiting input.")
    st.markdown('</div>', unsafe_allow_html=True)
