# Script para iniciar la aplicación Logistica
Write-Host "Iniciando aplicacion Logistica..." -ForegroundColor Green
Write-Host ""

# Activar entorno virtual
& .\.venv\Scripts\Activate.ps1

# Iniciar aplicación
python run.py
