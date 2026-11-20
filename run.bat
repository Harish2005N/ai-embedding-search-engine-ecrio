@echo off
cd /d "%~dp0ai-embedding-search-engine-main" 2>nul || cd /d "%~dp0"
echo Starting AI Embedding Search Engine...
python run.py
pause
