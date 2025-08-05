@echo off
echo ===============================================
echo     CRIANDO EXECUTAVEL DO MY EXAM GAME
echo ===============================================
echo.

echo Limpando builds anteriores...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

echo.
echo Criando executavel...
pyinstaller build_game.spec

echo.
echo ===============================================
if exist "dist\MyExamGame.exe" (
    echo     SUCESSO! Executavel criado em:
    echo     dist\MyExamGame.exe
    echo.
    echo     Tamanho do arquivo:
    dir "dist\MyExamGame.exe" | find "MyExamGame.exe"
    echo.
    echo     Para testar, execute:
    echo     dist\MyExamGame.exe
) else (
    echo     ERRO! Nao foi possivel criar o executavel.
    echo     Verifique os erros acima.
)
echo ===============================================
echo.
pause
