@echo off
echo Setting up environment...

:: Check if .env exists
if not exist .env (
    echo Creating .env from .env.example...
    copy .env.example .env
    echo Please edit .env with your API keys!
)

:: Install modules
echo Installing dependencies...
pip install -r deploy/requirements.txt

:: Run the app
echo Starting Relationship Counseling AI...
python -m src.web.app
pause
