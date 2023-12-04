@echo off

echo "##########################################################"
echo "###         SCRIPT TO INSTALL ALL REQUIREMENTS         ###"
echo "###                  WINDOWS VERSION                   ###"
echo "###                                                    ###"
echo "###           MADE WITH LOVE BY 'Luciousdev'           ###"
echo "###                   mika-linux.com                   ###"
echo "##########################################################"

REM Check if Git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] - Git is not installed. Installing Git...
    call winget install Git.Git
    echo [OK] - Git is successfully installed.

    REM Refresh environment variables
    call refreshenv
) else (
    echo [OK] - Git is already installed.
)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] - Python is not installed. Installing Python...
    start /b winget install python3
    echo [OK] - Python is successfully installed.
) else (
    echo [OK] - Python is already installed.
)


REM Check if Pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] - pip is not installed. Please install pip manually.
    exit /b 1
) else (
    echo [OK] - pip is already installed.
)

@REM Handling the scoop install
powershell -Command "Set-ExecutionPolicy RemoteSigned -scope CurrentUser"
powershell -Command "iwr -useb get.scoop.sh | iex"
echo [OK] - Scoop is successfully installed, or already present on users machine.

REM Install packages using Scoop
echo "installing bucket.."
call scoop bucket add extras

call refreshenv

echo "installing ani-cli and other packages."
REM Install additional packages
call scoop install aria2 ffmpeg fzf mpv wget ani-cli


REM Install packages from requirements.txt using Pip
if exist requirements.txt (
    echo [PROGRESS] - Installing Python packages from requirements.txt...

    REM Ask the user if they want to use the '--break-system-packages' argument
    set /p "arguments=Would you like to use the argument '--break-system-packages'? Note: this can cause major issues. [y/n]"
    if /i "%arguments%"=="y" (
        REM Install Python dependencies
        start /b pip install --break-system-packages -r requirements.txt || call :handle_error
    ) else (
        REM Install Python dependencies
        start /b pip install -r requirements.txt || call :handle_error pip
    )
) else (
    echo [ERROR] - requirements.txt not found.
    exit /b 1
)

echo [OK] - Installation of Python, Pip, and/or the needed packages was successful.

set /p "argument=Do you want to run the script now? [y/n]"
if /i "%argument%"=="y" (
    python script.py
) else (
    exit
)

pause