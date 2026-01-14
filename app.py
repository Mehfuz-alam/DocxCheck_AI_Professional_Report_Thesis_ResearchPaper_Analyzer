# import streamlit as st
# import requests
# import os

# st.set_page_config(page_title="DocxCheck AI", layout="wide")

# # Sidebar with Logo
# with st.sidebar:
#     if os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)
#     st.markdown("<h2 style='text-align:center; color:white;'>DocxCheck AI</h2>", unsafe_allow_html=True)
#     st.markdown("---")
#     st.success("System: Online")
#     st.info("💡 **Dynamic Mode:** Rules are extracted directly from your guidelines.")

# st.title("🎓 Professional Report Analyzer")
# c1, c2 = st.columns(2)
# with c1: g_file = st.file_uploader("Upload Guidelines", type=["pdf", "docx"])
# with c2: r_file = st.file_uploader("Upload Report", type=["pdf", "docx"])

# if g_file and r_file:
#     if st.button("🚀 EXECUTE AUDIT", use_container_width=True):
#         with st.spinner("AI is reading guidelines and auditing..."):
#             files = {"guidelines": (g_file.name, g_file, g_file.type), "report": (r_file.name, r_file, r_file.type)}
#             data = requests.post("http://127.0.0.1:8000/upload_report/", files=files).json()

#             # SHOW DETECTED RULES (The Hackathon "Wow" Factor)
#             st.markdown("### 📋 Detected Institutional Requirements")
#             r = data["detected_rules"]
#             st.info(f"**Font:** {r['font_name']} | **Size:** {r['font_size']}pt | **Required Sections:** {', '.join(r['sections'])}")

#             tab1, tab2, tab3 = st.tabs(["📊 Audit", "⚡ Quick Fixes", "📥 Export"])
#             with tab1:
#                 col_a, col_b = st.columns(2)
#                 with col_a:
#                     st.subheader("Formatting")
#                     for e in data["format_errors"]: st.error(e)
#                 with col_b:
#                     st.subheader("Structure")
#                     for e in data["structure_errors"]: st.warning(e)
            
#             with tab2:
#                 st.subheader("Action Plan")
#                 st.markdown(f'<div style="background:#fff4e5; padding:20px; border-radius:10px; color:black;">{data["rag_suggestions"]}</div>', unsafe_allow_html=True)

#             with tab3:
#                 if data["highlighted_report_path"]:
#                     with open(data["highlighted_report_path"], "rb") as f:
#                         st.download_button("Download Annotated Report", f, file_name=f"Audit_{r_file.name}")

