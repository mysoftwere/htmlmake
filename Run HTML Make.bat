@echo off
title HTML Make Software
cd /d "%~dp0"
python "HTML Make.py"
if %errorlevel% neq 0 (
    echo.
    echo Software encountered an issue or closed.
    pause
)
