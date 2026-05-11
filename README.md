# CMP2812-2526_Assessment-3

Development notes

Environment variables

- Copy `.env.example` to `.env` and fill in your local values.
- `.env` and `.env.local` are ignored by git (see `.gitignore`).

Quick start (venv activated):

```bash
python -m uvicorn backend.main:app --reload --port 8000
```

Or use the VS Code task: **Run Task → Run Backend (uvicorn)**
