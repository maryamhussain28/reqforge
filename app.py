import streamlit as st
from analyzer import analyze_requirement
from rewriter import rewrite_requirement
import plotly.graph_objects as go
from datetime import datetime

import re

from ai_module import RealTimeInferencePipeline

ai_pipeline = RealTimeInferencePipeline()

def validate_requirement(text):
    if not text or not text.strip():
        return False, "Requirement cannot be empty."

    if len(text.split()) < 6:
        return False, "Requirement is too short. Provide a complete structured sentence."

    if not re.search(r"\b(shall|must|will|should)\b", text.lower()):
        return False, "Requirement must contain a modal verb (e.g., 'shall', 'must')."

    if not re.search(r"[a-zA-Z]", text):
        return False, "Requirement must contain valid textual content."

    # Basic verb check
    if not re.search(r"\b(is|are|provide|process|authenticate|display|calculate|store|send|receive|generate)\b", text.lower()):
        return False, "Requirement does not appear to contain a valid action."

    return True, ""

st.set_page_config(
    page_title="ReqForge Studio",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- STYLING ----------------
st.markdown("""
<style>
.block-container {
    max-width: 1200px;
    padding-top: 2rem;
}
.section {
    padding: 20px;
    border: 1px solid #1f2937;
    border-radius: 6px;
    background-color: #0f172a;
}
.badge {
    padding: 6px 12px;
    border-radius: 6px;
    font-weight: 600;
}
.good { background-color: #065f46; color: white; }
.medium { background-color: #92400e; color: white; }
.bad { background-color: #7f1d1d; color: white; }
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("ReqForge Studio")
st.caption("Enterprise Requirements Optimization Platform")

st.divider()

# ---------------- INPUT MODE ----------------
mode = st.radio(
    "Select Mode",
    ["Single Requirement", "Batch Analysis"],
    horizontal=True
)

if mode == "Single Requirement":
    requirement = st.text_area("Enter requirement statement", height=100)
    requirements_list = [requirement]
else:
    batch_input = st.text_area(
        "Enter multiple requirements (one per line)",
        height=150
    )
    requirements_list = batch_input.split("\n")

run = st.button("Run Analysis")

# ---------------- SESSION HISTORY ----------------
if "history" not in st.session_state:
    st.session_state.history = []

if run:
   

    for requirement in requirements_list:

        if not requirement.strip():
            continue

        is_valid, error_message = validate_requirement(requirement)

        if not is_valid:
            st.error(f"Invalid Requirement: {error_message}")
            st.stop()

        issues = analyze_requirement(requirement)
        rewritten, explanation = rewrite_requirement(requirement)

        modal_issue = any("modal" in issue.lower() for issue in issues)
        ambiguity_issue = any("ambiguous" in issue.lower() for issue in issues)
        atomic_issue = any("compound" in issue.lower() for issue in issues)
        measurable_issue = any("measurable" in issue.lower() for issue in issues)

        overall_score = 4 - sum([modal_issue, ambiguity_issue, atomic_issue, measurable_issue])
        score_percent = int((overall_score / 4) * 100)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        st.divider()
        st.header("Executive Summary")

        # Status Classification
        if score_percent >= 75:
            status_class = "good"
            status_text = "Compliant"
        elif score_percent >= 50:
            status_class = "medium"
            status_text = "Requires Improvement"
        else:
            status_class = "bad"
            status_text = "Critical Revision Required"

        st.markdown(f'<span class="badge {status_class}">{status_text}</span>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("Quality Score", f"{score_percent}%")
        col2.metric("Issues Identified", len(issues))
        col3.metric("Confidence Level", f"{85 + overall_score*3}%")

        st.divider()

        # ---------------- QUALITY GAUGE ----------------
        st.subheader("Structural Quality Index")

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score_percent,
            number={'suffix': "%"},
            gauge={'axis': {'range': [0, 100]},
                   'bar': {'color': "#2563eb"}}
        ))

        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # ---------------- TRANSFORMATION ----------------
        st.header("Requirement Transformation")

        colA, colB = st.columns(2)

        with colA:
            st.subheader("Original")
            st.markdown('<div class="section">', unsafe_allow_html=True)
            st.write(requirement)
            st.markdown('</div>', unsafe_allow_html=True)

        with colB:
            st.subheader("Optimized")
            st.markdown('<div class="section">', unsafe_allow_html=True)
            st.write(rewritten)
            st.markdown('</div>', unsafe_allow_html=True)

        st.divider()

        # ---------------- ISSUE TABLE ----------------
        st.header("Issue Classification")

        if issues:
            for issue in issues:
                st.write(f"- {issue}")
        else:
            st.write("No structural issues identified.")

        st.divider()

        # ---------------- INSIGHTS ----------------
        st.header("Improvement Notes")

        if explanation:
            for exp in explanation:
                st.write(f"- {exp}")
        else:
            st.write("No additional optimization required.")

        st.divider()

        # ---------------- COMPLIANCE MAPPING ----------------
        st.header("Standards Alignment")

        compliance_map = {
            "Clarity": not modal_issue,
            "Unambiguity": not ambiguity_issue,
            "Atomicity": not atomic_issue,
            "Verifiability": not measurable_issue
        }

        for k, v in compliance_map.items():
            st.write(f"{k}: {'Aligned' if v else 'Needs Revision'}")

        st.divider()

        # ---------------- EXPORT ----------------
        report_text = f"""
ReqForge Analysis Report
Timestamp: {timestamp}

Original Requirement:
{requirement}

Optimized Requirement:
{rewritten}

Score: {score_percent}%
Issues: {len(issues)}

"""

        st.download_button(
            "Download Full Report",
            report_text,
            file_name="reqforge_report.txt"
        )

        # Save to history
        st.session_state.history.append(
            {"requirement": requirement, "score": score_percent}
        )

# ---------------- HISTORY PANEL ----------------
if st.session_state.history:
    st.divider()
    st.header("Session History")

    for entry in st.session_state.history:
        st.write(f"- {entry['requirement'][:60]}... | Score: {entry['score']}%")

st.divider()
st.caption("ReqForge Studio — Internal Requirements Governance Platform")