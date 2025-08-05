@echo off
echo ===============================================
echo        TESTANDO MY EXAM GAME EXECUTAVEL
echo ===============================================
echo.

if not exist "dist\MyExamGame.exe" (
    echo ERRO: Executavel nao encontrado!
    echo Execute primeiro: build_game.bat
    pause
    exit /b 1
)

echo Informacoes do executavel:
dir "dist\MyExamGame.exe"

echo.
echo Executando o jogo...
echo (Pressione Ctrl+C para fechar este terminal se necessario)
echo.

start "" "dist\MyExamGame.exe"

echo.
echo Jogo iniciado! Se abrir corretamente, esta pronto para distribuir.
echo.
pause
