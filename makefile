PHONY: run

docker-run:
	docker run api:v0.0

build:
	docker build  . -f DockerFile.dev -t api:v0.0

shell: 
	python manage.py shell

run:
	python manage.py runserver

migrate:
	python manage.py migrate

migration:
	python manage.py makemigrations

freeze:
	pip freeze > requirements.txt

merge:
	git checkout master && git merge develop

master-push:
	git checkout master && git push master master

dev-push:
	git checkout develop && git push develop develop