import streamlit as st
import requests
import os
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="DocxCheck AI | Professional Compliance Auditor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Google Material Design Inspired CSS ---
st.markdown("""
    <style>
    /* Global Styles */
    .stApp {
        background-color: #fdfdfd;
    }
    
    /* Sidebar Customization */
    section[data-testid="stSidebar"] {
        background-color: #1a1c1e !important;
        border-right: 1px solid #e1e3e1;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #1a1c1e;
        font-family: 'Google Sans', sans-serif;
    }

    /* Cards for Rules & Results */
    .rule-card {
        background-color: #f0f4f8;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #d1d9e0;
        margin-bottom: 20px;
    }
    
    .status-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        margin-right: 8px;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 500;
        height: 50px;
        color: #444746;
    }
    .stTabs [aria-selected="true"] {
        color: #0b57d0 !important;
        border-bottom-color: #0b57d0 !important;
    }

    /* Action Plan Box */
    .action-plan {
        background: #ffffff;
        padding: 24px;
        border-radius: 12px;
        border-left: 6px solid #fbac34;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        color: #1a1c1e;
        line-height: 1.6;
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        color: #0b57d0;
        font-weight: 700;
    }
    /* Sidebar Caption Styling */
    section[data-testid="stSidebar"] .stCaption {
        color: #ffffff !important;
        font-weight: 500;
        font-size: 0.95rem;
    }
    /* Enhanced Sidebar Contrast */
    section[data-testid="stSidebar"] .stCaption {
        color: #FFFFFF !important; /* Brighter White */
        font-weight: 600 !important;
        font-size: 1rem !important;
        opacity: 1 !important;
    }
    
    /* Highlight the Success Indicators */
    .stAlert {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    
    st.markdown("<h2 style='text-align: center; color: white;'>DocxCheck AI</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("<p style='color: #c4c7c5; font-size: 0.9rem;'>SYSTEM STATUS</p>", unsafe_allow_html=True)
    st.success("🟢 Engine: Online")
    st.success("🔵 API: Connected")
    
    st.markdown("---")
    st.markdown("<p style='color: #c4c7c5; font-size: 0.9rem;'>ACTIVE MODULES</p>", unsafe_allow_html=True)
    st.caption("✅ Dynamic RAG Extractor")
    st.caption("✅ Structural Auditor")
    st.caption("✅ Style Compliance Engine")
    
    st.markdown("---")
    st.info("💡 Rules are extracted directly from your guidelines using Gemini LLM reasoning.")

# --- Main Interface ---
st.title("🎓 Professional Report Analyzer")
st.markdown("##### Upload institutional guidelines to audit your academic reports against custom rules.")

st.markdown("<br>", unsafe_allow_html=True)

# --- Upload Section ---
u_col1, u_col2 = st.columns(2)

with u_col1:
    st.markdown("**Institutional Guidelines**")
    g_file = st.file_uploader("Rules (PDF/DOCX)", type=["pdf", "docx"], label_visibility="collapsed")

with u_col2:
    st.markdown("**Academic Report**")
    r_file = st.file_uploader("Your Report (PDF/DOCX)", type=["pdf", "docx"], label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

# --- Execution ---
if g_file and r_file:
    if st.button("🚀 EXECUTE COMPLIANCE AUDIT", use_container_width=True):
        with st.spinner("AI is retrieving guidelines and auditing your document..."):
            try:
                files = {
                    "guidelines": (g_file.name, g_file, g_file.type),
                    "report": (r_file.name, r_file, r_file.type)
                }
                # Your FastAPI backend endpoint
                response = requests.post("http://127.0.0.1:8000/upload_report/", files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    r = data.get("detected_rules", {})
                    
                    # --- 1. Detected Requirements Section ---
                    st.markdown("### 📋 Detected Institutional Requirements")
                    st.markdown(f"""
                    <div class="rule-card">
                        <span class="status-pill" style="background:#e8f0fe; color:#174ea6;">FONT: {r.get('font_name', 'N/A')}</span>
                        <span class="status-pill" style="background:#e8f0fe; color:#174ea6;">SIZE: {r.get('font_size', 'N/A')}pt</span>
                        <br><br>
                        <b>Required Sections:</b><br>{', '.join(r.get('sections', []))}
                    </div>
                    """, unsafe_allow_html=True)

                    # --- 2. Metrics ---
                    f_errors = data.get("format_errors", [])
                    s_errors = data.get("structure_errors", [])
                    
                    m1, m2, m3 = st.columns(3)
                    with m1:
                        score = max(0, 100 - (len(f_errors) * 2) - (len(s_errors) * 10))
                        st.metric("Compliance Score", f"{score}%")
                    with m2:
                        st.metric("Style Issues", len(f_errors))
                    with m3:
                        st.metric("Structure Gaps", len(s_errors))

                    st.markdown("<br>", unsafe_allow_html=True)

                    # --- 3. Result Tabs ---
                    tab1, tab2, tab3 = st.tabs(["📊 AUDIT LOG", "⚡ ACTION PLAN", "📥 EXPORT"])

                    with tab1:
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.subheader("Formatting & Style")
                            if f_errors:
                                for err in f_errors: st.error(err)
                            else:
                                st.success("Document styles comply with the guidelines.")
                        with col_b:
                            st.subheader("Structure & Sections")
                            if s_errors:
                                for err in s_errors: st.warning(err)
                            else:
                                st.success("All mandatory sections were detected.")

                    with tab2:
                        st.subheader("Short & Sweet Correction Guide")
                        st.markdown(f"""
                        <div class="action-plan">
                            {data.get("rag_suggestions", "No suggestions available.")}
                        </div>
                        """, unsafe_allow_html=True)

                    with tab3:
                        st.subheader("Download Annotated Report")
                        st.write("The annotated version includes highlights on all detected issues.")
                        h_path = data.get("highlighted_report_path")
                        if h_path and os.path.exists(h_path):
                            with open(h_path, "rb") as f:
                                st.download_button(
                                    label="Download Highlighted DOCX",
                                    data=f,
                                    file_name=f"Audit_Report_{r_file.name}",
                                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                    use_container_width=True
                                )
                        else:
                            st.info("Highlighting is currently available for DOCX report files.")

                else:
                    st.error(f"Backend Error ({response.status_code}): Please check your FastAPI server logs.")
            
            except Exception as e:
                st.error(f"Connection failed: {str(e)}")
else:
    # --- Landing Page Info ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    l_col1, l_col2, l_col3 = st.columns(3)
    with l_col1:
        st.markdown("🛡️ **Compliance Checks**")
        st.caption("Validates typography, margins, and page layouts against institution-specific rules.")
    with l_col2:
        st.markdown("🧩 **Structure Audit**")
        st.caption("Ensures all mandatory chapters like Abstract, Methodology, and References are present.")
    with l_col3:
        st.markdown("💡 **AI Reasoning**")
        st.caption("Uses RAG to provide granular, actionable feedback for complex formatting errors.")