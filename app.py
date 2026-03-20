import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_community.tools.tavily_search import TavilySearchResults
import os

# Configuration
os.environ["TAVILY_API_KEY"] = "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"
search_tool = TavilySearchResults(k=5)
llm = OllamaLLM(model="llama3")

# --- UI ENHANCEMENTS (The Vita-c Theme) ---
st.set_page_config(page_title="Vita-c AI", page_icon="🍊", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
        background-color: #0a0a0b;
        color: #e2e8f0;
    }
    .stButton>button {
        background: linear-gradient(90deg, #f97316 0%, #ea580c 100%);
        color: white; border-radius: 12px; border: none;
        padding: 12px 28px; font-weight: 700; width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        box-shadow: 0 0 20px rgba(249, 115, 22, 0.4);
        transform: translateY(-2px);
    }
    .main-title {
        font-size: 3.5rem; font-weight: 900; text-align: center;
        margin-bottom: 0; background: -webkit-linear-gradient(#fff, #94a3b8);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("<h1 style='color: #f97316;'>🍊 Vita-c</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.status("Agent Status: Online", state="complete")
    st.write("📍 **Engine:** Llama 3.1")
    st.write("🌐 **Search:** Live Enabled")

# Main Interface
st.markdown("<h1 class='main-title'>What should Vita-c research?</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b; font-size: 1.2rem;'>Advanced Research Synthesis powered by Local AI</p>", unsafe_allow_html=True)

query = st.text_input("", placeholder="e.g. Impact of AI on Healthcare 2026...", label_visibility="collapsed")

col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.button("Run Deep Analysis"):
        if query:
            with st.status("🍊 Vita-c is squeezing the web...", expanded=True) as status:
                st.write("🔍 Searching real-time sources...")
                data = search_tool.invoke({"query": query})
                st.write("🧠 Llama 3 is synthesizing insights...")
                prompt = f"System: You are Vita-c, a world-class researcher. Goal: {query}. Data: {data}. Task: Provide a high-level executive report with bullet points."
                response = llm.invoke(prompt)
                status.update(label="Analysis Complete!", state="complete")
            
            st.markdown("### 📊 Executive Report")
            st.markdown(response)
            st.download_button("📥 Download Report", response, file_name="vitac_report.md")
        else:
            st.warning("Please enter a research goal.")