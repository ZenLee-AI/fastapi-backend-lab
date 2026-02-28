# fastapi-backend-lab

FastAPI backend practice focused on observability, testing, reliability, and AI-ready patterns.

## Features (so far)
- `/health` endpoint
- Environment config via `.env` (see `.env.example`)

## Quickstart (Windows)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload