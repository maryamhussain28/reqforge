import streamlit as st
from analyzer import analyze_requirement
from rewriter import rewrite_requirement
import plotly.graph_objects as go
from datetime import datetime
import re

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="ReqForge Studio",
    layout="wide",
    page_icon="📊"
)

# ---------------------------------------------------
# SESSION INIT
# ---------------------------------------------------

if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:
    st.markdown("## ⚙️ Controls")

    st.session_state.theme = st.radio(
        "Theme",
        ["Dark", "Light"]
    )

    st.markdown("---")

    page = st.radio(
        "Navigation",
        ["Requirement Analysis", "Overview", "Methodology"]
    )

# ---------------------------------------------------
# THEME ENGINE (FIXED)
# ---------------------------------------------------

if st.session_state.theme == "Dark":
    bg = "#0f172a"
    card = "#111827"
    text = "#e5e7eb"
    accent = "#2563eb"
else:
    bg = "#f8fafc"
    card = "#ffffff"
    text = "#111827"
    accent = "#2563eb"

st.markdown(f"""
<style>
.stApp {{
    background-color: {bg};
    color: {text};
}}

.section-card {{
    background-color: {card};
    padding: 24px;
    border-radius: 10px;
    border: 1px solid #1f2937;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}}

.header-title {{
    font-size: 32px;
    font-weight: 700;
}}

.subtle {{
    color: #6b7280;
}}

.badge {{
    padding: 6px 12px;
    border-radius: 6px;
    font-weight: 600;
}}

.good {{ background-color: #065f46; color: white; }}
.medium {{ background-color: #92400e; color: white; }}
.bad {{ background-color: #7f1d1d; color: white; }}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# VALIDATION
# ---------------------------------------------------

def validate_requirement(text):
    if not text or not text.strip():
        return False, "Requirement cannot be empty."

    if len(text.split()) < 6:
        return False, "Requirement is too short."

    if not re.search(r"\b(shall|must|will|should)\b", text.lower()):
        return False, "Must include modal verb (shall/must/will/should)."

    return True, ""

# ---------------------------------------------------
# OVERVIEW PAGE
# ---------------------------------------------------

if page == "Overview":

    st.markdown('<div class="header-title">ReqForge Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtle">AI-Supported Requirements Governance Platform</div>', unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    ### Platform Capabilities

    - Structural quality validation  
    - Ambiguity and atomicity detection  
    - Optimization and reformulation  
    - Compliance alignment reporting  
    - Executive-level scoring dashboard  

    Designed as a modular AI-supported research prototype with extensible architecture.
    """)

# ---------------------------------------------------
# METHODOLOGY PAGE
# ---------------------------------------------------

elif page == "Methodology":

    st.markdown('<div class="header-title">Evaluation Framework</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtle">Structural Quality Index (SQI)</div>', unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    The SQI evaluates requirements across four dimensions:

    1. Modal Compliance  
    2. Unambiguity  
    3. Atomicity  
    4. Verifiability  

    Hybrid evaluation combines:
    - Rule-based structural checks
    - Semantic structuring logic
    - Extensible embedding interface

    Designed for enterprise-scale requirement governance.
    """)

# ---------------------------------------------------
# MAIN ANALYSIS
# ---------------------------------------------------

elif page == "Requirement Analysis":

    st.markdown('<div class="header-title">Executive Analysis Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtle">Automated Structural Quality Evaluation</div>', unsafe_allow_html=True)

    st.markdown("---")

    requirement = st.text_area("Enter Requirement", height=120)

    run = st.button("Run Evaluation")

    if run:

        valid, msg = validate_requirement(requirement)

        if not valid:
            st.error(msg)
            st.stop()

        issues = analyze_requirement(requirement)
        rewritten, explanation = rewrite_requirement(requirement)

        score = 100 - len(issues) * 20
        score = max(score, 0)

        # STATUS BADGE
        if score >= 75:
            status = "Compliant"
            status_class = "good"
        elif score >= 50:
            status = "Needs Improvement"
            status_class = "medium"
        else:
            status = "Critical Revision"
            status_class = "bad"

        st.markdown(f'<span class="badge {status_class}">{status}</span>', unsafe_allow_html=True)

        # METRICS ROW
        col1, col2, col3 = st.columns(3)
        col1.metric("Quality Score", f"{score}%")
        col2.metric("Issues Identified", len(issues))
        col3.metric("Confidence Index", f"{85 + score//5}%")

        # GAUGE
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            number={'suffix': "%"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': accent}
            }
        ))

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # TRANSFORMATION CARDS
        colA, colB = st.columns(2)

        with colA:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("### Original Requirement")
            st.write(requirement)
            st.markdown('</div>', unsafe_allow_html=True)

        with colB:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("### Optimized Requirement")
            st.write(rewritten)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")

        # ISSUE LIST
        st.markdown("### Issue Classification")

        if issues:
            for issue in issues:
                st.write(f"- {issue}")
        else:
            st.success("No structural issues identified.")

        st.markdown("---")

        # EXPORT
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        report = f"""
ReqForge Executive Report
Timestamp: {timestamp}

Original:
{requirement}

Optimized:
{rewritten}

Score: {score}%
Issues: {len(issues)}
"""

        st.download_button(
            "Download Executive Report",
            report,
            file_name="reqforge_report.txt"
        )

st.markdown("---")
st.caption("ReqForge Studio v2.0 • Enterprise AI Requirements Governance Platform")