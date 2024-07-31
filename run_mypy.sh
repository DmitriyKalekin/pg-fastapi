# python3.12 -m pip install mypy types-passlib
mypy src/app/domain/issues/ --strict | grep deps.py