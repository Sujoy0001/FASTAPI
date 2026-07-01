@echo off
set PROJECT_ROOT=D:\FASTAPI\server-Frontend

if exist "C:\nginx\nginx.exe" (
    set NGINX_EXE=C:\nginx\nginx.exe
) else if exist "C:\Program Files\nginx\nginx.exe" (
    set NGINX_EXE=C:\Program Files\nginx\nginx.exe
) else if exist "C:\Program Files (x86)\nginx\nginx.exe" (
    set NGINX_EXE=C:\Program Files (x86)\nginx\nginx.exe
) else (
    echo Nginx was not found. Install it and re-run this script.
    exit /b 1
)

start "FastAPI" "%PROJECT_ROOT%\.venv\Scripts\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8000
start "Nginx" "%NGINX_EXE%" -c "%PROJECT_ROOT%\nginx\nginx.conf"

echo Started FastAPI and Nginx.
echo Open http://localhost
