Write-Host "==> Stopping and removing all containers..." -ForegroundColor Cyan
$containers = docker ps -aq
if ($containers) {
    docker stop $containers
    docker rm -f $containers
    Write-Host "Containers removed successfully." -ForegroundColor Green
} else {
    Write-Host "No containers to stop or remove." -ForegroundColor Yellow
}

Write-Host "`n==> Removing unused images..." -ForegroundColor Cyan
$images = docker images -aq
if ($images) {
    docker rmi -f $images
    Write-Host "Images removed successfully." -ForegroundColor Green
} else {
    Write-Host "No images to remove." -ForegroundColor Yellow
}

Write-Host "`n==> Removing unused volumes..." -ForegroundColor Cyan
docker volume prune -f | Out-Null
Write-Host "Volumes removed." -ForegroundColor Green

Write-Host "`n==> Removing unused networks..." -ForegroundColor Cyan
docker network prune -f | Out-Null
Write-Host "Networks removed." -ForegroundColor Green

Write-Host "`n==> Building images with docker compose (no cache)..." -ForegroundColor Blue
docker-compose build --no-cache
Write-Host "Images built successfully." -ForegroundColor Green

Write-Host "`n==> Starting containers in detached mode..." -ForegroundColor Blue
docker-compose up -d
Write-Host "Containers started successfully." -ForegroundColor Green

Write-Host "`n==> Showing live logs of the backend..." -ForegroundColor Magenta
docker-compose logs -f backend
