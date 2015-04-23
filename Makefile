.PHONY: clean

help:
	    @echo "  clean      remove unwanted stuff"
	    @echo "  install    install the dependencies"
	    @echo "  run        run the development server"

clean:
	    find . -name '*.pyc' -exec rm -f {} +
	    find . -name '*.pyo' -exec rm -f {} +
	    find . -name '*~' -exec rm -f {} +
	    find . -name '__pycache__' -exec rm -rf {} +

run:
	    python manage.py runserver

install:
	    pip install -r requirements.txt
