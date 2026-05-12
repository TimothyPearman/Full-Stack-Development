## Deployment Requirements

### Server choices and rationale
- Frontend: `python -m http.server 5500`.
- Backend: `uvicorn backend.main:app --reload --port 8000`.
- Database: local MySQL server, either from a Docker container or a local MySQL installation.

The frontend uses Python's HTTP server because this project is a static HTML/CSS/JS client and does not need a build step or framework-specific host. Uvicorn is used for the FastAPI backend because it is the standard ASGI server for development and local deployment. MySQL is used locally so the app can connect to the same schema used for development and assessment.

### Configuration files
- `.env.example`: holds the required environment variables for database URL, CORS, secret key, and app environment.
- `.env`: local copy of the example file with your real values.
- `.vscode/tasks.json`: tasks for running the backend, frontend, and tests.
- `.vscode/launch.json`: debug configuration for the backend.
- `backend/Database.sql`: schema and seed script for MySQL.

### Environment variables
- Copy `.env.example` to `.env`.
- Set either `DATABASE_URL_HOME` or `DATABASE_URL_LAB`, or fill in `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, and `DB_NAME`.
- Set `SECRET_KEY` to a secure value.
- Set `CORS_ORIGINS` to `http://127.0.0.1:5500,http://localhost:5500`.
- Set `CORS_METHODS` and `CORS_HEADERS` to match the frontend requests.
- Set `APP_ENV=development` for local use.

### Local setup
1. Create the virtual environment.
    - Use **Ctrl + Shift + P** → **Python: Create Environment**.
    - Choose `venv` and create it in `.venv`.
    - Install dependencies from `requirements.txt`.
2. Start the local MySQL server.
    - Run a MySQL Docker container or start the local MySQL service.
3. Seed the database.
    - Open MySQL Workbench.
    - Connect to the local MySQL instance.
    - Open `backend/Database.sql` and execute it.
4. Start the backend.
    - Run the VS Code task **Run Backend (uvicorn)**.
    - Or use:

```bash
python -m uvicorn backend.main:app --reload --port 8000
```

5. Start the frontend.
    - Run the VS Code task **Run Frontend (http.server)**.
    - Or use:

```bash
python -m http.server 5500
```

### Port settings
- Frontend: `5500`
- Backend: `8000`
- MySQL: `3306`