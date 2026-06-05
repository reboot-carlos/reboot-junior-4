@echo off
REM Démarrage du serveur NovAI pour Windows

echo 🤖 Démarrage de NovAI API...
echo.
echo Vérification de la clé API...

findstr /M "sk-ant-REMPLACE_MOI" .env >nul
if %ERRORLEVEL% == 0 (
    echo ⚠️  ERREUR: Clé API non configurée !
    echo.
    echo Édite .env et remplace:
    echo   ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE
    pause
    exit /b 1
)

echo ✅ Clé API configurée
echo.
echo 🚀 Lancement du serveur...
echo 📡 L'API sera disponible à: http://127.0.0.1:8000
echo 📚 Documentation: http://127.0.0.1:8000/docs
echo.
echo Ouvre index.html dans ton navigateur...
echo.

uvicorn main:app --reload
pause
