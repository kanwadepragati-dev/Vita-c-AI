import os
import streamlit as st
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_groq import ChatGroq

# 1. Page Config
st.set_page_config(page_title="Vita-c AI", page_icon="🍊", layout="wide")

# 2. Styling (Professional UI)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { background-color: #FF4B4B; color: white; border-radius: 8px; font-weight: bold; width: 100%; }
    .stTextInput>div>div>input { border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.title("🍊 Vita-c AI")
    st.subheader("Your Research Partner")
    st.info("Powered by Groq Llama 3.3 & Tavily")
    st.write("---")
    st.write("🚀 **Project Status:** Live & Secure")
    st.write("👤 **Developed by:** Pragati Kanwade")
    st.write("---")
    st.markdown("This agent performs real-time web research to give you accurate insights.")

# 4. Main Page Header
st.title("🍊 Vita-c: Autonomous Research Agent")
st.markdown("### Search any topic and get a detailed AI report instantly.")

# 5. Logic Section (Key loading)
load_dotenv()
# Online deployment ke liye secrets use honge, local ke liye .env
tavily_key = os.getenv("TAVILY_API_KEY")
groq_key = os.getenv("GROQ_API_KEY")

if not tavily_key or not groq_key:
    st.error("API Keys missing! Please check Streamlit Secrets or .env file.")
else:
    os.environ["TAVILY_API_KEY"] = tavily_key
    search_tool = TavilySearchResults(k=5)
    
    # Updated Model: llama-3.3-70b-versatile
    llm = ChatGroq(
        model="llama-3.3-70b-versatile", 
        groq_api_key=groq_key
    )

    # 6. User Input
    query = st.text_input("What would you like to research today?", placeholder="e.g. Future of AI in Healthcare 2030")

    if st.button("Start Research"):
        if query:
            with st.spinner("Searching the web and synthesizing report..."):
                try:
                    # Step 1: Web Search
                    search_results = search_tool.invoke(query)
                    context = "\n".join([r['content'] for r in search_results])
                    
                    # Step 2: AI Synthesis
                    prompt = f"Research Goal: {query}\n\nWeb Findings:\n{context}\n\nWrite a professional, detailed, and structured research report with headings and bullet points:"
                    response = llm.invoke(prompt)
                    
                    # Step 3: Display Result
                    st.success("Done!")
                    st.markdown("---")
                    st.markdown("### 📄 Research Report")
                    st.write(response.content)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a topic!")