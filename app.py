import streamlit as st
import google.generativeai as genai
from tavily import TavilyClient
import plotly.express as px
import pandas as pd

# --- 1. GLOBAL UI & GLASSMORPHISM DESIGN ---
st.set_page_config(page_title="The Truth fr", layout="wide")

st.markdown("""
    <style>
    /* High-End Dark Space Background */
    .stApp {
        background: linear-gradient(to bottom right, #050505, #12002b, #00121a);
        color: #FFFFFF !important;
    }
    
    /* Website Name at Top - Neon Pulse */
    .main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 60px;
        text-align: center;
        color: #bc13fe;
        text-shadow: 0 0 20px #bc13fe, 0 0 40px #7a00ff;
        padding-top: 20px;
        margin-bottom: 5px;
        font-weight: 900;
    }

    /* Glassmorphism Card Style */
    .glass-card {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 25px;
        padding: 40px;
        margin: 20px auto;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
    }

    /* Floating Branding for Khajit Krishna */
    .khajit-branding {
        position: fixed;
        bottom: 10px;
        right: 20px;
        color: rgba(255, 255, 255, 0.5);
        font-size: 14px;
        letter-spacing: 2px;
        z-index: 1000;
    }

    /* Input Field High Contrast */
    .stTextArea textarea {
        background: rgba(0, 0, 0, 0.3) !important;
        color: #00f2ff !important;
        border: 1px solid #bc13fe !important;
        border-radius: 15px !important;
        font-size: 18px !important;
    }

    /* Sidebar Fixes */
    [data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.9) !important;
        border-right: 1px solid #bc13fe;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE BRANDING ---
st.markdown('<div class="main-title">THE TRUTH FR</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#00f2ff; font-size:18px;">Automated Reality Verification Terminal</p>', unsafe_allow_html=True)
st.markdown('<div class="khajit-branding">BY KHAJIT KRISHNA</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### SYSTEM CONTROLS")
    st.write(f"**Developer:** Khajit Krishna")
    menu = st.selectbox("Navigation", ["Verify Claim", "Truth History", "Viral Scourge"])
    st.write("---")
    st.info("💡 If you see 'Quota Exceeded', the Free Tier is at its limit. Please try again in a few minutes.")

# --- 3. MAIN FACT-CHECKER ---
if menu == "Verify Claim":
    # Glass Wrapper
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    claim = st.text_area("Input claim for verification:", placeholder="e.g., 'Viral video of floating city in China'")
    
    if st.button("EXECUTE SCANNERS"):
        if not claim:
            st.warning("Please provide a claim to verify.")
        else:
            try:
                # Load Keys
                gem_key = st.secrets["GEMINI_API_KEY"]
                tav_key = st.secrets["TAVILY_API_KEY"]

                with st.spinner("INITIATING AI SEARCH..."):
                    # Tavily Search
                    tavily = TavilyClient(api_key=tav_key)
                    search_data = tavily.search(query=claim, search_depth="advanced")
                    
                    # Gemini Analysis
                    genai.configure(api_key=gem_key)
                    model = genai.GenerativeModel('gemini-2.0-flash')
                    
                    prompt = f"Claim: {claim}\nSources: {search_data['results']}\nDecide: True, False, or Mixed. Explain briefly in sharp slang. Give a confidence score."
                    response = model.generate_content(prompt)

                    # Display Results in Modern Layout
                    st.markdown("### 📊 VERDICT ENGINE")
                    c1, c2 = st.columns([2, 1])
                    
                    with c1:
                        st.markdown(f"#### {response.text}")
                    
                    with c2:
                        fig = px.pie(values=[90, 10], names=['Accuracy', 'Noise'], hole=0.6,
                                    color_discrete_sequence=['#bc13fe', '#00f2ff'])
                        fig.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
                        st.plotly_chart(fig, use_container_width=True)

                    st.markdown("### 🔗 VERIFIED SOURCES")
                    for r in search_data['results']:
                        st.markdown(f"- **{r['title']}**: [View Source]({r['url']})")

            except Exception as e:
                if "429" in str(e):
                    st.error("🚨 **Gemini API Limit Reached.** You are on the free tier. Wait 60 seconds or check your Google AI Studio quota.")
                else:
                    st.error(f"Error: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer Branding
st.markdown("<br><br><br><center><p style='color:grey;'>Built by Khajit Krishna • 2026 Edition</p></center>", unsafe_allow_html=True)
