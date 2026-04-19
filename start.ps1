# start.ps1 - Arranca todo el proyecto CEFUSA E-Commerce
# Uso: .\start.ps1
# Para detener todo: .\stop.ps1

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  CEFUSA E-Commerce - Iniciando..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$ROOT = (Get-Location).Path

# 1. Django (monolito legacy)
Write-Host "[1/4] Iniciando Django en :8000..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", `
    "cd '$ROOT'; Write-Host 'DJANGO :8000' -ForegroundColor Green; venv\Scripts\python CEFUSAECommerce\manage.py runserver"

Start-Sleep 2

# 2. Flask (microservicio pagos)
Write-Host "[2/4] Iniciando Flask en :5000..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", `
    "cd '$ROOT'; Write-Host 'FLASK :5000' -ForegroundColor Magenta; venv\Scripts\python flask_payment_service\app.py"

Start-Sleep 2

# 3. Nginx (orquestador de trafico)
Write-Host "[3/4] Iniciando Nginx en :80..." -ForegroundColor Yellow
Set-Location "$ROOT\nginx-1.27.4"
Start-Process ".\nginx.exe"
Set-Location $ROOT

Start-Sleep 1

# 4. Frontend (React/Vite)
Write-Host "[4/4] Iniciando Frontend React (Vite)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", `
    "cd '$ROOT\frontend'; Write-Host 'FRONTEND' -ForegroundColor Cyan; npm run dev"

Start-Sleep 2

# Verificacion rapida
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Todo corriendo. Verificando..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Django (legacy)  ->  http://localhost:8000/api/products/" -ForegroundColor White
Write-Host "  Flask  (pagos)   ->  http://localhost:5000/health" -ForegroundColor White
Write-Host "  Nginx  (router)  ->  http://localhost/api/products/" -ForegroundColor White
Write-Host "                       http://localhost/api/v2/checkout/" -ForegroundColor White
Write-Host "  Frontend (React) ->  http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "  Para detener todo: .\stop.ps1" -ForegroundColor Red
Write-Host ""
