# Python-scaffolding
Scaffolding for a python/flask project with docker + postgresql + SQLAlchemy

# Starting the app
## Prerequisites
* Docker is installed
* Docker compose is installed

To build and run the app, execute the command: \
`docker-compose up --build`

# Creating DB migrations
## Prerequisites
* Python3, Docker, Docker-compose are installed
* Python dependencies are installed - to install execute the following:
```
pip3 install -r requirements.txt
```
* Creating the migrations requires several environment variables to be set on the host system. They are as follows:
```
POSTGRES_USER=local
POSTGRES_PASSWORD=123456
POSTGRES_DB=localdb
POSTGRES_HOST=0.0.0.0
POSTGRES_PORT=5432
FLASK_APP=app.py
```
## Running the migrations
The DB needs to be running in the docker container. To run the DB:
```
docker-compose up db
```
Finally, to create the migrations, with the DB running in a separate terminal instance, execute the following:
```
python3 run.py db init
python3 run.py db migrate
python3 run.py db upgrade
```
