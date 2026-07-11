# GitNerd

GitNerd is an AI-powered repository learning and interview platform.

## Backend

Run the FastAPI backend from the project root:

```bash
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload
```

Backend endpoints:

- `GET /` - API status
- `GET /health` - backend health check

Interactive API docs are available at:

- `http://127.0.0.1:8000/docs`
