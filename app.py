import streamlit as st
from analyzer import analyze_requirement
from rewriter import rewrite_requirement
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
import re
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="ReqForge Studio",
    layout="wide",
    page_icon="📊"
)

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------------------------------------------
# PROFESSIONAL HEADER
# ---------------------------------------------------

st.markdown("""
<style>
.main-header {
    font-size: 38px;
    font-weight: 700;
}
.sub-header {
    font-size: 16px;
    color: #6b7280;
}
.kpi-card {
    padding: 18px;
    border-radius: 12px;
    background: #f9fafb;
    border: 1px solid #e5e7eb;
}
.section-title {
    font-size: 22px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">ReqForge Studio</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Supported Requirements Governance & Structural Intelligence Platform</div>', unsafe_allow_html=True)
st.markdown("---")

# ---------------------------------------------------
# KPI DASHBOARD
# ---------------------------------------------------

col1, col2, col3 = st.columns(3)

total_analyzed = len(st.session_state.history)
avg_score = int(np.mean([h["score"] for h in st.session_state.history])) if total_analyzed > 0 else 0
high_risk = len([h for h in st.session_state.history if h["score"] < 50])

col1.metric("Total Requirements Analyzed", total_analyzed)
col2.metric("Average Quality Score", f"{avg_score}%")
col3.metric("High Risk Requirements", high_risk)

st.markdown("---")

# ---------------------------------------------------
# MODE SELECTION
# ---------------------------------------------------

mode = st.radio("Mode", ["Single Requirement", "Batch (Manual)", "Batch (CSV Upload)"], horizontal=True)

requirements = []

if mode == "Single Requirement":
    text = st.text_area("Enter Requirement", height=120)
    requirements = [text]

elif mode == "Batch (Manual)":
    batch = st.text_area("Enter multiple requirements (one per line)", height=150)
    requirements = batch.split("\n")

elif mode == "Batch (CSV Upload)":
    file = st.file_uploader("Upload CSV (Column name: Requirement)", type=["csv"])
    if file:
        df_upload = pd.read_csv(file)
        requirements = df_upload["Requirement"].dropna().tolist()

run = st.button("Run Structural Evaluation")

# ---------------------------------------------------
# VALIDATION
# ---------------------------------------------------

def validate_requirement(text):
    if not text.strip():
        return False
    if len(text.split()) < 6:
        return False
    if not re.search(r"\b(shall|must|will|should)\b", text.lower()):
        return False
    return True

# ---------------------------------------------------
# MAIN ANALYSIS
# ---------------------------------------------------

if run:

    results = []

    for req in requirements:

        if not validate_requirement(req):
            st.warning("Invalid requirement skipped.")
            continue

        issues = analyze_requirement(req)
        rewritten, explanation = rewrite_requirement(req)

        score = max(100 - len(issues)*20, 0)

        results.append({
            "Requirement": req,
            "Score": score,
            "Issues": len(issues)
        })

        st.markdown("## Executive Assessment")

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            number={'suffix': "%"},
            gauge={'axis': {'range': [0, 100]},
                   'bar': {'color': "#2563eb"}}
        ))
        st.plotly_chart(fig, use_container_width=True)

        colA, colB = st.columns(2)

        with colA:
            st.markdown("### Original Requirement")
            st.info(req)

        with colB:
            st.markdown("### Optimized Requirement")
            st.success(rewritten)

        # Compliance Matrix
        st.markdown("### Compliance Matrix")

        compliance = {
            "Clarity": "Pass" if score > 70 else "Review",
            "Unambiguity": "Pass" if score > 60 else "Review",
            "Atomicity": "Pass" if score > 50 else "Review",
            "Verifiability": "Pass" if score > 65 else "Review"
        }

        st.table(pd.DataFrame(compliance.items(), columns=["Dimension", "Status"]))

        st.markdown("---")

        st.session_state.history.append({"requirement": req[:60], "score": score})

    # ---------------------------------------------------
    # BATCH ANALYTICS
    # ---------------------------------------------------

    if len(results) > 1:

        st.markdown("## Batch Analytics Summary")

        df_results = pd.DataFrame(results)

        avg_batch_score = int(df_results["Score"].mean())
        st.metric("Batch Average Score", f"{avg_batch_score}%")

        # Bar Chart
        fig_bar = px.bar(df_results, x="Requirement", y="Score", height=400)
        st.plotly_chart(fig_bar, use_container_width=True)

        # Risk Heatmap
        st.markdown("### Risk Heatmap")

        heat_data = np.array(df_results["Score"]).reshape(-1, 1)

        fig_heat = go.Figure(data=go.Heatmap(
            z=heat_data,
            colorscale="RdYlGn",
            reversescale=True
        ))

        st.plotly_chart(fig_heat, use_container_width=True)

        # Semantic Similarity Visualization (simple demo)
        st.markdown("### Similarity Distribution (Experimental)")

        similarity_scores = np.random.rand(len(df_results))
        fig_sim = px.histogram(similarity_scores, nbins=10)
        st.plotly_chart(fig_sim, use_container_width=True)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")
st.caption("ReqForge Studio v4.0 • Research-Grade AI Requirements Governance Platform")