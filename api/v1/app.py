#!/usr/bin/python3
"""This is a flask app"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.url_map.strict_slashes = False
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def teardown_session(*args):
    storage.close()


if __name__ == '__main__':
    if getenv("HBNB_API_HOST") is None and getenv("HBNB_API_PORT") is None:
        app.run(host='0.0.0.0', port=5000, threaded=True)
    elif getenv("HBNB_API_HOST") is not None and \
            getenv("HBNB_API_PORT") is None:
        app.run(host=getenv("HBNB_API_HOST"), port=5000, threaded=True)
    elif getenv("HBNB_API_HOST") is None and \
            getenv("HBNB_API_PORT") is not None:
        app.run(host='0.0.0.0', port=getenv("HBNB_API_PORT"), threaded=True)
    else:
        app.run(host=getenv("HBNB_API_HOST"), port=getenv("HBNB_API_PORT"),
                threaded=True)
