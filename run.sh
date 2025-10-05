#!/bin/bash

# Colors
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${CYAN}==> Stopping and removing all containers...${NC}"
containers=$(docker ps -aq)
if [ -n "$containers" ]; then
    docker stop $containers >/dev/null
    docker rm -f $containers >/dev/null
    echo -e "${GREEN}Containers removed successfully.${NC}"
else
    echo -e "${YELLOW}No containers to stop or remove.${NC}"
fi

echo -e "\n${CYAN}==> Removing unused images...${NC}"
images=$(docker images -aq)
if [ -n "$images" ]; then
    docker rmi -f $images >/dev/null
    echo -e "${GREEN}Images removed successfully.${NC}"
else
    echo -e "${YELLOW}No images to remove.${NC}"
fi

echo -e "\n${CYAN}==> Removing unused volumes...${NC}"
docker volume prune -f >/dev/null
echo -e "${GREEN}Volumes removed.${NC}"

echo -e "\n${CYAN}==> Removing unused networks...${NC}"
docker network prune -f >/dev/null
echo -e "${GREEN}Networks removed.${NC}"

echo -e "\n${BLUE}==> Building images with docker compose (no cache)...${NC}"
docker compose build --no-cache
echo -e "${GREEN}Images built successfully.${NC}"

echo -e "\n${BLUE}==> Starting containers in detached mode...${NC}"
docker compose up -d
echo -e "${GREEN}Containers started successfully.${NC}"

echo -e "\n${MAGENTA}==> Showing live logs of the backend...${NC}"
docker compose logs -f backend
