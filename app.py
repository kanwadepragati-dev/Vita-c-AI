import os
import streamlit as st
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_ollama import OllamaLLM

# 1. Page Config (Browser tab par kya dikhega)
st.set_page_config(page_title="Vita-c AI", page_icon="🍊", layout="wide")

# 2. Styling (Professional look ke liye)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { background-color: #FF4B4B; color: white; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar (Aapka introduction)
with st.sidebar:
    st.title("🍊 Vita-c AI")
    st.subheader("Your Research Partner")
    st.info("Built with Llama 3 & Tavily")
    st.write("---")
    st.write("Developed by: **Pragati Kanwade**")

# 4. Main Page Header
st.title("🍊 Vita-c: Autonomous Research Agent")
st.markdown("### Search any topic and get a detailed AI report instantly.")

# 5. Logic Section (Key loading)
load_dotenv()
tavily_key = os.getenv("TAVILY_API_KEY")

if not tavily_key:
    st.error("API Key missing! Please check .env file.")
else:
    os.environ["TAVILY_API_KEY"] = tavily_key
    search_tool = TavilySearchResults(k=5)
    llm = OllamaLLM(model="llama3")

    # 6. User Input
    query = st.text_input("What would you like to research today?", placeholder="e.g. Future of AI in 2026")

    if st.button("Start Research"):
        if query:
            with st.spinner("Researching and writing report..."):
                # Research Logic
                search_results = search_tool.invoke(query)
                context = "\n".join([r['content'] for r in search_results])
                
                prompt = f"Research Goal: {query}\n\nWeb Findings:\n{context}\n\nWrite a professional report:"
                response = llm.invoke(prompt)
                
                st.success("Done!")
                st.markdown("### 📄 Research Report")
                st.write(response)
        else:
            st.warning("Please enter a topic!")