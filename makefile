PHONY: run

shell: 
	python manage.py shell

run:
	python manage.py runserver

migrate:
	python manage.py migrate

migration:
	python manage.py makemigrations
