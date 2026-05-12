1. *start database server*
- run MySQL docker container

2. *seed database*
- open **MySQLWorkbench**
- select **local MySQL connection**
- open **File → Open SQL Script → Project → backend → Database.sql**
- execute script

3. *start backend*
- Run task: Terminal → Run Task → Run **Backend (uvicorn)**

or

```bash
python -m uvicorn backend.main:app --reload --port 8000
```

4. *start frontend*
- Run task: Terminal → Run Task → Run **Frontend (http.server)**

or

```bash
python -m http.server 5500
```

5. *visit web pages*
- open **http://127.0.0.1:5500/index.html#info**
- open **http://127.0.0.1:8000/docs#/**

### Startup procedure
1. Start MySQL first.
2. Ensure `.env` is present and contains valid values.
3. Start the backend on port `8000`.
4. Start the frontend on port `5500`.
5. Open `http://127.0.0.1:5500/index.html#info`.
6. Open `http://127.0.0.1:8000/docs` to confirm the API is running.

### Shutdown procedure
1. Stop the frontend server with `Ctrl+C` in the terminal running `http.server`.
2. Stop the backend server with `Ctrl+C` in the Uvicorn terminal.
3. Stop the MySQL Docker container or MySQL service.
