import streamlit as st
from analyzer import analyze_requirement
from rewriter import rewrite_requirement
import plotly.graph_objects as go
from datetime import datetime
import re

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="ReqForge Studio",
    layout="wide",
    page_icon="📊"
)

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:
    st.markdown("## ReqForge Controls")

    st.session_state.theme = st.radio("Theme Mode", ["Dark", "Light"])

    st.markdown("---")

    page = st.radio(
        "Navigation",
        ["Welcome", "Requirement Analysis", "Methodology"]
    )

    st.markdown("---")

    st.markdown("### System Info")
    st.caption("Version 2.1")
    st.caption("Enterprise Governance Prototype")
    st.caption("AI-Supported Structuring Engine")

# ---------------------------------------------------
# THEME ENGINE
# ---------------------------------------------------

if st.session_state.theme == "Dark":
    bg = "#0f172a"
    card = "#111827"
    text = "#e5e7eb"
    accent = "#2563eb"
else:
    bg = "#f3f4f6"
    card = "#ffffff"
    text = "#111827"
    accent = "#2563eb"

st.markdown(f"""
<style>
.stApp {{
    background-color: {bg};
    color: {text};
}}

.card {{
    background-color: {card};
    padding: 28px;
    border-radius: 12px;
    border: 1px solid #1f2937;
    box-shadow: 0 4px 14px rgba(0,0,0,0.05);
}}

.main-title {{
    font-size: 34px;
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
    if not text.strip():
        return False, "Requirement cannot be empty."

    if len(text.split()) < 6:
        return False, "Requirement too short."

    if not re.search(r"\b(shall|must|will|should)\b", text.lower()):
        return False, "Include modal verb (shall/must/will/should)."

    return True, ""

# ---------------------------------------------------
# WELCOME SCREEN
# ---------------------------------------------------

if page == "Welcome":

    st.markdown('<div class="main-title">ReqForge Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtle">AI-Supported Requirements Governance Platform</div>', unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns([2,1])

    with col1:
        st.markdown("""
        ### Executive Overview

        ReqForge Studio is a structured requirements optimization platform designed to:

        - Evaluate requirement clarity and compliance
        - Detect ambiguity and compound structures
        - Improve verifiability and measurability
        - Provide executive-grade quality scoring
        - Support batch governance workflows

        Built with modular AI-supported architecture and extensible semantic evaluation pipelines.
        """)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Platform Capabilities")
        st.write("✔ Structural Quality Index")
        st.write("✔ Optimization Engine")
        st.write("✔ Compliance Mapping")
        st.write("✔ Batch Processing")
        st.write("✔ Executive Reporting")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    st.info("Navigate to 'Requirement Analysis' to begin structured evaluation.")

# ---------------------------------------------------
# METHODOLOGY PAGE
# ---------------------------------------------------

elif page == "Methodology":

    st.markdown('<div class="main-title">Evaluation Framework</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtle">Structural Quality Index (SQI)</div>', unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    The Structural Quality Index evaluates requirements across four core dimensions:

    1. Modal Compliance  
    2. Unambiguity  
    3. Atomic Structure  
    4. Verifiability  

    Hybrid Evaluation Model:
    - guided validation
    - Semantic structuring pipeline
    - Extensible embedding architecture

    Designed for enterprise governance and research prototyping.
    """)

# ---------------------------------------------------
# REQUIREMENT ANALYSIS
# ---------------------------------------------------

elif page == "Requirement Analysis":

    st.markdown('<div class="main-title">Executive Analysis Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtle">Single & Batch Structural Evaluation</div>', unsafe_allow_html=True)

    st.markdown("---")

    mode = st.radio(
        "Analysis Mode",
        ["Single Requirement", "Batch Analysis"],
        horizontal=True
    )

    if mode == "Single Requirement":
        requirement_input = st.text_area("Enter Requirement", height=120)
        requirements = [requirement_input]
    else:
        batch_input = st.text_area(
            "Enter Multiple Requirements (one per line)",
            height=150
        )
        requirements = batch_input.split("\n")

    run = st.button("Run Evaluation")

    if run:

        for requirement in requirements:

            if not requirement.strip():
                continue

            valid, msg = validate_requirement(requirement)

            if not valid:
                st.error(msg)
                st.stop()

            issues = analyze_requirement(requirement)
            rewritten, explanation = rewrite_requirement(requirement)

            score = max(100 - len(issues) * 20, 0)

            if score >= 75:
                status = "Compliant"
                status_class = "good"
            elif score >= 50:
                status = "Requires Improvement"
                status_class = "medium"
            else:
                status = "Critical Revision"
                status_class = "bad"

            st.markdown("---")
            st.markdown(f'<span class="badge {status_class}">{status}</span>', unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            col1.metric("Quality Score", f"{score}%")
            col2.metric("Issues Identified", len(issues))
            col3.metric("Confidence Index", f"{85 + score//5}%")

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

            colA, colB = st.columns(2)

            with colA:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("### Original")
                st.write(requirement)
                st.markdown('</div>', unsafe_allow_html=True)

            with colB:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("### Optimized")
                st.write(rewritten)
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("### Issue Classification")

            if issues:
                for issue in issues:
                    st.write(f"- {issue}")
            else:
                st.success("No structural issues detected.")

            st.session_state.history.append(
                {"requirement": requirement[:60], "score": score}
            )

    # History
    if st.session_state.history:
        st.markdown("---")
        st.markdown("### Session History")
        for entry in st.session_state.history:
            st.write(f"- {entry['requirement']}... | Score: {entry['score']}%")

st.markdown("---")
st.caption("ReqForge Studio v2.1 • Enterprise AI Requirements Governance Platform")