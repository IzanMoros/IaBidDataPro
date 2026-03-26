# ========================================
# Script de Inicio Rápido - PowerShell
# Proyecto 8: Recomendador Semántico
# ========================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  RECOMENDADOR SEMÁNTICO DE PELÍCULAS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si Python está instalado
$pythonCmd = "python"
try {
    $v = python --version 2>&1
    Write-Host "[OK] Python encontrado: $v" -ForegroundColor Green
} catch {
    try {
        $v = py --version 2>&1
        $pythonCmd = "py"
        Write-Host "[OK] Python encontrado vía 'py': $v" -ForegroundColor Green
    } catch {
        try {
            $v = python3 --version 2>&1
            $pythonCmd = "python3"
            Write-Host "[OK] Python encontrado vía 'python3': $v" -ForegroundColor Green
        } catch {
            Write-Host "[ERROR] Python no está instalado o no está en el PATH" -ForegroundColor Red
            Write-Host ""
            Write-Host "Por favor, instala Python desde:" -ForegroundColor Yellow
            Write-Host "https://www.python.org/downloads/" -ForegroundColor Yellow
            Write-Host ""
            Write-Host "IMPORTANTE: Marca 'Add Python to PATH' durante la instalación" -ForegroundColor Yellow
            Write-Host ""
            pause
            exit 1
        }
    }
}

Write-Host ""

# Verificar si existe el entorno virtual
if (-Not (Test-Path "venv")) {
    Write-Host "[INFO] Creando entorno virtual..." -ForegroundColor Yellow
    & $pythonCmd -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] No se pudo crear el entorno virtual" -ForegroundColor Red
        pause
        exit 1
    }
    Write-Host "[OK] Entorno virtual creado" -ForegroundColor Green
    Write-Host ""
}

# Activar entorno virtual
Write-Host "[INFO] Activando entorno virtual..." -ForegroundColor Yellow

# Verificar política de ejecución
$policy = Get-ExecutionPolicy -Scope CurrentUser
if ($policy -eq "Restricted") {
    Write-Host "[AVISO] La política de ejecución está restringida" -ForegroundColor Yellow
    Write-Host "Intentando cambiarla..." -ForegroundColor Yellow
    try {
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
        Write-Host "[OK] Política de ejecución actualizada" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] No se pudo cambiar la política de ejecución" -ForegroundColor Red
        Write-Host "Ejecuta PowerShell como administrador y ejecuta:" -ForegroundColor Yellow
        Write-Host "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
        pause
        exit 1
    }
}

# Activar venv
& .\venv\Scripts\Activate.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] No se pudo activar el entorno virtual" -ForegroundColor Red
    pause
    exit 1
}
Write-Host "[OK] Entorno virtual activado" -ForegroundColor Green
Write-Host ""

# Verificar si las dependencias están instaladas
$streamlitInstalled = pip show streamlit 2>&1 | Select-String "Name: streamlit"
if (-Not $streamlitInstalled) {
    Write-Host "[INFO] Instalando dependencias..." -ForegroundColor Yellow
    Write-Host "[NOTA] Esto puede tardar varios minutos en la primera ejecución" -ForegroundColor Cyan
    Write-Host ""
    
    pip install -r requirements.txt
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Falló la instalación de dependencias" -ForegroundColor Red
        pause
        exit 1
    }
    
    Write-Host ""
    Write-Host "[OK] Dependencias instaladas correctamente" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "[OK] Dependencias ya instaladas" -ForegroundColor Green
    Write-Host ""
}

# Menú de opciones
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ¿QUÉ DESEAS HACER?" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Ejecutar la aplicación Streamlit" -ForegroundColor White
Write-Host "2. Ejecutar el script de prueba" -ForegroundColor White
Write-Host "3. Salir" -ForegroundColor White
Write-Host ""

$opcion = Read-Host "Elige una opción (1-3)"

switch ($opcion) {
    "1" {
        Write-Host ""
        Write-Host "[INFO] Iniciando aplicación Streamlit..." -ForegroundColor Yellow
        Write-Host "[NOTA] Se abrirá automáticamente en tu navegador" -ForegroundColor Cyan
        Write-Host "[NOTA] La primera ejecución descargará el modelo multilingüe avanzado (~470MB)" -ForegroundColor Cyan
        Write-Host "[NOTA] Presiona Ctrl+C para detener el servidor" -ForegroundColor Cyan
        Write-Host ""
        streamlit run app.py
    }
    "2" {
        Write-Host ""
        Write-Host "[INFO] Ejecutando script de prueba..." -ForegroundColor Yellow
        Write-Host ""
        & $pythonCmd test_sistema.py
        Write-Host ""
        pause
    }
    "3" {
        Write-Host ""
        Write-Host "¡Hasta luego!" -ForegroundColor Green
        exit 0
    }
    default {
        Write-Host ""
        Write-Host "[ERROR] Opción inválida" -ForegroundColor Red
        pause
        exit 1
    }
}
