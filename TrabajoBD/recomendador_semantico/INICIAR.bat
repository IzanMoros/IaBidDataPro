@echo off
REM ========================================
REM Script de Inicio Rapido
REM Proyecto 8: Recomendador Semantico
REM ========================================

echo.
echo ========================================
echo   RECOMENDADOR SEMANTICO DE PELICULAS
echo ========================================
echo.

REM Verificar si Python esta instalado
set PYTHON_CMD=python
python --version >nul 2>&1
if errorlevel 1 (
    py --version >nul 2>&1
    if errorlevel 1 (
        python3 --version >nul 2>&1
        if errorlevel 1 (
            echo [ERROR] Python no esta instalado o no esta en el PATH
            echo.
            echo Por favor, instala Python desde:
            echo https://www.python.org/downloads/
            echo.
            echo IMPORTANTE: Marca "Add Python to PATH" durante la instalacion
            echo.
            pause
            exit /b 1
        ) else (
            set PYTHON_CMD=python3
        )
    ) else (
        set PYTHON_CMD=py
    )
)

echo [OK] Python encontrado (%PYTHON_CMD%)
%PYTHON_CMD% --version
echo.

REM Verificar si existe el entorno virtual
if not exist "venv\" (
    echo [INFO] Creando entorno virtual...
    %PYTHON_CMD% -m venv venv
    if errorlevel 1 (
        echo [ERROR] No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
    echo [OK] Entorno virtual creado
    echo.
)

REM Activar entorno virtual
echo [INFO] Activando entorno virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] No se pudo activar el entorno virtual
    pause
    exit /b 1
)
echo [OK] Entorno virtual activado
echo.

REM Verificar si las dependencias estan instaladas
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo [INFO] Instalando dependencias...
    echo [NOTA] Esto puede tardar varios minutos en la primera ejecucion
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Fallo la instalacion de dependencias
        pause
        exit /b 1
    )
    echo.
    echo [OK] Dependencias instaladas correctamente
    echo.
) else (
    echo [OK] Dependencias ya instaladas
    echo.
)

REM Preguntar que hacer
echo ========================================
echo   QUE DESEAS HACER?
echo ========================================
echo.
echo 1. Ejecutar la aplicacion Streamlit
echo 2. Ejecutar el script de prueba
echo 3. Salir
echo.
set /p opcion="Elige una opcion (1-3): "

if "%opcion%"=="1" (
    echo.
    echo [INFO] Iniciando aplicacion Streamlit...
    echo [NOTA] Se abrira automaticamente en tu navegador
    echo [NOTA] La primera ejecucion descargara el modelo multilingue avanzado (~470MB)
    echo [NOTA] Presiona Ctrl+C para detener el servidor
    echo.
    streamlit run app.py
) else if "%opcion%"=="2" (
    echo.
    echo [INFO] Ejecutando script de prueba...
    echo.
    %PYTHON_CMD% test_sistema.py
    echo.
    pause
) else if "%opcion%"=="3" (
    echo.
    echo Hasta luego!
    exit /b 0
) else (
    echo.
    echo [ERROR] Opcion invalida
    pause
    exit /b 1
)
