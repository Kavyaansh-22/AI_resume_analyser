"""
AI Resume Analyzer & Job Match Checker
A simple Streamlit app that uses the OpenAI API to compare a resume
against a job description and return a structured match analysis.
"""

import os
import json
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key from .env file (for local development)
load_dotenv()

# Change the model here if needed (kept as a constant for easy editing)
MODEL_NAME = "models/gemini-2.5-flash"

SYSTEM_PROMPT = """You are an AI-powered resume screening assistant.
Compare the candidate's resume against the provided job description.
Evaluate skills, projects, experience, and relevance.
Consider: required technical skills, relevant projects/experience,
education/background relevance, and soft skills when relevant.
Return ONLY valid JSON. Do not include any text outside the JSON object.

The JSON must follow exactly this structure:
{
    "match_score": 0,
    "matched_skills": [],
    "missing_skills": [],
    "strengths": [],
    "weaknesses": [],
    "suggestions": [],
    "summary": ""
}

match_score must be an integer from 0 to 100."""


def analyze_resume(resume_text, job_text, api_key):
    """Send resume + job description to Gemini and return parsed JSON result."""
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        system_instruction=SYSTEM_PROMPT,
    )

    user_prompt = f"RESUME:\n{resume_text}\n\nJOB DESCRIPTION:\n{job_text}"

    response = model.generate_content(
        user_prompt,
        generation_config={
            "temperature": 0.3,
            "response_mime_type": "application/json",
        },
    )

    raw_text = response.text.strip()

    # Some models wrap JSON in ```json ... ``` — strip that if present
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        raw_text = raw_text.replace("json", "", 1).strip()

    return json.loads(raw_text)


def display_results(result):
    """Render the analysis results using simple Streamlit components."""
    score = result.get("match_score", 0)

    st.subheader("MATCH SCORE")
    st.metric(label="Overall Match", value=f"{score} / 100")
    st.progress(min(max(score, 0), 100) / 100)
    st.caption(
        "Match score is an AI-generated estimate based on the similarity "
        "between the resume and job requirements."
    )

    st.subheader("Matched Skills")
    st.success(", ".join(result.get("matched_skills", [])) or "None found")

    st.subheader("Missing Skills")
    st.warning(", ".join(result.get("missing_skills", [])) or "None")

    with st.expander("Strengths"):
        for item in result.get("strengths", []):
            st.write(f"- {item}")

    with st.expander("Weaknesses"):
        for item in result.get("weaknesses", []):
            st.write(f"- {item}")

    st.subheader("Suggestions")
    for i, tip in enumerate(result.get("suggestions", []), start=1):
        st.write(f"{i}. {tip}")

    st.subheader("Overall Analysis")
    st.write(result.get("summary", ""))


# ---------------- UI ----------------

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")

st.title("AI Resume Analyzer")
st.caption("AI-powered resume analysis and job matching")

resume_input = st.text_area("Resume", height=250, placeholder="Paste resume text here...")
job_input = st.text_area("Job Description", height=250, placeholder="Paste job description here...")

if st.button("Analyze Resume"):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        st.error("GEMINI_API_KEY not found. Please set it in your .env file.")
    elif not resume_input.strip():
        st.error("Please paste your resume text before analyzing.")
    elif not job_input.strip():
        st.error("Please paste the job description before analyzing.")
    else:
        with st.spinner("Analyzing resume against job description..."):
            try:
                result = analyze_resume(resume_input, job_input, api_key)
                display_results(result)
            except json.JSONDecodeError:
                st.error("The AI response could not be understood (invalid JSON). Please try again.")
            except Exception as e:
                st.error(f"An error occurred while contacting the Gemini API: {e}")