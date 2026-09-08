@echo off

start cmd /k "python -m uvicorn backend:app --host 127.0.0.1 --port 8000"
timeout /t 3
start cmd /k "python -m streamlit run streamlit_app.py --server.port 8501"

start http://localhost:8501