# stop.ps1 - Detiene todo el proyecto CEFUSA E-Commerce
# Uso: .\stop.ps1

Write-Host ""
Write-Host "Deteniendo servicios..." -ForegroundColor Red

# Detener Nginx
$nginxDir = Join-Path (Get-Location).Path "nginx-1.27.4"
if (Test-Path "$nginxDir\nginx.exe") {
    Start-Process "$nginxDir\nginx.exe" -ArgumentList "-s", "stop" -WorkingDirectory $nginxDir -Wait -NoNewWindow 2>$null
    Write-Host "  [OK] Nginx detenido" -ForegroundColor Green
} elseif (Get-Command nginx -ErrorAction SilentlyContinue) {
    nginx -s stop 2>$null
    Write-Host "  [OK] Nginx detenido" -ForegroundColor Green
} else {
    Write-Host "  [--] Nginx no estaba corriendo" -ForegroundColor DarkGray
}

# Detener procesos Python (Django y Flask)
Get-Process -Name "python" -ErrorAction SilentlyContinue | Stop-Process -Force
Write-Host "  [OK] Django y Flask detenidos" -ForegroundColor Green

Write-Host ""
Write-Host "Todos los servicios detenidos." -ForegroundColor Cyan
Write-Host ""
