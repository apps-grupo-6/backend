echo "==> Deteniendo y eliminando todos los contenedores..."
docker stop $(docker ps -aq) 2>/dev/null
docker rm -f $(docker ps -aq) 2>/dev/null

echo "==> Eliminando imágenes sin usar..."
docker rmi -f $(docker images -aq) 2>/dev/null

echo "==> Eliminando volúmenes sin usar..."
docker volume prune -f

echo "==> Eliminando redes sin usar..."
docker network prune -f

echo "==> Construyendo imágenes con Docker Compose (sin caché)..."
docker-compose build --no-cache

echo "==> Levantando contenedores en segundo plano..."
docker-compose up -d

echo "==> Logs en vivo del backend..."
docker-compose logs -f backend
