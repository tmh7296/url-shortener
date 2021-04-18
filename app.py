import os
from flask import Flask, request
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from models import Url, db

### Config
app = Flask(__name__)

db_username = os.environ['POSTGRES_USER']
db_password = os.environ['POSTGRES_PASSWORD']
db_host     = os.environ['POSTGRES_HOST']
db_port     = os.environ['POSTGRES_PORT']
db_name     = os.environ['POSTGRES_DB']

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{}:{}@{}:{}/{}".format(db_username, db_password, db_host, db_port, db_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db.init_app(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

### Endpoints
@app.route('/shorten', methods=['POST'])
def createShortenedUrl():
    data = request.get_json(force=True)
    slug = data['slug']
    url = data['url']
    new_url = Url(slug=slug, url=url)
    db.session.add(new_url)
    db.session.commit()
    return request.data
