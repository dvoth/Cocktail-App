# Cocktail-App
## Setting up the server for Local React Native development
* open command prompt
* run `ipconfig`
* copy IPv4 Address
* add your IP address to ALLOWED_HOSTS in settings.py (but do not commit this to git)
* `python manage.py runserver $ip:8000`
* In the React Native `.env` file, change the `API_URL` to your ip address

## Nuking the migrations and database locally
* Delete `db.sqlite3`
* Delete migrations folder 
* `python manage.py makemigrations Cocktail_App`
* `python manage.py migrate`