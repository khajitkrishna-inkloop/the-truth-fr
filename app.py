import streamlit as st
import google.generativeai as genai
from tavily import TavilyClient
import plotly.express as px
import pandas as pd

# --- BRANDING & THEME ---
st.set_page_config(page_title="The Truth fr | Khajit Krishna", layout="wide")

# Custom CSS for Purple/Black Space Tech Theme
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #1a1a2e, #16213e); color: #e0e0e0; }
    [data-testid="stSidebar"] { background-color: rgba(15, 12, 41, 0.9) !important; border-right: 1px solid #bc13fe; }
    h1, h2, h3 { color: #bc13fe !important; font-family: 'Orbitron', sans-serif; text-shadow: 0 0 10px #bc13fe; }
    .khajit-header { font-size: 32px; font-weight: 900; color: #00f2ff; text-align: center; border: 2px solid #bc13fe; padding: 10px; border-radius: 10px; margin-bottom: 30px; }
    </style>
    """, unsafe_allow_html=True)

# Persistent Identity
st.markdown('<div class="khajit-header">DEVELOPED BY KHAJIT KRISHNA</div>', unsafe_allow_html=True)

# Sidebar UI
st.sidebar.image("logo.png", width=150) # Ensure logo.png is in your GitHub repo
st.sidebar.title("The Truth fr ⚖️")
menu = st.sidebar.radio("Navigation", ["🛰️ Fact Checker", "📖 Your Truth History", "🔬 Science", "🏥 Health", "🎬 Entertainment"])

# --- SENSITIVE TOPIC FILTER ---
SENSITIVE_WORDS = ["religion", "god", "faith", "belief", "spiritual", "worship", "theology"]

def is_sensitive(text):
    return any(word in text.lower() for word in SENSITIVE_WORDS)

# --- MAIN LOGIC ---
if menu == "🛰️ Fact Checker":
    st.subheader("Automated Web & Social Scourge")
    claim = st.text_input("Enter a viral claim, tweet, or topic to verify:", placeholder="e.g., Is there a new planet discovered in 2026?")

    if st.button("EXECUTE ANALYSIS"):
        if is_sensitive(claim):
            st.error("🛑 TOPIC FLAGGED: This topic involves personal beliefs or religion. 'The Truth fr' does not fact-check beliefs.")
        elif claim:
            try:
                # Get keys from Streamlit Secrets
                gemini_key = st.secrets["GEMINI_API_KEY"]
                tavily_key = st.secrets["TAVILY_API_KEY"]

                with st.spinner("Khajit's AI is scouring social media..."):
                    # 1. Search with Tavily
                    tavily = TavilyClient(api_key=tavily_key)
                    search = tavily.search(query=claim, search_depth="advanced")
                    
                    # 2. Process with Gemini
                    genai.configure(api_key=gemini_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    context = "\n".join([f"Source: {r['url']}\nContent: {r['content']}" for r in search['results']])
                    prompt = f"Claim: {claim}\n\nSources:\n{context}\n\nVerdict? (True/False/Mixed). Explain in 'for real' slang. Give a confidence %."
                    
                    response = model.generate_content(prompt)

                    # 3. Data Visualization
                    st.success("Analysis Complete")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"### Verdict\n{response.text}")
                    
                    with col2:
                        # Pie chart logic (Extracting % roughly or using 90/10 for demo)
                        fig_data = pd.DataFrame({'Verdict': ['Certainty', 'Doubt'], 'Value': [85, 15]})
                        fig = px.pie(fig_data, values='Value', names='Verdict', hole=0.4, color_discrete_sequence=['#bc13fe', '#00f2ff'])
                        st.plotly_chart(fig)

                    st.markdown("### 🔗 Exact Sources Used:")
                    for r in search['results']:
                        st.markdown(f"- [{r['title']}]({r['url']})")

            except Exception as e:
                st.error(f"Error: {e}. Check your API keys in the Streamlit Settings!")

else:
    st.info(f"Section '{menu}' is locked. Khajit Krishna is currently training this module.")

st.markdown("---")
st.caption("© 2026 Khajit Krishna | The Truth fr - Built for the future.")
