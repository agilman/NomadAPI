# NomadAPI

## Build Setup

```bash
# Create a virtual environment:	
$ mkvirtualenv -p /usr/bin/python3 nomadapi

# Install required packages:
$ pip install -r requirements.txt

# Create db:
$ python manage.py migrate

# Run server:
$ python manage.py runserver
```