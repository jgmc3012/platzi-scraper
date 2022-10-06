title="platzi-scraper - Localhost"

echo "$title"
docker network create --driver=bridge scraper-proxy-net
docker-compose -f docker-compose.yml -f docker-compose.local.yml $@
