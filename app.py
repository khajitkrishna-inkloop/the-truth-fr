import streamlit as st
import google.generativeai as genai
from tavily import TavilyClient
import plotly.express as px
import pandas as pd

# --- THEME & GLASSMORPHISM UI ---
st.set_page_config(page_title="The Truth fr | Khajit Krishna", layout="wide")

st.markdown("""
    <style>
    /* Global Space Background */
    .stApp {
        background: radial-gradient(circle at top, #1a1a3a, #0a0a12);
        color: #ffffff;
    }
    
    /* Glowing Khajit Header */
    .khajit-ultra-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 50px;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(to right, #bc13fe, #00f2ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 0px 20px rgba(188, 19, 254, 0.6);
        padding: 20px;
        border-bottom: 2px solid rgba(188, 19, 254, 0.3);
        margin-bottom: 40px;
    }

    /* Modern Glass Cards */
    div[data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(188, 19, 254, 0.2);
        margin-bottom: 20px;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(10, 10, 20, 0.95) !important;
        border-right: 2px solid #bc13fe;
    }

    /* High Contrast Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #bc13fe, #7a00ff);
        color: white !important;
        font-weight: bold;
        border: none;
        border-radius: 10px;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        box-shadow: 0px 0px 15px #bc13fe;
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# --- PERSISTENT BRANDING ---
st.markdown('<div class="khajit-ultra-header">KHAJIT KRISHNA</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🛰️ THE TRUTH FR")
    st.write("---")
    menu = st.radio("DASHBOARD", ["Home", "History", "Science", "Health", "Viral Scourge"])
    st.write("---")
    st.caption("v2.0.26 Optimized")

# --- CORE LOGIC ---
if menu == "Home":
    st.title("⚖️ Fact Check Terminal")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        claim = st.text_area("PASTE CLAIM OR LINK:", placeholder="Enter a viral claim to verify...")
    
    with col2:
        # Check for keys in secrets
        try:
            gem_key = st.secrets["GEMINI_API_KEY"]
            tav_key = st.secrets["TAVILY_API_KEY"]
            st.success("✅ Systems Online")
        except:
            st.error("❌ Keys missing in Streamlit Secrets")

    if st.button("RUN FACT-CHECK"):
        # Sensitive Topic Filter
        if any(x in claim.lower() for x in ["religion", "god", "faith", "belief"]):
            st.warning("⚠️ Topic Flagged: Subjective beliefs/religions are not fact-checked by this system.")
        elif claim:
            with st.spinner("AI Scourge in Progress..."):
                try:
                    # 1. Search
                    tavily = TavilyClient(api_key=tav_key)
                    search = tavily.search(query=claim, search_depth="advanced")
                    
                    # 2. AI using the NEW 2026 Model Name
                    genai.configure(api_key=gem_key)
                    model = genai.GenerativeModel('gemini-2.0-flash') # UPDATED MODEL
                    
                    context = "\n".join([f"Source: {r['url']}\nContent: {r['content']}" for r in search['results']])
                    prompt = f"Claim: {claim}\nSources: {context}\nGive verdict (True/False/Mixed), 'for real' explanation, and a confidence score."
                    
                    response = model.generate_content(prompt)
                    
                    # 3. Display
                    st.markdown("### 📊 Analysis Result")
                    res_col1, res_col2 = st.columns([1, 1])
                    
                    with res_col1:
                        st.write(response.text)
                    
                    with res_col2:
                        fig = px.pie(values=[80, 20], names=['Truth', 'Unverified'], hole=0.5,
                                    color_discrete_sequence=['#00f2ff', '#bc13fe'])
                        fig.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
                        st.plotly_chart(fig)

                    st.markdown("### 🔗 Sources Scoured")
                    for r in search['results']:
                        st.markdown(f"⭐ [{r['title']}]({r['url']})")
                        
                except Exception as e:
                    st.error(f"System Error: {e}")
        else:
            st.info("Input a claim above to begin.")

else:
    st.markdown(f"## {menu} Module")
    st.info("Module currently under encryption by Khajit Krishna.")
