@echo off
title Instalador e Inicializador do Jogo

:: Limpa a tela
cls

echo ===================================================
echo  Instalador e Inicializador do Jogo
echo ===================================================
echo.

:: 1. Instalar dependencias
echo Verificando e instalando a biblioteca Pygame...
pip install pygame

:: Verifica se a instalacao foi bem-sucedida
if %errorlevel% neq 0 (
    echo.
    echo ---------------------------------------------------
    echo  ERRO: Nao foi possivel instalar o Pygame.
    echo  Verifique se o Python e o pip estao instalados
    echo  e configurados corretamente no PATH do sistema.
    echo ---------------------------------------------------
    echo.
    pause
    exit /b
)

echo.
echo Biblioteca Pygame instalada com sucesso!
echo.
echo ===================================================
echo.

:: 2. Iniciar o jogo
echo Iniciando o jogo... Pressione qualquer tecla para continuar.
pause >nul
python core.py

echo.
echo Jogo finalizado.
pause
