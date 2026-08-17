"""
AI Resume Analyzer & Job Match Checker
A polished Streamlit app that uses the Gemini API to compare a resume
against a job description and return a structured, concise match analysis.
"""

import os
import json
import re
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key from .env file (for local development)
load_dotenv()

# Change the model here if needed (kept as a constant for easy editing)
MODEL_NAME = "models/gemini-2.5-flash"

SYSTEM_PROMPT = """You are a senior technical recruiter with 15 years of experience \
screening resumes. You are known for being sharp, blunt, and concise — never vague, \
never filler, never generic praise.

Compare the candidate's resume against the job description. Evaluate required \
technical skills, relevant projects/experience, education/background relevance, \
and soft skills (only if clearly relevant).

STRICT OUTPUT RULES:
- Return ONLY valid JSON. No markdown, no code fences, no text outside the JSON object.
- Every list item must be a short, specific phrase (max ~12 words). No full sentences, \
no restating the obvious, no filler like "Great communication skills" unless evidence \
from the resume actually supports it.
- matched_skills / missing_skills: single skill or tool names only, no descriptions.
- strengths / weaknesses: 3 to 5 items each, ranked by importance, most important first.
- suggestions: exactly 3 items, each a concrete, actionable next step (not generic advice).
- summary: exactly 2 sentences. Sentence 1 = the verdict. Sentence 2 = the single \
biggest reason for it. No hedging, no "overall" filler.
- Be honest and critical. Do not inflate the score to be nice.

The JSON must follow exactly this structure:
{
    "match_score": 0,
    "verdict": "",
    "matched_skills": [],
    "missing_skills": [],
    "strengths": [],
    "weaknesses": [],
    "suggestions": [],
    "summary": ""
}

match_score must be an integer from 0 to 100.
verdict must be exactly one of: "Strong Match", "Good Match", "Partial Match", "Weak Match"."""


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
            "temperature": 0.2,
            "response_mime_type": "application/json",
        },
    )

    raw_text = response.text.strip()

    # Defensive cleanup in case the model still wraps JSON in a code fence
    if raw_text.startswith("```"):
        raw_text = re.sub(r"^```(json)?", "", raw_text)
        raw_text = raw_text.rstrip("`").strip()

    return json.loads(raw_text)


# ---------------- Styling ----------------
# Palette: ink & brass. A restrained, editorial "assessment dossier" look —
# deep charcoal ground, warm brass accent, hairline rules, serif headings.

