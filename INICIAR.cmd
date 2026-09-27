@echo off
setlocal
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" goto dependencias
python -m venv .venv
if errorlevel 1 goto erro
:dependencias
".venv\Scripts\python.exe" -m pip install --disable-pip-version-check -r requirements.txt
if errorlevel 1 goto erro
if exist ".env" goto executar
".venv\Scripts\python.exe" configurar.py
if errorlevel 1 goto erro
:executar
echo.
echo Acesse http://127.0.0.1:5000 no navegador.
echo Mantenha esta janela aberta. Para encerrar, pressione Ctrl+C.
".venv\Scripts\python.exe" run.py
if errorlevel 1 goto erro
exit /b 0
:erro
echo.
echo Nao foi possivel iniciar. Confira a mensagem acima e o README.md.
pause
exit /b 1
