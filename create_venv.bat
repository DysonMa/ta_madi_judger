@echo off
cmd /k "python -m venv venv & call venv\Scripts\activate & pip install -r requirements.txt & cd ./frontend/ & yarn install"