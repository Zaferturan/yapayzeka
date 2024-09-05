@echo off
cd /d %~dp0
call venv\Scripts\activate.bat
pip install jupyterlab
pip install notebook
cmd /k