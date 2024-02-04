#!/usr/bin/python3
""" app api """
from models import storage
from flask import Flask, make_response, jsonify
from os import getenv
from flask_cors import CORS
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_storage(error):
    """ Calls close method for storage """
    storage.close()


@app.errorhandler(404)
def handle_not_found(error):
    """ A custom 404 page not found """
    return make_response(jsonify({
        "error": "Not found"
    }), 404)


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)

    app.run(host=host, port=int(port), threaded=True)
