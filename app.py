import streamlit as st
from analyzer import analyze_requirement
from rewriter import rewrite_requirement
import plotly.graph_objects as go
import plotly.express as px
import time

st.set_page_config(page_title="ReqForge", layout="wide")

# ---------------- SIDEBAR ----------------
st.sidebar.title("ReqForge")
st.sidebar.markdown("Precision Engineering for Requirements")
st.sidebar.divider()
st.sidebar.markdown("### Features")
st.sidebar.markdown("""
- Structural Analysis  
- Rule-Based Optimization  
- Quality Scoring  
- Improvement Insights  
- History Tracking  
""")

# ---------------- STYLING ----------------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}
.big-title {
    font-size: 46px;
    font-weight: 700;
    color: #f1f5f9;
}
.subtitle {
    font-size: 18px;
    color: #94a3b8;
}
.section-card {
    padding: 20px;
    border-radius: 14px;
    background-color: #111827;
    border: 1px solid #334155;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HERO ----------------
st.markdown('<div class="big-title">ReqForge Studio</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Advanced optimization for high-quality software requirements.</div>', unsafe_allow_html=True)

st.divider()

# ---------------- INPUT ----------------
st.subheader("Requirement Input")
requirement = st.text_area("", height=130, placeholder="Enter requirement statement...")

analyze_button = st.button("Run Structural Optimization")

if analyze_button and requirement.strip():

    issues = analyze_requirement(requirement)
    rewritten, explanation = rewrite_requirement(requirement)

    modal_issue = any("modal" in issue.lower() for issue in issues)
    ambiguity_issue = any("ambiguous" in issue.lower() for issue in issues)
    atomic_issue = any("compound" in issue.lower() for issue in issues)
    measurable_issue = any("measurable" in issue.lower() for issue in issues)

    overall_score = 4 - sum([modal_issue, ambiguity_issue, atomic_issue, measurable_issue])
    score_percent = int((overall_score / 4) * 100)

    st.divider()

    # ---------------- GAUGE ----------------
    st.subheader("Structural Quality Index")

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score_percent,
        number={'suffix': "%"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#3b82f6"},
            'steps': [
                {'range': [0, 40], 'color': "#7f1d1d"},
                {'range': [40, 70], 'color': "#78350f"},
                {'range': [70, 100], 'color': "#064e3b"}
            ],
        }
    ))

    st.plotly_chart(fig, use_container_width=True)

    # ---------------- RADAR CHART ----------------
    st.subheader("Dimension Breakdown")

    categories = ["Modal Strength", "Clarity", "Atomicity", "Measurability"]
    values = [
        1 if not modal_issue else 0,
        1 if not ambiguity_issue else 0,
        1 if not atomic_issue else 0,
        1 if not measurable_issue else 0
    ]

    radar = go.Figure()

    radar.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        line_color="#3b82f6"
    ))

    radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1])
        ),
        showlegend=False
    )

    st.plotly_chart(radar, use_container_width=True)

    st.divider()

    # ---------------- BEFORE / AFTER ----------------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Original")
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.write(requirement)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("### Optimized")
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.write(rewritten)
        st.markdown('</div>', unsafe_allow_html=True)

    st.download_button(
        "Download Optimized Requirement",
        rewritten,
        file_name="optimized_requirement.txt"
    )

    st.divider()

    # ---------------- IMPROVEMENT INSIGHTS ----------------
    st.subheader("Optimization Insights")

    for exp in explanation:
        st.markdown(f"- {exp}")

    # ---------------- MINI ANALYTICS ----------------
    st.divider()
    st.subheader("Performance Snapshot")

    colA, colB, colC = st.columns(3)
    colA.metric("Quality Score", f"{score_percent}%")
    colB.metric("Detected Issues", len(issues))
    colC.metric("AI Confidence", f"{80 + overall_score*5}%")

# ---------------- FOOTER ----------------
st.divider()
st.caption("ReqForge Studio — Intelligent structural optimization engine for software requirements.")