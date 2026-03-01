import streamlit as st
from analyzer import analyze_requirement
from rewriter import rewrite_requirement
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import re
import pandas as pd

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
    st.markdown("## ReqForge Studio")

    st.session_state.theme = st.radio("Theme Mode", ["Dark", "Light"])

    st.markdown("---")

    page = st.radio(
        "Navigation",
        ["Welcome", "Analysis", "Methodology", "Architecture"]
    )

    st.markdown("---")
    st.caption("Version 3.0")
    st.caption("AI-Supported Requirements Governance Platform")

# ---------------------------------------------------
# THEME ENGINE
# ---------------------------------------------------

if st.session_state.theme == "Dark":
    bg = "#0f172a"
    card = "#111827"
    text = "#e5e7eb"
    accent = "#2563eb"
else:
    bg = "#f5f7fa"
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
    padding: 24px;
    border-radius: 12px;
    border: 1px solid #1f2937;
    box-shadow: 0 6px 16px rgba(0,0,0,0.05);
}}

.title {{
    font-size: 36px;
    font-weight: 700;
}}

.subtitle {{
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
        return False, "Include modal verb."
    return True, ""

# ---------------------------------------------------
# WELCOME
# ---------------------------------------------------

if page == "Welcome":

    st.markdown('<div class="title">ReqForge Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">AI-Supported Requirements Structuring & Quality Evaluation Platform</div>', unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns([2,1])

    with col1:
        st.markdown("""
        ### Executive Overview

        ReqForge Studio provides structured requirement analysis using
        rule-guided validation and modular AI-supported evaluation pipelines.

        Designed to support:
        - Structural compliance analysis
        - Ambiguity detection
        - Atomicity validation
        - Verifiability assessment
        - Batch governance workflows
        """)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Platform Capabilities")
        st.write("✔ Structural Quality Index")
        st.write("✔ Optimization Engine")
        st.write("✔ Compliance Mapping")
        st.write("✔ Batch Analytics")
        st.write("✔ Research-Oriented Architecture")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# METHODOLOGY
# ---------------------------------------------------

elif page == "Methodology":

    st.markdown('<div class="title">Evaluation Methodology</div>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("""
    Structural Quality Index (SQI) evaluates requirements across:

    1. Modal Compliance  
    2. Unambiguity  
    3. Atomic Structure  
    4. Verifiability  

    Hybrid Evaluation:
    - Structural Analysis
    - Modular Embedding Interface
    - Scoring & Compliance Mapping

    Designed for extensibility toward transformer-based semantic analysis.
    """)

# ---------------------------------------------------
# ARCHITECTURE
# ---------------------------------------------------

elif page == "Architecture":

    st.markdown('<div class="title">System Architecture</div>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("""
    ### Modular Pipeline

    - Input Validation Layer  
    - Structural Rule Engine  
    - Embedding Engine Interface (Extensible)  
    - Scoring & Compliance Module  
    - Optimization/Rewriting Engine  
    - Reporting & Export Layer  

    The embedding layer is abstracted to allow integration of pretrained
    transformer-based models without modifying evaluation logic.
    """)

# ---------------------------------------------------
# ANALYSIS
# ---------------------------------------------------

elif page == "Analysis":

    st.markdown('<div class="title">Executive Analysis Dashboard</div>', unsafe_allow_html=True)
    st.markdown("---")

    mode = st.radio("Mode", ["Single Requirement", "Batch Analysis"], horizontal=True)

    if mode == "Single Requirement":
        user_input = st.text_area("Enter Requirement", height=120)
        requirements = [user_input]
    else:
        batch_input = st.text_area("Enter Multiple Requirements (one per line)", height=150)
        requirements = batch_input.split("\n")

    run = st.button("Run Evaluation")

    if run:

        results = []

        for req in requirements:

            if not req.strip():
                continue

            valid, msg = validate_requirement(req)
            if not valid:
                st.error(msg)
                st.stop()

            issues = analyze_requirement(req)
            rewritten, explanation = rewrite_requirement(req)

            score = max(100 - len(issues)*20, 0)

            results.append({
                "Requirement": req,
                "Score": score,
                "Issues": len(issues)
            })

            st.markdown("---")

            if score >= 75:
                status_class = "good"
            elif score >= 50:
                status_class = "medium"
            else:
                status_class = "bad"

            st.markdown(f'<span class="badge {status_class}">Score: {score}%</span>', unsafe_allow_html=True)

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                number={'suffix': "%"},
                gauge={'axis': {'range': [0, 100]},
                       'bar': {'color': accent}}
            ))

            st.plotly_chart(fig, use_container_width=True)

            colA, colB = st.columns(2)

            with colA:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("### Original")
                st.write(req)
                st.markdown('</div>', unsafe_allow_html=True)

            with colB:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("### Optimized")
                st.write(rewritten)
                st.markdown('</div>', unsafe_allow_html=True)

        # ---------------- BATCH SUMMARY ----------------
        if len(results) > 1:

            st.markdown("---")
            st.markdown("## Batch Summary")

            df = pd.DataFrame(results)

            avg_score = int(df["Score"].mean())

            col1, col2 = st.columns(2)
            col1.metric("Average Score", f"{avg_score}%")
            col2.metric("Total Requirements", len(df))

            fig_bar = px.bar(df, x="Requirement", y="Score", height=400)
            st.plotly_chart(fig_bar, use_container_width=True)

# ---------------------------------------------------

st.markdown("---")
st.caption("ReqForge Studio v3.0 • AI-Supported Requirements Governance Platform")