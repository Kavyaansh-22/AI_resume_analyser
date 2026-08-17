# AI Resume Analyzer & Job Match Checker

A simple, API-based Streamlit application that uses the Google Gemini API to
compare a candidate's resume against a job description and generate a
structured match analysis — including a match score, matched/missing
skills, strengths, weaknesses, and personalized suggestions.



---

## 1. Project Overview

The AI Resume Analyzer lets a user paste their resume text and a job
description into a web interface. When the user clicks **Analyze
Resume**, the app sends both texts to a Gemini language model, which
evaluates the resume against the job requirements and returns a
structured JSON result. This result is then displayed on the screen as
a simple, readable dashboard.

## 2. Problem Statement

Manually comparing a resume against a job description is time-consuming
and subjective. Students and job seekers often don't know which skills
they are missing or how well their resume actually matches a given job
posting. This project automates that comparison using an AI language
model, giving instant, structured feedback.

## 3. How the AI Is Used

The AI (a Google Gemini large language model) acts as the "brain" of the
application. It is given:
- The candidate's resume text
- The job description text
- A clear instruction (system prompt) telling it to act as an ATS/resume
  evaluator and return the result strictly in JSON format

The model uses natural language understanding to reason about skill
overlap, relevant projects/experience, and overall fit — something that
simple keyword matching cannot do well.

## 4. How the Gemini API Is Used

- The app uses the official `google-generativeai` Python SDK.
- A single API call is made per analysis using
  `model.generate_content(...)`.
- The request contains a **system instruction** (the evaluation rules,
  passed via `system_instruction`) and a **user prompt** (the resume +
  job description text).
- `generation_config` sets `response_mime_type="application/json"`,
  which tells Gemini to return a strict JSON response.
- The API key is read securely from an environment variable
  (`GEMINI_API_KEY`), loaded from a local `.env` file using
  `python-dotenv`. The key is never hard-coded.
- The model's response is parsed as JSON and rendered in the UI.

## 5. Technologies Used

| Technology         | Purpose                              |
|---------------------|---------------------------------------|
| Python              | Core programming language             |
| Streamlit           | Web-based user interface              |
| Google Gemini API   | AI-based resume/job matching analysis |
| python-dotenv       | Securely load API key from `.env`     |
| JSON                | Structured data exchange format       |

## 6. Project Workflow

```
User
 ↓
Resume + Job Description
 ↓
Streamlit Application
 ↓
Gemini API
 ↓
Structured JSON
 ↓
Resume Analysis Dashboard
```

1. User pastes their resume and a job description into two text boxes.
2. User clicks **Analyze Resume**.
3. The app validates the inputs (non-empty fields, valid API key).
4. The app sends a prompt containing both texts to the Gemini API.
5. The API returns a structured JSON object with the analysis.
6. The app parses the JSON and displays it using Streamlit components
   (`st.metric`, `st.progress`, `st.success`, `st.warning`,
   `st.expander`).

## 7. Installation

```bash
# 1. Clone or download this project folder
cd ai-resume-analyzer

# 2. (Optional but recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

## 8. How to Add the API Key

1. Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Copy `.env.example` to a new file named `.env`:
   ```bash
   cp .env.example .env
   ```
3. Open `.env` and paste your Gemini API key:
   ```
   GEMINI_API_KEY=your-actual-key-here
   ```
4. Save the file. The app will automatically load this key using
   `python-dotenv`. Never commit your real `.env` file to GitHub.

## 9. How to Run the Application

```bash
streamlit run app.py
```

This will open the app in your default web browser
(usually at `http://localhost:8501`).

You can use the provided demo files (`resume_strong.txt`,
`resume_medium.txt`, `resume_weak.txt`, `job_description.txt`) to test
the app — just copy-paste their contents into the text areas.

## 10. Limitations

- The match score is an AI-generated estimate, not a scientifically
  validated ATS score, and should not be treated as a guaranteed
  accuracy percentage.
- The app currently accepts only pasted plain text (no PDF/DOCX resume
  upload/parsing).
- Results depend on the quality and clarity of the pasted resume and
  job description text.
- No database — results are not saved between sessions.
- Requires an active internet connection and a valid Gemini API key.

## 11. Future Improvements

- Add PDF/DOCX resume upload with automatic text extraction.
- Allow exporting the analysis report as a PDF.
- Add support for comparing a resume against multiple job descriptions
  at once.
- Store analysis history using a lightweight database (e.g., SQLite).
- Add a resume "rewrite suggestions" feature to auto-generate improved
  bullet points.

---

## 30-Second Viva Explanation

"This project takes a resume and a job description as plain text input
through a Streamlit web app. It sends both to the Google Gemini API with a
prompt asking the model to act like an ATS evaluator and compare them.
The API returns a structured JSON response containing a match score,
matched and missing skills, strengths, weaknesses, and improvement
suggestions, which we then display on the dashboard using simple
Streamlit components. We used an API instead of training our own model
because a pre-trained large language model already understands
language and context far better than a small model we could train
ourselves with limited data and time."

### Likely Viva Questions & Answers

**1. Where is AI used?**
AI is used at the core analysis step — the Gemini language model reads
the resume and job description and generates the match score, skills
comparison, and suggestions.

**2. Why did you use an API instead of training your own model?**
Training a custom NLP model requires a large labeled dataset, significant
compute resources, and time. A pre-trained large language model, accessed
via an API, already understands language deeply and can perform this
kind of reasoning task accurately with a well-designed prompt — making it
far more practical for a mini-project.

**3. What is NLP?**
NLP (Natural Language Processing) is a branch of AI that enables
computers to understand, interpret, and generate human language. Here,
NLP is used to understand the meaning and context of resume and job
description text, not just match exact keywords.

**4. What does the API receive?**
The API receives a system instruction (telling it to act as a resume
evaluator and return JSON) and a user message containing the resume
text and the job description text.

**5. What does the API return?**
The API returns a text response containing a structured JSON object
with fields: `match_score`, `matched_skills`, `missing_skills`,
`strengths`, `weaknesses`, `suggestions`, and `summary`.

**6. How is the match score generated?**
The model conceptually evaluates the overlap between the resume and job
requirements — required technical skills, relevant projects/experience,
education/background relevance, and soft skills — and produces an
integer score from 0 to 100 based on this evaluation. It is an
AI-generated estimate, not a fixed mathematical formula.

**7. What are the limitations?**
The score is an AI estimate and not a certified ATS score; the app only
accepts pasted text (no file upload); there's no database to save past
results; and it depends on having a valid API key and internet access.

**8. How could this be improved in the future?**
By adding PDF/DOCX resume upload with text extraction, exporting reports
as PDF, comparing against multiple job descriptions, storing analysis
history in a database, and generating improved resume bullet-point
suggestions automatically.