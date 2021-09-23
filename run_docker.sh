echo Killing old Docker processes
docker-compose rm -fs

echo Starting Docker containers
docker-compose up -d core
docker-compose up -d backend-app
docker-compose up -d frontend-app
docker-compose up -d reddit-stream