def inject_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500&display=swap');

        :root {
            --ink: #14161B;
            --panel: #1B1E25;
            --panel-2: #1F232B;
            --hairline: #2B2F3A;
            --brass: #C6A15B;
            --brass-dim: #8A733F;
            --paper: #EDEAE2;
            --muted: #8D93A3;
            --sage: #7FA084;
            --rust: #B0654C;
        }

        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

        .stApp {
            background: var(--ink);
            background-image:
                radial-gradient(ellipse 900px 500px at 15% -5%, rgba(198,161,91,0.06), transparent 60%);
        }

        section[data-testid="stSidebar"] { display: none; }
        #MainMenu, footer { visibility: hidden; }
        .block-container { max-width: 880px; padding-top: 2.2rem; }

        /* ---------- Masthead ---------- */
        .masthead {
            border-bottom: 1px solid var(--hairline);
            padding-bottom: 1.4rem;
            margin-bottom: 2.2rem;
        }
        .masthead .eyebrow {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72rem;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: var(--brass);
            margin-bottom: 0.5rem;
        }
        .masthead h1 {
            font-family: 'Fraunces', serif;
            font-weight: 600;
            font-size: 2.4rem;
            color: var(--paper);
            letter-spacing: -0.01em;
            margin: 0 0 0.35rem 0;
        }
        .masthead p {
            color: var(--muted);
            font-size: 0.98rem;
            margin: 0;
        }

        /* ---------- Inputs ---------- */
        .input-label {
            font-family: 'JetBrains Mono', monospace;
            font-weight: 500;
            font-size: 0.72rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--muted);
            margin-bottom: 0.5rem;
        }
        .stTextArea textarea {
            background-color: var(--panel) !important;
            border: 1px solid var(--hairline) !important;
            border-radius: 6px !important;
            color: var(--paper) !important;
            font-size: 0.9rem !important;
            line-height: 1.5 !important;
        }
        .stTextArea textarea:focus {
            border: 1px solid var(--brass) !important;
            box-shadow: 0 0 0 1px var(--brass) !important;
        }
        .stTextArea textarea::placeholder { color: #565C6B !important; }

        div.stButton > button {
            width: 100%;
            background: var(--brass);
            color: #1A1508;
            font-weight: 700;
            font-size: 0.92rem;
            letter-spacing: 0.02em;
            padding: 0.65rem 0;
            border: none;
            border-radius: 6px;
            margin-top: 0.4rem;
            transition: background 0.15s ease;
        }
        div.stButton > button:hover {
            background: #D4B172;
            color: #1A1508;
            border: none;
        }

        /* ---------- Report sections ---------- */
        .report-section {
            border-top: 1px solid var(--hairline);
            padding: 1.6rem 0;
        }
        .report-section:first-of-type { border-top: none; }
        .section-label {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72rem;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            color: var(--brass);
            margin-bottom: 0.9rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .section-label::after {
            content: "";
            flex: 1;
            height: 1px;
            background: var(--hairline);
        }

        /* ---------- Verdict block ---------- */
        .verdict-row {
            display: flex;
            align-items: center;
            gap: 1.8rem;
        }
        .score-num {
            font-family: 'Fraunces', serif;
            font-weight: 600;
            font-size: 3.6rem;
            color: var(--paper);
            line-height: 1;
            min-width: 130px;
        }
        .score-num span {
            font-family: 'Inter', sans-serif;
            font-size: 1rem;
            color: var(--muted);
            font-weight: 500;
        }
        .verdict-tag {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            padding: 0.28rem 0.7rem;
            border-radius: 3px;
            display: inline-block;
            margin-bottom: 0.55rem;
            border: 1px solid;
        }
        .verdict-summary {
            color: #C9CDD6;
            font-size: 1.02rem;
            line-height: 1.6;
            margin: 0;
        }

        /* ---------- Chips ---------- */
        .chip {
            display: inline-block;
            padding: 0.3rem 0.75rem;
            border-radius: 3px;
            font-size: 0.84rem;
            font-weight: 500;
            margin: 0 0.4rem 0.4rem 0;
            border: 1px solid var(--hairline);
            background: var(--panel-2);
            color: var(--paper);
        }
        .chip-missing {
            color: var(--rust);
            border-color: rgba(176,101,76,0.35);
        }
        .chip-matched {
            color: var(--sage);
            border-color: rgba(127,160,132,0.3);
        }
        .empty-note { color: #5B6070; font-size: 0.9rem; font-style: italic; }

        /* ---------- Bullet list ---------- */
        .bullet-row {
            display: flex;
            gap: 0.7rem;
            padding: 0.5rem 0;
            border-bottom: 1px solid var(--hairline);
            color: #D6D9E0;
            font-size: 0.95rem;
            line-height: 1.5;
        }
        .bullet-row:last-child { border-bottom: none; }
        .bullet-marker {
            font-family: 'JetBrains Mono', monospace;
            flex-shrink: 0;
            font-weight: 600;
            font-size: 0.85rem;
            width: 1.1rem;
            padding-top: 0.1rem;
        }
        .marker-strength { color: var(--sage); }
        .marker-weakness { color: var(--rust); }
        .marker-suggestion { color: var(--brass); }
    </style>
    """, unsafe_allow_html=True)


def score_style(score):
    if score >= 80:
        return "Strong Match", "#7FA084", "rgba(127,160,132,0.35)"
    if score >= 60:
        return "Good Match", "#C6A15B", "rgba(198,161,91,0.35)"
    if score >= 40:
        return "Partial Match", "#C99A5B", "rgba(201,154,91,0.35)"
    return "Weak Match", "#B0654C", "rgba(176,101,76,0.35)"


def section(label):
    st.markdown(f'<div class="report-section"><div class="section-label">{label}</div>', unsafe_allow_html=True)


def end_section():
    st.markdown('</div>', unsafe_allow_html=True)


def display_results(result):
    """Render the analysis results as a single-column, section-by-section report."""
    score = int(result.get("match_score", 0) or 0)
    score = min(max(score, 0), 100)
    fallback_verdict, color, border = score_style(score)
    verdict = result.get("verdict") or fallback_verdict

    # Verdict
    section("Match Assessment")
    st.markdown(f"""
        <div class="verdict-row">
            <div class="score-num">{score}<span> / 100</span></div>
            <div>
                <div class="verdict-tag" style="color:{color}; border-color:{border}; background:{color}14;">{verdict}</div>
                <p class="verdict-summary">{result.get("summary", "")}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    end_section()

    # Matched skills
    section("Matched Skills")
    matched = result.get("matched_skills", [])
    if matched:
        st.markdown("".join(f'<span class="chip chip-matched">{s}</span>' for s in matched), unsafe_allow_html=True)
    else:
        st.markdown('<span class="empty-note">No overlapping skills found.</span>', unsafe_allow_html=True)
    end_section()

    # Missing skills
    section("Missing Skills")
    missing = result.get("missing_skills", [])
    if missing:
        st.markdown("".join(f'<span class="chip chip-missing">{s}</span>' for s in missing), unsafe_allow_html=True)
    else:
        st.markdown('<span class="empty-note">No notable gaps.</span>', unsafe_allow_html=True)
    end_section()

    # Strengths
    section("Strengths")
    strengths = result.get("strengths", [])
    if strengths:
        st.markdown("".join(
            f'<div class="bullet-row"><span class="bullet-marker marker-strength">+</span><span>{s}</span></div>'
            for s in strengths
        ), unsafe_allow_html=True)
    else:
        st.markdown('<span class="empty-note">None listed.</span>', unsafe_allow_html=True)
    end_section()

    # Weaknesses
    section("Weaknesses")
    weaknesses = result.get("weaknesses", [])
    if weaknesses:
        st.markdown("".join(
            f'<div class="bullet-row"><span class="bullet-marker marker-weakness">−</span><span>{s}</span></div>'
            for s in weaknesses
        ), unsafe_allow_html=True)
    else:
        st.markdown('<span class="empty-note">None listed.</span>', unsafe_allow_html=True)
    end_section()

    # Suggestions
    section("Suggestions to Improve Fit")
    suggestions = result.get("suggestions", [])
    if suggestions:
        st.markdown("".join(
            f'<div class="bullet-row"><span class="bullet-marker marker-suggestion">{i:02d}</span><span>{s}</span></div>'
            for i, s in enumerate(suggestions, start=1)
        ), unsafe_allow_html=True)
    else:
        st.markdown('<span class="empty-note">None.</span>', unsafe_allow_html=True)
    end_section()


# ---------------- UI ----------------

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="centered")

inject_css()

st.markdown("""
<div class="masthead">
    <div class="eyebrow">Candidate Assessment</div>
    <h1>Resume Analyzer</h1>
    <p>Paste a resume and job description for a sharp, honest fit assessment.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="input-label">Resume</div>', unsafe_allow_html=True)
resume_input = st.text_area("Resume", height=220, placeholder="Paste resume text here...", label_visibility="collapsed")

st.markdown('<div class="input-label" style="margin-top: 1.1rem;">Job Description</div>', unsafe_allow_html=True)
job_input = st.text_area("Job Description", height=220, placeholder="Paste job description here...", label_visibility="collapsed")

analyze_clicked = st.button("Analyze Resume")

if analyze_clicked:
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