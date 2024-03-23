export PYTHONDONTWRITEBYTECODE=1
sudo chmod -R 777 ./
find ./ | grep -E "(\.coverage|\.pytest_cache|__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

docker rm -f $(docker ps -a -q)
docker volume rm $(docker volume ls -q)
docker-compose up --build

sudo chmod -R 777 ./
find ./ | grep -E "(\.coverage|\.pytest_cache|__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
