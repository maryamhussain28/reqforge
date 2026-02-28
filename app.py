import streamlit as st
from analyzer import analyze_requirement
from rewriter import rewrite_requirement
import plotly.graph_objects as go

st.set_page_config(
    page_title="ReqForge Studio",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- PROFESSIONAL STYLING ----------------
st.markdown("""
<style>

html, body, [class*="css"]  {
    font-family: 'Segoe UI', sans-serif;
}

.block-container {
    padding-top: 2rem;
}

.main-header {
    font-size: 34px;
    font-weight: 600;
    margin-bottom: 5px;
}

.sub-header {
    font-size: 16px;
    color: #94a3b8;
    margin-bottom: 20px;
}

.section-card {
    background-color: #111827;
    padding: 25px;
    border-radius: 10px;
    border: 1px solid #1f2937;
}

.metric-card {
    background-color: #0f172a;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #1f2937;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("### ReqForge Studio")
st.sidebar.markdown("Requirements Optimization Platform")
st.sidebar.divider()

st.sidebar.markdown("**Modules**")
st.sidebar.markdown("""
- Structural Analysis  
- Optimization Engine  
- Quality Index  
- Insights Reporting  
- Performance Metrics  
""")

# ---------------- HEADER ----------------
st.markdown('<div class="main-header">ReqForge Studio</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Enterprise-grade structural optimization for software requirements.</div>', unsafe_allow_html=True)

st.divider()

# ---------------- INPUT SECTION ----------------
st.subheader("Requirement Statement")

requirement = st.text_area(
    "",
    height=120,
    placeholder="The system shall authenticate users within 2 seconds."
)

analyze_button = st.button("Analyze & Optimize")

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

    # ---------------- QUALITY INDEX ----------------
    st.subheader("Structural Quality Index")

    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score_percent,
        number={'suffix': "%"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#2563eb"},
            'steps': [
                {'range': [0, 40], 'color': "#7f1d1d"},
                {'range': [40, 70], 'color': "#92400e"},
                {'range': [70, 100], 'color': "#065f46"}
            ],
        }
    ))

    st.plotly_chart(gauge, use_container_width=True)

    # ---------------- RADAR ----------------
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
        line_color="#2563eb"
    ))

    radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=False
    )

    st.plotly_chart(radar, use_container_width=True)

    st.divider()

    # ---------------- BEFORE / AFTER ----------------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Original Requirement")
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.write(requirement)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("#### Optimized Requirement")
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.write(rewritten)
        st.markdown('</div>', unsafe_allow_html=True)

    st.download_button(
        "Download Optimized Requirement",
        rewritten,
        file_name="optimized_requirement.txt"
    )

    st.divider()

    # ---------------- INSIGHTS ----------------
    st.subheader("Optimization Insights")

    if explanation:
        for exp in explanation:
            st.write(f"- {exp}")
    else:
        st.write("No structural improvements identified.")

    st.divider()

    # ---------------- METRICS ----------------
    st.subheader("Performance Metrics")

    colA, colB, colC = st.columns(3)

    with colA:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Quality Score", f"{score_percent}%")
        st.markdown('</div>', unsafe_allow_html=True)

    with colB:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Issues Detected", len(issues))
        st.markdown('</div>', unsafe_allow_html=True)

    with colC:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Confidence Index", f"{85 + overall_score*3}%")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.divider()
st.caption("ReqForge Studio — Requirements Engineering Optimization Platform.")