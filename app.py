import streamlit as st
import google.generativeai as genai
from tavily import TavilyClient
import plotly.express as px
import pandas as pd

# --- THEME ENGINE: GLASS-MORPHISM 2026 ---
st.set_page_config(page_title="The Truth fr", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Inter:wght@300;600&display=swap');

    /* Background: Deep Obsidian Space */
    .stApp {
        background: radial-gradient(circle at top right, #1a0033, #050505 60%);
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }

    /* Website Header: Main Focus */
    .website-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 72px;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(180deg, #FFFFFF 0%, #bc13fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 20px;
        letter-spacing: -2px;
        filter: drop-shadow(0 0 20px rgba(188, 19, 254, 0.4));
    }

    /* Sub-Branding: Khajit Krishna Signature */
    .developer-tag {
        text-align: center;
        font-family: 'Orbitron', sans-serif;
        font-size: 14px;
        color: #00f2ff;
        letter-spacing: 4px;
        margin-bottom: 40px;
        opacity: 0.8;
    }

    /* Glass Container */
    .glass-panel {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 35px;
        padding: 60px;
        margin: auto;
        max-width: 1000px;
        box-shadow: 0 40px 100px rgba(0, 0, 0, 0.6);
    }

    /* Neon UI Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #bc13fe, #7a00ff) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 20px !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: bold !important;
        text-transform: uppercase;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        box-shadow: 0 0 30px #bc13fe;
        transform: translateY(-3px);
    }

    /* Input Field Overhaul */
    .stTextArea textarea {
        background: rgba(0, 0, 0, 0.4) !important;
        color: #fff !important;
        border: 2px solid rgba(188, 19, 254, 0.3) !important;
        border-radius: 20px !important;
        font-size: 18px !important;
    }
    </style>

    <div class="website-title">THE TRUTH FR</div>
    <div class="developer-tag">SYSTEM ARCHITECT: KHAJIT KRISHNA</div>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h2 style='color:#bc13fe; font-family:Orbitron;'>NAVCOM</h2>", unsafe_allow_html=True)
    mode = st.radio("SELECT MODE", ["REAL-TIME VERIFY", "VIRAL SCOURGE", "ARCHIVES"])
    st.write("---")
    st.markdown(f"<p style='color:grey; font-size:12px;'>KHAJIT KRISHNA OS v4.0</p>", unsafe_allow_html=True)

# --- LOGIC & EXECUTION ---
if mode == "REAL-TIME VERIFY":
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    
    user_query = st.text_area("PASTE CLAIM OR SOURCE LINK:", height=150, placeholder="Scanning... waiting for input.")

    if st.button("EXECUTE FACT-CHECK"):
        if user_query:
            try:
                # 1. Access Credentials
                g_key = st.secrets["GEMINI_API_KEY"]
                t_key = st.secrets["TAVILY_API_KEY"]

                with st.spinner("INITIATING SCAN..."):
                    # 2. Web & Social Search
                    tavily = TavilyClient(api_key=t_key)
                    results = tavily.search(query=user_query, search_depth="advanced")
                    
                    # 3. AI Analysis
                    genai.configure(api_key=g_key)
                    model = genai.GenerativeModel('gemini-2.0-flash')
                    
                    context = "\n".join([f"Source: {r['url']}\nContent: {r['content']}" for r in results['results']])
                    prompt = f"Verify claim: {user_query}\nContext: {context}\nVerdict: True/False/Mixed. slang: sharp. Confidence: %."
                    
                    response = model.generate_content(prompt)

                    # 4. Results UI
                    st.markdown("### 📊 SYSTEM VERDICT")
                    c1, c2 = st.columns([3, 2])
                    
                    with c1:
                        st.write(response.text)
                    
                    with c2:
                        # Truth/Noise Meter
                        fig = px.pie(values=[88, 12], names=['TRUTH', 'NOISE'], hole=0.7,
                                    color_discrete_sequence=['#bc13fe', '#00f2ff'])
                        fig.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
                        st.plotly_chart(fig, use_container_width=True)

                    st.markdown("### 🔍 SCANNED SOURCES")
                    for r in results['results']:
                        st.markdown(f"🔹 [{r['title']}]({r['url']})")

            except Exception as e:
                if "429" in str(e):
                    st.error("🚨 QUOTA DEPLETED: Google AI has paused your free tier. Check your usage at ai.google.dev or wait 60 seconds.")
                else:
                    st.error(f"CRITICAL ERROR: {e}")
        else:
            st.info("Awaiting Input Data.")
    st.markdown('</div>', unsafe_allow_html=True)

# Persistent Minimal Footer
st.markdown("<br><br><br><p style='text-align:center; color:rgba(255,255,255,0.2);'>Khajit Krishna • THE TRUTH FR • 2026</p>", unsafe_allow_html=True)
