import streamlit as st
from analyzer import analyze_requirement
from rewriter import rewrite_requirement
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import re
import numpy as np

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
# STYLING
# ---------------------------------------------------

st.markdown("""
<style>
.main-title {
    font-size: 36px;
    font-weight: 700;
}
.sub-title {
    font-size: 16px;
    color: #6b7280;
}
.section-title {
    font-size: 22px;
    font-weight: 600;
}
.card {
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #e5e7eb;
    background-color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.markdown('<div class="main-title">ReqForge Studio</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">AI-Supported Requirements Governance Platform</div>', unsafe_allow_html=True)
st.markdown("---")

# ---------------------------------------------------
# KPI DASHBOARD
# ---------------------------------------------------

total = len(st.session_state.history)
avg_score = int(np.mean([h["score"] for h in st.session_state.history])) if total else 0
high_risk = len([h for h in st.session_state.history if h["score"] < 50])

col1, col2, col3 = st.columns(3)
col1.metric("Total Analyzed", total)
col2.metric("Average Score", f"{avg_score}%")
col3.metric("High Risk Count", high_risk)

st.markdown("---")

# ---------------------------------------------------
# MODE SELECTION
# ---------------------------------------------------

mode = st.radio("Analysis Mode", ["Single Requirement", "Batch Analysis"], horizontal=True)

if mode == "Single Requirement":
    input_text = st.text_area("Enter Requirement", height=120)
    requirements = [input_text]
else:
    batch_input = st.text_area("Enter Multiple Requirements (one per line)", height=150)
    requirements = batch_input.split("\n")

run = st.button("Run Evaluation")

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

        if not req.strip():
            continue

        if not validate_requirement(req):
            st.error("Invalid requirement format.")
            st.stop()

        issues = analyze_requirement(req)
        rewritten, explanation = rewrite_requirement(req)

        score = max(100 - len(issues)*20, 0)

        results.append({
            "Requirement": req[:60],
            "Score": score
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
            st.markdown("### Original")
            st.info(req)

        with colB:
            st.markdown("### Optimized")
            st.success(rewritten)

        # Compliance Matrix
        st.markdown("### Compliance Matrix")

        compliance = pd.DataFrame({
            "Dimension": ["Clarity", "Unambiguity", "Atomicity", "Verifiability"],
            "Status": ["Pass" if score >= 70 else "Review"]*4
        })

        st.table(compliance)

        # Risk Classification
        if score >= 75:
            st.success("Risk Level: Low")
        elif score >= 50:
            st.warning("Risk Level: Moderate")
        else:
            st.error("Risk Level: High")

        st.markdown("---")

        st.session_state.history.append({"requirement": req[:60], "score": score})

    # ---------------------------------------------------
    # BATCH SUMMARY
    # ---------------------------------------------------

    if len(results) > 1:

        st.markdown("## Batch Summary")

        df = pd.DataFrame(results)

        avg_batch = int(df["Score"].mean())
        st.metric("Batch Average Score", f"{avg_batch}%")

        fig_bar = px.bar(df, x="Requirement", y="Score", height=400)
        st.plotly_chart(fig_bar, use_container_width=True)

# ---------------------------------------------------

st.markdown("---")
st.caption("ReqForge Studio • AI-Supported Structural Requirement Evaluation System")