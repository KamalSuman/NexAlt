@echo off
REM Initialize Git repository

git init

REM Add all files
git add .

REM Create initial commit
git commit -m "Initial commit"

REM Instructions for adding a remote repository
echo.
echo Repository initialized successfully!
echo.
echo To push to GitHub, run the following commands:
echo   git remote add origin https://github.com/yourusername/investment-portfolio-allocation.git
echo   git branch -M main
echo   git push -u origin main
echo.
echo Replace 'yourusername' with your GitHub username.

pause