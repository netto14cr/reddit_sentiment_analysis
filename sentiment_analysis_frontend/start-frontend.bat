@echo off
REM Verifica si la carpeta node_modules existe
if exist node_modules (
    echo Dependencias ya instaladas.
) else (
    echo Instalando dependencias...
    npm install
)

REM Inicia el servidor de desarrollo
npm start

REM Mantiene la ventana abierta para ver los logs (opcional)
pause
