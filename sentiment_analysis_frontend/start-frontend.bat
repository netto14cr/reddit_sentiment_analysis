@echo off
REM Check if the node_modules folder exists
if exist node_modules (
    echo Dependencies already installed.
) else (
    echo Installing dependencies...
    npm install
)

REM Start the development server
npm start

REM Keep the window open to view logs (optional)
pause