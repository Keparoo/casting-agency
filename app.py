
import os
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from models import setup_db
import json
from flask_cors import CORS

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/', methods=['GET'])
    def homepage():
        return 'Hello Casting Agency!'

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)