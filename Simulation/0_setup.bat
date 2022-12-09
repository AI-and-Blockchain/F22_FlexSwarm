@REM Set up project
@REM 
@REM 

@REM Create virtual environment
python -m venv .venv

@REM Activate virtual environment
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted
.venv\Scripts\Activate.ps1

@REM Download required packages
pip install -r .\requirements.txt
