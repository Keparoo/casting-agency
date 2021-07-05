import os
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Movie, Actor, db
import json
from flask_cors import CORS

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    
#----------------------------------------------------------------------------#
# Movie Routes
#----------------------------------------------------------------------------#
    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            'message': 'Welcome to the Casting Agency Home Page'
        })

    @app.route('/movies', methods=['GET'])
    def get_movies():
        '''Return all movies from database'''

        try:
            movies = Movie.query.all()

            return jsonify({
                'success': 'True',
                'movies': [movie.format() for movie in movies]
            }), 200
        except Exception as e:
            abort(500)

    @app.route('/movies/<int:id>', methods=['GET'])
    def get_movie_by_id(id):
        '''Return movie matching the id'''

        try:
            movie = Movie.query.get(id)

            if movie is None:
                abort(404)
            else:
                return jsonify({
                    'success': True,
                    'movie': movie.format()
                }), 200
        except Exception as e:
            abort(422)

    @app.route('/movies', methods=['POST'])
    def add_movie():
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
    def update_movie(id):
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
    def delete_movie(id):
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
    def get_actors():
        '''Return all actors from database'''

        try:
            actors = Actor.query.all()

            return jsonify({
                'success': 'True',
                'actors': [actor.format() for actor in actors]
            }), 200
        except Exception as e:
            abort(500)

    @app.route('/actors/<int:id>', methods=['GET'])
    def get_actor_by_id(id):
        '''Return actor matching the id'''

        try:
            actor = Actor.query.get(id)

            if actor is None:
                abort(404)
            else:
                return jsonify({
                    'success': True,
                    'actor': actor.format()
                }), 200
        except Exception as e:
            abort(422)

    @app.route('/actors', methods=['POST'])
    def add_actor():
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
    def update_actor(id):
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
    def delete_actor(id):
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

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)