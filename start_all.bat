
@echo off
REM Start backend in new window
start cmd /k "cd %~dp0\backend && python -m venv venv && .\venv\Scripts\Activate.ps1 && pip install -r requirements.txt && python models.py && python seed_admin.py && python seed_demo.py && python app.py"
REM Start frontend in new window
start cmd /k "cd %~dp0\frontend && npm install && npm start"
echo Started backend and frontend.
