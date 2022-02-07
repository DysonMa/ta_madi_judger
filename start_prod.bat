@echo off
cmd /k "call venv\Scripts\activate & set FLASK_APP=app.py & set FLASK_ENV=production & flask run"