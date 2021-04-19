import os
import uuid

from exceptions import BadRequest
from flask import Flask, request, Response, jsonify, redirect, abort,json
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from models import ShortenedUrl, db
from utils import validateRequestBody

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
@app.route('/shortened_url', methods=['POST'])
def createShortenedUrl():
    """
    Endpoint that accepts a URL and an optional slug and return a shortened version
    """
    data = request.get_json(force=True)

    # checking the validity of the request body
    if not validateRequestBody(data):
        raise BadRequest('Request payload is malformed')

    # validate the provided slug is not in use
    if 'slug' in data:
        slug = data['slug']
        if ShortenedUrl.query.get(slug) != None:
            raise BadRequest('Slug is not unique')
    else:
        slug = uuid.uuid4().hex[:6].lower()
        # validate the generated slug is not in use
        while ShortenedUrl.query.get(slug) != None:
            slug = uuid.uuid4().hex[:6].lower()

    url = data['url']
    response = Response()
    returnObj = {
        'url': url,
        'slug': slug,
        'shortened_url': '{}r/{}'.format(request.url_root, slug)
    }
    response.headers['location'] = '/r/{}'.format(slug)
    response.headers['Content-Type'] = 'application/json'
    response.status_code = 201
    response.data = json.dumps(returnObj)

    # create object and write to db
    shortenedUrl = ShortenedUrl(slug=slug, url=url)

    db.session.add(shortenedUrl)
    db.session.commit()

    return response

@app.route('/r/<slug>', methods=['GET'])
def redirectToOriginalUrl(slug):
    """
    Endpoint that takes a slug as a path param and redirects the user to the original URL associated with the slug

    After re-reading the spec sheet, I think it would've been more accurate to have the GET return the original URL
    in the response rather than redirecting the user. This endpoint is meant to be used in the browser. 
    """
    url = ShortenedUrl.query.get(slug)
    if url != None:
        return redirect(url.url, code=302)
    abort(404)


### Error handling
@app.errorhandler(BadRequest)
def handle_bad_request(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
