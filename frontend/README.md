# Grant Platform (Complete)

This folder matches your requested structure and includes:

- backend/main.py (FastAPI)
- frontend/ (Vue 3 + Vite)

## Backend (local)
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

## Frontend (local)
cd frontend
npm install
npm run dev

## Deploy notes
- Backend uses DATABASE_URL env var (Render provides it).
- Frontend calls https://grant-app-backend.onrender.com by default.
