# ResAI Frontend (Streamlit)

## What it does
Campus-facing UI for students. Calls the backend API.

## Run locally
```bash
cd frontend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
export BACKEND_URL=http://localhost:8000
streamlit run app.py
```

## Deploy (Streamlit Community Cloud)
1. Push this frontend folder to a GitHub repo.
2. In Streamlit Cloud, select repo + branch.
3. App file path: `app.py`.
4. Add secret: `BACKEND_URL` = your deployed backend URL.
