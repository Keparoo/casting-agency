import os
from flask import Flask, request, jsonify, abort
from flask import render_template, session, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Movie, Actor, db
import json
from flask_cors import CORS
from auth import AuthError, requires_auth, requires_signed_in
from urllib.parse import urlencode
from authlib.integrations.flask_client import OAuth

AUTH0_CALLBACK_URL = os.environ['AUTH0_CALLBACK_URL']
AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
AUTH0_CLIENT_ID = os.environ['AUTH0_CLIENT_ID']
AUTH0_CLIENT_SECRET = os.environ['AUTH0_CLIENT_SECRET']
AUTH0_AUDIENCE = os.environ['AUTH0_AUDIENCE']
AUTH0_BASE_URL='https://' + AUTH0_DOMAIN

# create and configure the Flask app
def create_app(test_config=None):
    
    app = Flask(__name__)
    app.secret_key = "really super secret"
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    oauth = OAuth(app)

    auth0 = oauth.register(
        'auth0',
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET,
        api_base_url=AUTH0_BASE_URL,
        access_token_url=AUTH0_BASE_URL + '/oauth/token',
        authorize_url=AUTH0_BASE_URL + '/authorize',
        client_kwargs={
            'scope': 'openid profile email',
        },
    )
#----------------------------------------------------------------------------#
# API Endpoints
#----------------------------------------------------------------------------#
    @app.route('/', methods=['GET'])
    def index():
        '''Home page route'''
        return render_template('index.html')
        # return jsonify({
        #     'message': 'Welcome to the Casting Agency Home Page'
        # })

    @app.route('/login')
    def login():
        return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)
        # params = {'audience': API_AUDIENCE, 'response_type': 'token','client_id': AUTH0_CLIENT_ID, 'redirect_uri': url_for('jwtcontrol', _external=True)}
        # return redirect(AUTH0_BASE_URL + '/authorize?' + urlencode(params))
        # return render_template('login.html')

    @app.route('/callback')
    def callback():
        # Handles callback response from Auth0
        res = auth0.authorize_access_token()
        token = res.get('access_token')

        # Store the user jwt token in flask session
        session['jwt_token'] = token
        
        return redirect('/jwtcontrol')

    @app.route('/logout')
    def logout():
        session.clear()
        params = {'returnTo': url_for('index', _external=True), 'client_id': AUTH0_CLIENT_ID}
        return redirect(AUTH0_BASE_URL + '/v2/logout?' + urlencode(params))
    
    @app.route('/jwtcontrol')
    @requires_signed_in
    def jwtcontrol():
        return render_template('jwtcontrol.html', token=session['jwt_token'])

#----------------------------------------------------------------------------#
# Movie Routes
#----------------------------------------------------------------------------#
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(jwt):
        '''Return all movies from database'''

        try:
            movies = Movie.query.all()

            return jsonify({
                'success': True,
                'movies': [movie.format() for movie in movies]
            }), 200
        except Exception as e:
            abort(500)

    @app.route('/movies/<int:id>', methods=['GET'])
    @requires_auth('get:movies')
    def get_movie_by_id(jwt, id):
        '''Return movie matching the id'''

        try:
            movie = Movie.query.get(id)
        except Exception as e:
            abort(422)


        if movie is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'movie': movie.format()
            }), 200

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(jwt):
        """Create and insert new movie into database"""

        data = request.get_json()

        title = data.get("title", None)
        release_date = data.get("release_date", None)

        movie = Movie(title=title, release_date=release_date)

        if title is None or release_date is None:
            abort(400)

        try:
            movie.insert()
            return jsonify({
                "success": True,
                "movie": movie.format()
            }), 201
        except Exception as e:
            abort(422)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(jwt, id):
        '''Update movie info in database'''

        data = request.get_json()
        title = data.get('title', None)
        release_date = data.get('release_date', None)

        try:
            movie = Movie.query.get(id)
        except:
            abort(500)

        if movie is None:
            abort(404)

        if title is None or release_date is None:
            abort(400)

        movie.title = title
        movie.release_date = release_date

        try:
            movie.update()
            return jsonify({
                'success': True,
                'movie': movie.format()
            }), 200
        except Exception as e:
            db.session.rollback()
            abort(422)

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt, id):
        '''Delete movie matching id from database'''

        try:
            movie = Movie.query.get(id)
        except:
            abort(500)

        if movie is None:
            abort(404)
        
        try:
            movie.delete()
            return jsonify({
                'success': True,
                'delete': id
            }), 200
        except Exception as e:
            db.session.rollback()
            abort(500)
#----------------------------------------------------------------------------#
# Actor Routes
#----------------------------------------------------------------------------#
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(jwt):
        '''Return all actors from database'''

        try:
            actors = Actor.query.all()

            return jsonify({
                'success': True,
                'actors': [actor.format() for actor in actors]
            }), 200
        except Exception as e:
            abort(500)

    @app.route('/actors/<int:id>', methods=['GET'])
    @requires_auth('get:actors')
    def get_actor_by_id(jwt, id):
        '''Return actor matching the id'''

        try:
            actor = Actor.query.get(id)
        except Exception as e:
            abort(422)   

        if actor is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'actor': actor.format()
            }), 200

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(jwt):
        """Create and insert new actor into database"""

        data = request.get_json()

        name = data.get("name", None)
        age = data.get("age", None)
        gender = data.get("gender", None)

        actor = Actor(name=name, age=age, gender=gender)

        if name is None or age is None or gender is None:
            abort(400)

        try:
            actor.insert()
            return jsonify({
                "success": True,
                "actor": actor.format()
            }), 201
        except Exception as e:
            abort(422)

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(jwt, id):
        '''Update actor info in database'''

        data = request.get_json()
        name = data.get('name', None)
        age = data.get('age', None)
        gender = data.get('gender', None)

        try:
            actor = Actor.query.get(id)
        except:
            abort(500)

        if actor is None:
            abort(404)

        if name is None or age is None or gender is None:
            abort(400)

        actor.name = name
        actor.age = age
        actor.gender = gender

        try:
            actor.update()
            return jsonify({
                'success': True,
                'actor': actor.format()
            }), 200
        except Exception as e:
            db.session.rollback()
            abort(422)

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(jwt, id):
        '''Delete actor matching id from database'''

        try:
            actor = Actor.query.get(id)
        except:
            abort(500)

        if actor is None:
            abort(404)
        
        try:
            actor.delete()
            return jsonify({
                'success': True,
                'delete': id
            }), 200
        except Exception as e:
            db.session.rollback()
            abort(500)

#----------------------------------------------------------------------------#
# Error Handling
#----------------------------------------------------------------------------#
    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
                "success": False,
                "error": 404,
                "message": "resource not found"
            }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
                "success": False,
                "error": 500,
                "message": "internal server error",
                }), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify(
                {
                    "success": False,
                    "error": 400,
                    "message": "bad request",
                }
            ), 400

    @app.errorhandler(401)
    def unathorized(error):
        return jsonify(
                {
                    "success": False,
                    "error": 401,
                    "message": error.description,
                }
            ), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify(
                {
                    "success": False,
                    "error": 403,
                    "message": "forbidden",
                }
            ), 403

    @app.errorhandler(AuthError)
    def handle_auth_error(exception):
        response = jsonify(exception.error)
        response.status_code = exception.status_code
        return response

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)