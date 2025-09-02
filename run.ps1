Write-Host "==> Limpiando contenedores detenidos..." -ForegroundColor Cyan
docker container prune -f

Write-Host "==> Construyendo imágenes con Docker Compose..." -ForegroundColor Cyan
docker-compose build

Write-Host "==> Levantando contenedores en segundo plano..." -ForegroundColor Cyan
docker-compose up -d

Write-Host "==> Logs en vivo del backend..." -ForegroundColor Yellow
docker-compose logs -f