import os
from typing import Dict, Optional

import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")

st.set_page_config(page_title="ResAI Campus", layout="wide")

st.markdown(
    """
    <style>
      :root {
        --ink: #0f172a;
        --muted: #334155;
        --paper: #f8fafc;
        --brand: #0ea5e9;
        --brand-2: #14b8a6;
        --line: #dbeafe;
      }
      .stApp {
        background:
          radial-gradient(circle at 12% 14%, rgba(20,184,166,.18), transparent 32%),
          radial-gradient(circle at 88% 24%, rgba(14,165,233,.17), transparent 35%),
          linear-gradient(180deg, #f0f9ff 0%, #f8fafc 55%, #ffffff 100%);
      }
      .hero {
        padding: 1.1rem 1.2rem;
        border: 1px solid var(--line);
        border-radius: 16px;
        background: linear-gradient(120deg, #ffffff 0%, #ecfeff 60%, #eff6ff 100%);
        box-shadow: 0 12px 30px rgba(2, 132, 199, .08);
        margin-bottom: 1rem;
      }
      .hero h1 {
        margin: 0;
        font-size: 2rem;
        color: var(--ink);
      }
      .hero p {
        margin: 0.35rem 0 0;
        color: var(--muted);
      }
      .panel {
        padding: 1rem;
        border-radius: 14px;
        border: 1px solid #dbeafe;
        background: #ffffff;
        box-shadow: 0 6px 24px rgba(15, 23, 42, 0.05);
      }
      .result {
        border: 1px solid #bae6fd;
        border-radius: 12px;
        padding: .9rem;
        background: #f8fafc;
        color: #0f172a;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <h1>ResAI Campus</h1>
      <p>AI career copilot for resumes, interviews, and job targeting.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


def api_call(path: str, files: Dict, data: Optional[Dict] = None):
    url = f"{BACKEND_URL}{path}"
    response = requests.post(url, files=files, data=data or {}, timeout=180)
    if response.status_code >= 400:
        raise RuntimeError(f"{response.status_code}: {response.text}")
    return response.json()


with st.sidebar:
    st.markdown("### Settings")
    st.caption(f"Backend: {BACKEND_URL}")
    if st.button("Check API Health"):
        try:
            status = requests.get(f"{BACKEND_URL}/health", timeout=15).json()
            st.success(f"API OK | model: {status.get('model')}")
        except Exception as exc:
            st.error(f"Health check failed: {exc}")

    mode = st.radio(
        "Choose Tool",
        [
            "Resume Analysis",
            "Resume Optimizer",
            "Cover Letter",
            "Interview Prep",
            "Market Position",
            "Skill Plan",
            "Job Search",
        ],
    )

left, right = st.columns([1, 1])

with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    job_description = st.text_area("Job Description", height=220)
    resume = st.file_uploader("Upload resume (PDF)", type=["pdf"])
    company_name = st.text_input("Company (for cover letter)")
    hiring_manager = st.text_input("Hiring Manager (optional)")
    focus = st.text_input("Cover letter focus (comma-separated)")
    job_count = st.slider("Job results", 1, 10, 5)
    run = st.button("Run", type="primary", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Output")

    if run:
        if not resume or not job_description.strip():
            st.warning("Please upload a resume and add a job description.")
        else:
            file_payload = {
                "resume": (resume.name, resume.getvalue(), "application/pdf"),
            }
            with st.spinner("Generating..."):
                try:
                    if mode == "Resume Analysis":
                        out = api_call(
                            "/api/resume/analyze",
                            files=file_payload,
                            data={"job_description": job_description},
                        )
                        pct = float(out.get("match_percentage", 0))
                        st.metric("Resume Match", f"{pct:.1f}%")
                        st.progress(min(max(int(round(pct)), 0), 100))
                        st.markdown(f'<div class="result">{out["analysis"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)

                    elif mode == "Resume Optimizer":
                        out = api_call(
                            "/api/resume/optimize",
                            files=file_payload,
                            data={"job_description": job_description},
                        )
                        st.markdown("#### Suggestions")
                        st.markdown(f'<div class="result">{out["suggestions"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                        st.markdown("#### Target Keywords")
                        st.write(out.get("keywords", []))

                    elif mode == "Cover Letter":
                        out = api_call(
                            "/api/cover-letter",
                            files=file_payload,
                            data={
                                "job_description": job_description,
                                "company_name": company_name or "Company",
                                "hiring_manager": hiring_manager or "Hiring Manager",
                                "focus_areas": focus or "balanced",
                            },
                        )
                        content = out["content"]
                        st.markdown(f'<div class="result">{content.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                        st.download_button("Download cover letter", data=content, file_name="cover_letter.txt", mime="text/plain")

                    elif mode == "Interview Prep":
                        out = api_call(
                            "/api/interview-prep",
                            files=file_payload,
                            data={"job_description": job_description},
                        )
                        st.markdown(f'<div class="result">{out["content"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)

                    elif mode == "Market Position":
                        out = api_call(
                            "/api/market-position",
                            files=file_payload,
                            data={"job_description": job_description},
                        )
                        st.markdown(f'<div class="result">{out["content"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)

                    elif mode == "Skill Plan":
                        out = api_call(
                            "/api/skill-plan",
                            files=file_payload,
                            data={"job_description": job_description},
                        )
                        st.markdown(f'<div class="result">{out["content"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)

                    elif mode == "Job Search":
                        out = api_call(
                            "/api/jobs/search",
                            files=file_payload,
                            data={"job_description": job_description, "count": str(job_count)},
                        )
                        st.markdown(out["results_markdown"])

                except Exception as exc:
                    st.error(f"Request failed: {exc}")
    else:
        st.info("Upload a resume + job description, choose a tool, then click Run.")

    st.markdown("</div>", unsafe_allow_html=True)
