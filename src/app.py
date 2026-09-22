import os
import sys
import streamlit as st

# Force Python to register the framework variable automatically
os.environ["NEMOGUARDRAILS_LLM_FRAMEWORK"] = "langchain"

# Forces Python to look at your root project folder for 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.inference_engine import GeminiClinicalRAGEngine

# --- LAYOUT CONFIGURATION ---
st.set_page_config(
    page_title="Secure Clinical Insights Engine",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INJECT CLINICAL CSS STYLESHEET WITH VISIBILITY FIX ---
# CRITICAL FIX: Explicitly forced all chat bubbles and inner typography to utilize high-contrast dark text
st.markdown("""
    <style>
        .main-header { font-size: 2.2rem; color: #0f4c81; font-weight: 700; margin-bottom: 5px; }
        .sub-header { font-size: 1.1rem; color: #5a6b7c; margin-bottom: 25px; }
        .system-pill { background-color: #e8f4fd; border-left: 5px solid #1aa1f5; padding: 10px; border-radius: 4px; margin-bottom: 15px; }
        
        .chat-bubble-user { 
            background-color: #f4f6f8; 
            color: #1e293b !important; 
            padding: 12px 16px; 
            border-radius: 8px; 
            margin-bottom: 10px; 
            font-weight: 500;
        }
        
        .chat-bubble-ai { 
            background-color: #ffffff; 
            color: #1e293b !important; 
            border: 1px solid #e1e4e8; 
            padding: 12px 16px; 
            border-radius: 8px; 
            margin-bottom: 10px; 
        }
        
        .guardrail-block { 
            background-color: #fdf2f2; 
            border-left: 5px solid #f04444; 
            padding: 15px; 
            border-radius: 4px; 
            color: #b91c1c !important; 
            font-weight: 500;
        }
        
        /* Force text colors inside bubble containers */
        .chat-bubble-user *, .chat-bubble-ai *, .guardrail-block * {
            color: inherit !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- ENGINE STATE INITIALIZATION ---
@st.cache_resource
def load_rag_core():
    """Caches the heavy ML models/engines so they do not reload on every button click"""
    return GeminiClinicalRAGEngine()

try:
    engine = load_rag_core()
except Exception as e:
    st.error(f"Initialization Error: Ensure your .env variables and AWS Security Groups are active. Details: {e}")
    st.stop()

# --- APP LAYOUT STRUCTURE ---
st.markdown("<div class='main-header'>🔒 Secure Clinical Insights Engine</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Enterprise-Grade Zero-Trust Clinical Retrieval-Augmented Generation Dashboard</div>", unsafe_allow_html=True)

st.divider()

# --- SIDEBAR CONTROL CENTER ---
with st.sidebar:
    st.header("⚙️ Control Panel")
    
    available_patients = ["10003400", "10002495", "10002930", "10000032", "10004720"]
    
    selected_patient_id = st.selectbox(
        "Select Active Patient ID Record:",
        options=available_patients,
        index=0
    )
    
    st.markdown("---")
    st.markdown("### 🛡️ Active Security Modules")
    st.success("✔ Microsoft Presidio (PHI Anonymizer)")
    st.success("✔ NVIDIA NeMo Guardrails (Safety Mesh)")
    st.success("✔ AWS pgvector Hybrid Cloud Matcher")
    st.info("🤖 Model: `gemini-3.6-flash`")
    
    if st.button("Clear Chat Memory"):
        st.session_state.chat_history = []
        st.session_state.click_prompt = None
        st.rerun()

# --- CHAT STATE TRACKING MATRIX ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "click_prompt" not in st.session_state:
    st.session_state.click_prompt = None

# --- SUGGESTED TESTING QUESTIONS COMPONENT ---
st.markdown("### 📋 Quick-Test Clinical Scenarios")
st.caption("Click any query below to run it automatically against the active patient record:")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**🟢 Compliant Data Extractions (Allowed)**")
    if st.button("🔍 What was the patient's last recorded dosage details?", key="q1", use_container_width=True):
        st.session_state.click_prompt = "What was the patient's last recorded dosage details?"
    if st.button("📋 Summarize this patient's admission notes and logged test names", key="q2", use_container_width=True):
        st.session_state.click_prompt = "Summarize this patient's admission notes and logged test names"

with col2:
    st.markdown("**🛑 Non-Compliant Prescribing Advice (Blocked)**")
    if st.button("🚨 Based on the fluid retention, should I prescribe a higher dose of Furosemide?", key="q3", use_container_width=True):
        st.session_state.click_prompt = "Based on the fluid retention, should I prescribe a higher dose of Furosemide?"
    if st.button("💊 Can you recommend a new medication adjustment for this diagnosis?", key="q4", use_container_width=True):
        st.session_state.click_prompt = "Can you recommend a new medication adjustment for this diagnosis?"

st.markdown("---")

# --- RENDER CHAT INTERFACE HISTORY ---
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f"<div class='chat-bubble-user'>🧑‍⚕️ <b>Clinician:</b> {message['content']}</div>", unsafe_allow_html=True)
    else:
        if "[Guardrail Intercepted Action]" in message["content"] or "I cannot provide" in message["content"]:
            st.markdown(f"<div class='guardrail-block'>🛡️ {message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-bubble-ai'>🤖 <b>Engine Output:</b><br>{message['content']}</div>", unsafe_allow_html=True)

# --- USER PROMPT ENTRY LAYOUT ---
with st.container():
    user_query = st.chat_input("Enter secure natural language clinical lookup query or diagnostic fact check...")
    
    active_prompt = None
    if st.session_state.click_prompt:
        active_prompt = st.session_state.click_prompt
        st.session_state.click_prompt = None
    elif user_query:
        active_prompt = user_query

    if active_prompt:
        st.markdown(f"<div class='chat-bubble-user'>🧑‍⚕️ <b>Clinician:</b> {active_prompt}</div>", unsafe_allow_html=True)
        st.session_state.chat_history.append({"role": "user", "content": active_prompt})
        
        with st.spinner("Executing Zero-Trust Database Query & Compliance Audit..."):
            raw_response = engine.generate_clinical_insight(
                patient_id=selected_patient_id, 
                user_question=active_prompt
            )
        
        if "[Guardrail Intercepted Action]" in raw_response:
            st.markdown(f"<div class='guardrail-block'>🛡️ {raw_response}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-bubble-ai'>🤖 <b>Engine Output:</b><br>{raw_response}</div>", unsafe_allow_html=True)
            
        st.session_state.chat_history.append({"role": "assistant", "content": raw_response})
        st.rerun()
