import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv(Path(__file__).parent.parent / ".env")

SAMPLE_PATH = Path(__file__).parent / "blood_work.txt"

EXTRACTION_PROMPT = """You are a medical data extraction assistant.

From the blood report below, extract ALL test values and classify each one as HIGH, LOW, or NORMAL
based on the reference ranges provided in the report.

Format your response as:
- Test Name: value | Status: HIGH/LOW/NORMAL | Reference: range

Blood Report:
{blood_report}
"""

DIET_PROMPT = """You are a clinical nutritionist specializing in Pakistani dietary habits.

Based on the blood work analysis below, write:
1. A short health summary in 2 lines explaining the patient's condition in simple language
2. A short, practical Pakistani diet plan having only two sections (1) Foods to avoid (2) Foods to eat more of.
   Do not include any other sections in diet plan.

Blood Work Analysis:
{analysis}
"""


@st.cache_resource
def get_llm() -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(model="gemini-2.5-flash")


def extract_blood_values(llm: ChatGoogleGenerativeAI, blood_report: str) -> str:
    response = llm.invoke(EXTRACTION_PROMPT.format(blood_report=blood_report))
    return response.text


def generate_diet_plan(llm: ChatGoogleGenerativeAI, analysis: str) -> str:
    response = llm.invoke(DIET_PROMPT.format(analysis=analysis))
    return response.text


def main() -> None:
    st.set_page_config(
        page_title="Blood Work Health Analyzer",
        page_icon="🩺",
        layout="wide",
    )

    st.title("🩺 Blood Work Health Analyzer")
    st.caption(
        "Upload a blood report to extract test values and get a Pakistani diet recommendation."
    )

    if not os.getenv("GOOGLE_API_KEY"):
        st.warning(
            "Set `GOOGLE_API_KEY` in a `.env` file at the project root before running analysis."
        )

    col_input, col_preview = st.columns([1, 1])

    with col_input:
        st.subheader("Blood Report Input")
        input_mode = st.radio(
            "Choose input method",
            ["Upload file", "Paste text", "Use sample report"],
            horizontal=True,
        )

        blood_report = ""

        if input_mode == "Upload file":
            uploaded = st.file_uploader(
                "Upload blood report (.txt)",
                type=["txt"],
                help="Plain text blood work report",
            )
            if uploaded is not None:
                blood_report = uploaded.read().decode("utf-8")
        elif input_mode == "Paste text":
            blood_report = st.text_area(
                "Paste blood report",
                height=320,
                placeholder="Paste your blood work report here...",
            )
        else:
            if SAMPLE_PATH.exists():
                blood_report = SAMPLE_PATH.read_text(encoding="utf-8")
                st.info(f"Loaded sample report from `{SAMPLE_PATH.name}`.")
            else:
                st.error("Sample report file not found.")

    with col_preview:
        st.subheader("Report Preview")
        if blood_report.strip():
            st.text_area(
                "Preview",
                value=blood_report,
                height=320,
                disabled=True,
                label_visibility="collapsed",
            )
        else:
            st.info("Your blood report will appear here.")

    st.divider()

    analyze = st.button("Analyze Report", type="primary", use_container_width=True)

    if analyze:
        if not blood_report.strip():
            st.error("Please provide a blood report before analyzing.")
            return

        llm = get_llm()

        with st.spinner("Stage 1: Extracting and classifying test values..."):
            try:
                extraction = extract_blood_values(llm, blood_report)
            except Exception as exc:
                st.error(f"Analysis failed during extraction: {exc}")
                return

        st.success("Stage 1 complete.")
        st.subheader("Stage 1: Blood Work Analysis")
        st.markdown(extraction)

        with st.spinner("Stage 2: Generating health summary and diet plan..."):
            try:
                diet_plan = generate_diet_plan(llm, extraction)
            except Exception as exc:
                st.error(f"Analysis failed during diet planning: {exc}")
                return

        st.success("Stage 2 complete.")
        st.subheader("Stage 2: Health Summary & Pakistani Diet Plan")
        st.markdown(diet_plan)

    st.divider()
    st.caption(
        "This tool is for informational purposes only and does not replace professional medical advice."
    )


if __name__ == "__main__":
    main()
