import streamlit as st
from analyzer import analyze_requirement
from rewriter import rewrite_requirement
import plotly.graph_objects as go

st.set_page_config(
    page_title="ReqForge Studio",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- ENTERPRISE THEME ----------------
st.markdown("""
<style>
html, body, [class*="css"]  {
    font-family: 'Segoe UI', sans-serif;
}

.block-container {
    padding-top: 2rem;
    max-width: 1200px;
}

h1 {
    font-size: 28px;
    font-weight: 600;
}

h2 {
    font-size: 20px;
    font-weight: 600;
    margin-top: 40px;
}

.section {
    padding: 20px;
    border: 1px solid #1f2937;
    border-radius: 6px;
    background-color: #0f172a;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("ReqForge Studio")
st.caption("Internal Requirements Optimization Platform")

st.divider()

# ---------------- INPUT ----------------
st.header("Requirement Analysis")

requirement = st.text_area(
    "Enter requirement statement",
    height=100
)

run = st.button("Run Analysis")

if run and requirement.strip():

    issues = analyze_requirement(requirement)
    rewritten, explanation = rewrite_requirement(requirement)

    modal_issue = any("modal" in issue.lower() for issue in issues)
    ambiguity_issue = any("ambiguous" in issue.lower() for issue in issues)
    atomic_issue = any("compound" in issue.lower() for issue in issues)
    measurable_issue = any("measurable" in issue.lower() for issue in issues)

    overall_score = 4 - sum([modal_issue, ambiguity_issue, atomic_issue, measurable_issue])
    score_percent = int((overall_score / 4) * 100)

    st.divider()

    # ---------------- QUALITY INDEX ----------------
    st.header("Quality Index")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.metric("Overall Score", f"{score_percent}%")
        st.metric("Issues Identified", len(issues))
        st.metric("Confidence Level", f"{85 + overall_score*3}%")

    with col2:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score_percent,
            number={'suffix': "%"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#2563eb"}
            }
        ))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ---------------- RESULTS ----------------
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

    st.download_button(
        "Export Optimized Requirement",
        rewritten,
        file_name="optimized_requirement.txt"
    )

    st.divider()

    # ---------------- INSIGHTS ----------------
    st.header("Analysis Notes")

    if explanation:
        for exp in explanation:
            st.write(f"- {exp}")
    else:
        st.write("No structural adjustments required.")

st.divider()
st.caption("ReqForge Studio — Internal Requirements Engineering System")