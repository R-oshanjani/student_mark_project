# app/streamlit_app.py

import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="3-Subject Pass/Fail Predictor",
    page_icon="📘",
    layout="wide",
)


# ---------- CORE LOGIC ----------
def evaluate_result(g1: float, g2: float, g3: float):
    """
    Simple pass/fail logic:
    - Fail if any subject < 35
    - Or if average < 40
    - Else Pass
    """
    total = g1 + g2 + g3
    avg = total / 3.0

    fail_reasons = []
    if g1 < 35:
        fail_reasons.append("Subject 1 mark is below 35.")
    if g2 < 35:
        fail_reasons.append("Subject 2 mark is below 35.")
    if g3 < 35:
        fail_reasons.append("Subject 3 mark is below 35.")
    if avg < 40:
        fail_reasons.append("Overall average is below 40.")

    status = "Fail" if fail_reasons else "Pass"
    return status, avg, total, fail_reasons


def build_suggestions(g1: float, g2: float, g3: float, status: str, avg: float):
    suggestions = []

    # Identify weakest subject
    marks = {"Subject 1": g1, "Subject 2": g2, "Subject 3": g3}
    weakest_subj = min(marks, key=marks.get)
    weakest_mark = marks[weakest_subj]

    if status == "Fail":
        suggestions.append(
            f"**{weakest_subj}** is your weakest area (**{weakest_mark:.1f}**). "
            "Allocate extra daily revision time to this subject."
        )
        for subj, m in marks.items():
            if m < 35:
                suggestions.append(
                    f"{subj} is below the minimum pass mark. "
                    "Redo core topics and solve at least 5–10 practice questions per day."
                )
        if avg < 40:
            suggestions.append(
                "Your **overall average is low**. Create a realistic daily study plan "
                "with fixed time blocks for each subject (e.g., 1–2 hours per subject)."
            )
        suggestions.append(
            "After revising, take short timed mock tests and track your improvement."
        )

    else:  # Pass
        if avg < 60:
            suggestions.append(
                f"You passed, but your average (**{avg:.1f}**) can be better. "
                f"Focus on **{weakest_subj}** to boost your overall score."
            )
        else:
            suggestions.append(
                f"Solid performance with an average of **{avg:.1f}**. "
                "Maintain your current study routine and keep revising regularly."
            )

        suggestions.append(
            "Use previous-year question papers and timed practice sessions to "
            "strengthen exam performance."
        )

    return suggestions


# ---------- UI HELPERS ----------
def inject_css():
    st.markdown(
        """
        <style>
        /* Center main content a bit and tighten width */
        .main .block-container {
            max-width: 900px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }
        /* Make the predict button full width on its column */
        .stButton>button {
            width: 100%;
            border-radius: 999px;
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def header():
    st.markdown(
        "<h1 style='text-align: center;'>📘 3-Subject Pass/Fail Predictor</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center; color: #aaaaaa;'>"
        "Simple rule-based evaluation using three subject marks (G1, G2, G3)."
        "</p>",
        unsafe_allow_html=True,
    )
    st.markdown("---")


def input_form():
    st.subheader("Enter Marks")

    col1, col2, col3 = st.columns(3)

    with col1:
        g1 = st.number_input(
            "G1 - Subject 1",
            min_value=0.0,
            max_value=100.0,
            value=40.0,
            step=1.0,
        )
    with col2:
        g2 = st.number_input(
            "G2 - Subject 2",
            min_value=0.0,
            max_value=100.0,
            value=40.0,
            step=1.0,
        )
    with col3:
        g3 = st.number_input(
            "G3 - Subject 3",
            min_value=0.0,
            max_value=100.0,
            value=40.0,
            step=1.0,
        )

    return g1, g2, g3


def result_section(status, avg, total, reasons):
    # Centered card for result + metrics
    st.markdown("---")
    st.subheader("Result Summary")

    c1, c2, c3 = st.columns(3)

    with c1:
        if status == "Pass":
            st.success("✅ **PASS**")
        else:
            st.error("❌ **FAIL**")

    with c2:
        st.metric(label="Total Marks", value=f"{total:.1f}")

    with c3:
        st.metric(label="Average", value=f"{avg:.1f}")

    if status == "Fail" and reasons:
        st.markdown("**Reasons for Failure:**")
        for r in reasons:
            st.markdown(f"- {r}")


def suggestions_section(g1, g2, g3, status, avg):
    st.subheader("Suggestions to Improve")
    tips = build_suggestions(g1, g2, g3, status, avg)
    for tip in tips:
        st.markdown(f"- {tip}")


# ---------- MAIN APP ----------
def main():
    inject_css()
    header()

    g1, g2, g3 = input_form()

    st.markdown("")
    center_col = st.columns([1, 1, 1])[1]
    with center_col:
        clicked = st.button("Predict Pass / Fail")

    if clicked:
        status, avg, total, reasons = evaluate_result(g1, g2, g3)
        result_section(status, avg, total, reasons)
        suggestions_section(g1, g2, g3, status, avg)


if __name__ == "__main__":
    main()
