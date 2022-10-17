# pyrobots-backend

## iniciar

- python3 -m venv env
- source env/bin/activate
- pip3 install -r requirements.txt
- uvicorn main:app --reload --port 8000

## clear

- pip freeze > requirements.txt
- pip uninstall -r requirements.txt -y
- deactivate
- rm -r env/
- rm -rf \__pycache\__

## pre-commit pep8 check
```
echo -e '#!/bin/sh\nflake8 . --exclude .git,__pycache__,env --ignore=F403,F405' > .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
pip3 install flake8
```

## Registro de Usuario

- pip install python-dotenv

## crear un test

- en la carpeta tests crear un archivo test_`<nombre del archivo a testear>`.py
- agregar a requirements.txt
	- pip3 install requests
	- pip3 install pytest
	- pip3 install coverage
- para correr el test hacer `coverage run -m pytest` desde la carpeta principal
- para ver el informe hacer `coverage report -m`

