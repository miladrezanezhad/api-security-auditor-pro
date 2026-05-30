@echo off
REM install.bat - نصب خودکار در Windows

echo Installing API Security Auditor Pro...

REM بررسی نصب پایتون
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found! Please install Python 3.11 or higher.
    exit /b 1
)

REM ایجاد محیط مجازی
echo Creating virtual environment...
python -m venv venv

REM فعالسازی محیط مجازی
call venv\Scripts\activate.bat

REM آپگرید pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM نصب وابستگی‌ها
echo Installing dependencies...
pip install -r requirements.txt

REM نصب پکیج
echo Installing package...
pip install -e .

echo Installation complete!
echo.
echo To activate the environment:
echo    venv\Scripts\activate
echo.
echo To run the tool:
echo    api-auditor --help