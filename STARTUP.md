*Virtual Environment*
- Create python environment with Ctrl + Shift + P
- Select Python:Create Environment
- Choose venv
- Set the folder name to .venv
- Choose Install project dependencies
- Select requirements.txt

*Environment variables:*
- Copy `.env.example` to `.env` and fill in your local values
- add `.env` and `.env.local` to `.gitignore`

*VS Code Tasks:*
- Copy `.vscode.example` to `.vscode` and fill in your local values
- add `.vscode` to `.gitignore`

- Run task: Terminal → Run Task 
    → Run **Tests (pytest)**
    → Run **Backend (uvicorn)**
    → Run **Frontend (http.server)**

*or use commands*

# tests
```bash
pytest -v
```

# backend
```bash
python -m uvicorn backend.main:app --reload --port 8000
```

# frontend
```bash
python -m http.server 5500
```