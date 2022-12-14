# pyrobots-backend

## iniciar

```
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
python3 -m http.server --directory userUploads/ 9000
uvicorn main:app --reload --port 8000
```

## clear

```
pip freeze > requirements.txt
pip uninstall -r requirements.txt -y
deactivate
rm -r env/
rm -rf \__pycache\__
```

## pre-commit pep8 check

```
echo -e '#!/bin/sh\nflake8 . --exclude .git,__pycache__,env --ignore=F403,F405' > .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
pip3 install flake8
```

## testing

```
coverage run -m pytest && coverage report -m
```

