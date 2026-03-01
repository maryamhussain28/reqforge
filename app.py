import streamlit as st
from analyzer import analyze_requirement
from rewriter import rewrite_requirement
import plotly.graph_objects as go
from datetime import datetime
import re

# ---------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------

st.set_page_config(
    page_title="ReqForge Studio",
    layout="wide",
    page_icon="📊"
)

# ---------------------------------------------------
# THEME TOGGLE
# ---------------------------------------------------

if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

with st.sidebar:
    st.title("⚙️ Platform Controls")
    st.session_state.theme = st.radio(
        "Theme Mode",
        ["Dark", "Light"]
    )

    st.markdown("---")
    st.markdown("### Navigation")
    page = st.radio(
        "Go to",
        ["Requirement Analysis", "Platform Overview", "Methodology"]
    )

# ---------------------------------------------------
# THEME STYLING
# ---------------------------------------------------

if st.session_state.theme == "Dark":
    bg_color = "#0f172a"
    card_color = "#111827"
    text_color = "#e5e7eb"
else:
    bg_color = "#f8fafc"
    card_color = "#ffffff"
    text_color = "#111827"

st.markdown(f"""
<style>
body {{
    background-color: {bg_color};
    color: {text_color};
}}

.section {{
    padding: 20px;
    border-radius: 8px;
    background-color: {card_color};
    border: 1px solid #1f2937;
}}

.metric-card {{
    padding: 15px;
    border-radius: 8px;
    background-color: {card_color};
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
# VALIDATION FUNCTION
# ---------------------------------------------------

def validate_requirement(text):
    if not text or not text.strip():
        return False, "Requirement cannot be empty."

    if len(text.split()) < 6:
        return False, "Requirement is too short. Provide a complete structured sentence."

    if not re.search(r"\b(shall|must|will|should)\b", text.lower()):
        return False, "Requirement must contain a modal verb (e.g., 'shall', 'must')."

    if not re.search(r"[a-zA-Z]", text):
        return False, "Requirement must contain valid textual content."

    if not re.search(r"\b(is|are|provide|process|authenticate|display|calculate|store|send|receive|generate)\b", text.lower()):
        return False, "Requirement does not appear to contain a valid action."

    return True, ""

# ---------------------------------------------------
# PAGE ROUTING
# ---------------------------------------------------

if page == "Platform Overview":

    st.title("ReqForge Studio")
    st.subheader("AI-Supported Requirements Structuring & Governance Platform")

    st.markdown("""
    ReqForge Studio is a structured requirements governance prototype designed to:
    - Evaluate structural requirement quality
    - Detect ambiguity and non-atomic constructs
    - Improve measurability and compliance
    - Support enterprise-level documentation workflows

    This platform demonstrates modular AI-supported architecture with extensible embedding integration.
    """)

elif page == "Methodology":

    st.title("Evaluation Methodology")

    st.markdown("""
    ### Structural Quality Index (SQI)

    The SQI evaluates requirements across four dimensions:

    1. Modal Compliance
    2. Unambiguity
    3. Atomicity
    4. Verifiability

    Each structural issue reduces the aggregate score.

    Hybrid evaluation approach:
    - Rule-guided validation
    - Semantic structuring pipeline
    - Modular embedding architecture (extensible)

    This design supports scalable enterprise integration.
    """)

# ---------------------------------------------------
# MAIN ANALYSIS PAGE
# ---------------------------------------------------

elif page == "Requirement Analysis":

    st.title("ReqForge Studio")
    st.caption("Enterprise Requirements Optimization Dashboard")

    mode = st.radio(
        "Analysis Mode",
        ["Single Requirement", "Batch Analysis"],
        horizontal=True
    )

    if mode == "Single Requirement":
        requirement = st.text_area("Enter requirement statement", height=120)
        requirements_list = [requirement]
    else:
        batch_input = st.text_area(
            "Enter multiple requirements (one per line)",
            height=150
        )
        requirements_list = batch_input.split("\n")

    run = st.button("Run Structural Evaluation")

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

            # Executive Summary
            st.markdown("## Executive Assessment")

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
            col3.metric("Confidence Index", f"{85 + overall_score*3}%")

            # Gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score_percent,
                number={'suffix': "%"},
                gauge={'axis': {'range': [0, 100]},
                       'bar': {'color': "#2563eb"}}
            ))
            st.plotly_chart(fig, use_container_width=True)

            # Transformation
            st.markdown("## Requirement Transformation")

            colA, colB = st.columns(2)

            with colA:
                st.markdown("### Original")
                st.markdown('<div class="section">', unsafe_allow_html=True)
                st.write(requirement)
                st.markdown('</div>', unsafe_allow_html=True)

            with colB:
                st.markdown("### Optimized")
                st.markdown('<div class="section">', unsafe_allow_html=True)
                st.write(rewritten)
                st.markdown('</div>', unsafe_allow_html=True)

            # Issue Classification
            st.markdown("## Issue Classification")
            if issues:
                for issue in issues:
                    st.write(f"- {issue}")
            else:
                st.write("No structural issues identified.")

            # Standards Alignment
            st.markdown("## Standards Alignment")

            compliance_map = {
                "Clarity": not modal_issue,
                "Unambiguity": not ambiguity_issue,
                "Atomicity": not atomic_issue,
                "Verifiability": not measurable_issue
            }

            for k, v in compliance_map.items():
                st.write(f"{k}: {'Aligned' if v else 'Needs Revision'}")

            # Export
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
                "Download Report",
                report_text,
                file_name="reqforge_report.txt"
            )

            st.session_state.history.append(
                {"requirement": requirement, "score": score_percent}
            )

    # Session History
    if st.session_state.history:
        st.markdown("## Session History")
        for entry in st.session_state.history:
            st.write(f"- {entry['requirement'][:60]}... | Score: {entry['score']}%")

st.markdown("---")
st.caption("ReqForge Studio v1.3 • AI-Supported Requirements Governance Prototype")