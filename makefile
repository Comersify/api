PHONY: run

run:
	python manage.py runserver

migrate:
	python manage.py migrate

migration:
	python manage.py makemigrations
