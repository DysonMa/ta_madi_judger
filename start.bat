@echo off
cmd /k "python -m venv venv & call venv\Scripts\activate & set FLASK_APP=app.py & set FLASK_ENV=development &  flask run"