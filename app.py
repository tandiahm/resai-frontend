import os
from typing import Dict, Optional

import matplotlib.pyplot as plt
import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")

st.set_page_config(page_title="ResAI Campus", layout="wide")

st.markdown(
    """
    <style>
      :root {
        --ink: #0f172a; --muted: #334155; --brand: #0ea5e9;
        --brand-2: #14b8a6; --line: #dbeafe;
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
        box-shadow: 0 12px 30px rgba(2,132,199,.08);
        margin-bottom: 1.4rem;
      }
      .hero h1 { margin: 0; font-size: 2rem; color: var(--ink); }
      .hero p  { margin: .35rem 0 0; color: var(--muted); }
      .panel {
        padding: 1.2rem;
        border-radius: 14px;
        border: 1px solid #dbeafe;
        background: #ffffff;
        box-shadow: 0 6px 24px rgba(15,23,42,.05);
      }
      /* Make column buttons look like tool cards */
      [data-testid="column"] .stButton > button {
        border-radius: 12px;
        padding: .65rem .4rem;
        font-size: .78rem;
        font-weight: 600;
        line-height: 1.35;
        white-space: pre-wrap;
        border: 2px solid #dbeafe;
        background: #ffffff;
        color: #0f172a;
        box-shadow: 0 2px 6px rgba(15,23,42,.04);
        transition: all .15s;
      }
      [data-testid="column"] .stButton > button:hover {
        border-color: #0ea5e9;
        background: #f0f9ff;
        transform: translateY(-1px);
        box-shadow: 0 4px 14px rgba(14,165,233,.14);
      }
      [data-testid="column"] .stButton > button[kind="primary"] {
        border-color: #0ea5e9;
        background: linear-gradient(135deg, #f0f9ff, #ecfeff);
        box-shadow: 0 4px 14px rgba(14,165,233,.18);
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <h1>ResAI Campus</h1>
      <p>AI career copilot — resume, interviews, and job targeting in one place.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------------------------

TOOLS = [
    {"id": "Resume Analysis",  "icon": "📊", "desc": "Match score + recruiter feedback"},
    {"id": "Resume Optimizer", "icon": "✨", "desc": "Bullet-point resume improvements"},
    {"id": "Cover Letter",     "icon": "✉️",  "desc": "Tailored 300-400 word letter"},
    {"id": "Interview Prep",   "icon": "🎯", "desc": "Technical & behavioral questions"},
    {"id": "Market Position",  "icon": "📈", "desc": "Rank vs. the ideal candidate"},
    {"id": "Skill Plan",       "icon": "🗺️",  "desc": "3-month learning roadmap"},
    {"id": "Job Search",       "icon": "🔍", "desc": "Live listings matched to you"},
]

if "mode" not in st.session_state:
    st.session_state.mode = "Resume Analysis"

# ---------------------------------------------------------------------------
# Tool card grid
# ---------------------------------------------------------------------------

cols = st.columns(7)
for i, tool in enumerate(TOOLS):
    with cols[i]:
        btn_type = "primary" if st.session_state.mode == tool["id"] else "secondary"
        label = f"{tool['icon']}\n{tool['id']}"
        if st.button(label, key=f"tool_{i}", type=btn_type, use_container_width=True):
            st.session_state.mode = tool["id"]
            st.rerun()
        st.caption(tool["desc"])

mode = st.session_state.mode
current_tool = next(t for t in TOOLS if t["id"] == mode)

# ---------------------------------------------------------------------------
# Sidebar — health check only
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown("### Settings")
    st.caption(f"Backend: `{BACKEND_URL}`")
    if st.button("Check API Health"):
        try:
            status = requests.get(f"{BACKEND_URL}/health", timeout=15).json()
            st.success(f"API OK — model: {status.get('model')}")
        except Exception as exc:
            st.error(f"Health check failed: {exc}")

# ---------------------------------------------------------------------------
# API helper
# ---------------------------------------------------------------------------

def api_call(path: str, files: Dict, data: Optional[Dict] = None):
    url = f"{BACKEND_URL}{path}"
    response = requests.post(url, files=files, data=data or {}, timeout=180)
    if response.status_code >= 400:
        raise RuntimeError(f"{response.status_code}: {response.text}")
    return response.json()

# ---------------------------------------------------------------------------
# Main layout
# ---------------------------------------------------------------------------

left, right = st.columns([1, 1])

with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    job_description = st.text_area("Job Description", height=220)
    resume = st.file_uploader("Upload resume (PDF)", type=["pdf"])

    # Conditional fields
    company_name = hiring_manager = focus = ""
    if mode == "Cover Letter":
        company_name    = st.text_input("Company name")
        hiring_manager  = st.text_input("Hiring Manager (optional)")
        focus           = st.text_input("Focus areas (comma-separated)")

    job_count = 5
    if mode == "Job Search":
        job_count = st.slider("Number of results", 1, 10, 5)

    run = st.button("Run", type="primary", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader(f"{current_tool['icon']}  {mode}")

    if run:
        if not resume or not job_description.strip():
            st.warning("Please upload a resume and enter a job description.")
        else:
            file_payload = {"resume": (resume.name, resume.getvalue(), "application/pdf")}

            with st.spinner("Generating..."):
                try:
                    if mode == "Resume Analysis":
                        out = api_call(
                            "/api/resume/analyze",
                            files=file_payload,
                            data={"job_description": job_description},
                        )
                        pct = float(out.get("match_percentage", 0))
                        fig, ax = plt.subplots(figsize=(3.2, 3.2))
                        ax.pie(
                            [int(round(pct)), max(0, 100 - int(round(pct)))],
                            colors=["#0ea5e9", "#e2e8f0"],
                            startangle=90,
                            wedgeprops=dict(width=0.36, edgecolor="white"),
                        )
                        ax.text(0, 0, f"{pct:.1f}%", ha="center", va="center",
                                fontsize=22, fontweight="bold")
                        ax.axis("equal")
                        st.pyplot(fig)
                        st.markdown("---")
                        st.markdown(out["analysis"])

                    elif mode == "Resume Optimizer":
                        out = api_call(
                            "/api/resume/optimize",
                            files=file_payload,
                            data={"job_description": job_description},
                        )
                        st.markdown("#### Suggestions")
                        st.markdown(out["suggestions"])
                        st.markdown("#### Target Keywords")
                        st.write(out.get("keywords", []))

                    elif mode == "Cover Letter":
                        out = api_call(
                            "/api/cover-letter",
                            files=file_payload,
                            data={
                                "job_description":  job_description,
                                "company_name":     company_name or "Company",
                                "hiring_manager":   hiring_manager or "Hiring Manager",
                                "focus_areas":      focus or "balanced",
                            },
                        )
                        content = out["content"]
                        st.markdown(content)
                        st.download_button(
                            "Download cover letter",
                            data=content,
                            file_name="cover_letter.txt",
                            mime="text/plain",
                        )

                    elif mode == "Interview Prep":
                        out = api_call(
                            "/api/interview-prep",
                            files=file_payload,
                            data={"job_description": job_description},
                        )
                        st.markdown(out["content"])

                    elif mode == "Market Position":
                        out = api_call(
                            "/api/market-position",
                            files=file_payload,
                            data={"job_description": job_description},
                        )
                        st.markdown(out["content"])

                    elif mode == "Skill Plan":
                        out = api_call(
                            "/api/skill-plan",
                            files=file_payload,
                            data={"job_description": job_description},
                        )
                        st.markdown(out["content"])

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
        st.info("Upload a resume and job description, then click **Run**.")

    st.markdown("</div>", unsafe_allow_html=True)
