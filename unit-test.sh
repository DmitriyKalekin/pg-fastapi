# Стараемся не мусорить
export PYTHONDONTWRITEBYTECODE=1

# Есть где-то зависимость, которая убивает тесты без этой переменной
export JUPYTER_PLATFORM_DIRS=1

# Правильно читаем .env с комментариями и другими $-переменными
set -a            
source .env
set +a

# Нужно запускать из папки src
cd ./src && python3.12 -m pytest . -s -vv --cov="./app" --cov-report=term-missing --color=yes

# После запуска тестов удаляем __pycache__ и отчет о покрытии .coverage 
find . | grep -E "(\.pytest_cache|\.coverage|__pycache__|\.pyc|\.pyo$)" | xargs rm -rf


