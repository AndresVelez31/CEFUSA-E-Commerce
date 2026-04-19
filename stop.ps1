# stop.ps1 - Detiene todo el proyecto CEFUSA E-Commerce
# Uso: .\stop.ps1

Write-Host ""
Write-Host "Deteniendo servicios..." -ForegroundColor Red

# Detener Nginx
$nginxDir = Join-Path (Get-Location).Path "nginx-1.27.4"
if (Test-Path "$nginxDir\nginx.exe") {
    Set-Location $nginxDir
    .\nginx.exe -s stop 2>$null
    Set-Location (Get-Location).Path
    Write-Host "  [OK] Nginx detenido" -ForegroundColor Green
}

# Detener procesos Python (Django y Flask)
Get-Process -Name "python" -ErrorAction SilentlyContinue | Stop-Process -Force
Write-Host "  [OK] Django y Flask detenidos" -ForegroundColor Green

Write-Host ""
Write-Host "Todos los servicios detenidos." -ForegroundColor Cyan
Write-Host ""
