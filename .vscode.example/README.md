Sanitized example VS Code settings.

Copy files from this folder into `.vscode/` and update interpreter paths if needed.

- `launch.json`: launch configuration for the backend (uses `${workspaceFolder}`)
- `launch.json`: launch configurations for the backend and pytest (uses `${workspaceFolder}`)
- `tasks.json`: tasks to run uvicorn and pytest. They use `${command:python.interpreterPath}` so VS Code will pick the selected interpreter.
- `extensions.json`: recommended extensions.
