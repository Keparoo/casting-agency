import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie

#Insert JWT Constants
CASTING_ASSISTANT=''
CASTING_DIRECTOR=''
EXECUTIVE_PRODUCER=''

class CastingAgencyTestCase(unittest.TestCase):
    '''This class represents the Casting Agency Test Case'''

    def setUp(self) -> None:
        '''Define test variables and initialize app'''
        self.app = create_app()
        self.client = self.app.test_client

        # Set up database
        self.database_name = "casting"
        self.database_path = "postgresql://{}:{}@{}/{}".format('kep','password','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # Create test variable data
        self.test_movie = {
            'title': 'La Vie En Rose',
            'release_date': '2007-07-20',
        }
        self.test_actor = {
            'name': 'Marion Cotillard',
            'age': 46,
            'gender': 'female',
        }

    def tearDown(self):
        """Executed after each test"""
        pass

#----------------------------------------------------------------------------#
# Movie Route Tests
#----------------------------------------------------------------------------#
    def test_add_movie(self):
        '''Tests add movie success'''

        num_movies_before = Movie.query.all()

        res = self.client().post('/movies', json=self.test_movie)
        data = json.loads(res.data)

        num_movies_after = Movie.query.all()

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'La Vie En Rose')
        self.assertEqual(data['movie']['release_date'], 'Fri, 20 Jul 2007 05:00:00 GMT')
        #check that number of movies increases by 1
        self.assertTrue(len(num_movies_after) - len(num_movies_before) == 1)
    
    def test_400_add_movie_fails(self):
        '''Tests add_movie failure sends 422'''

        num_movies_before = Movie.query.all()

        # no data sent to create movie
        res = self.client().post('/movies', json={})
        data = json.loads(res.data)

        num_movies_after = Movie.query.all()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'])
        self.assertEqual(data["message"], "bad request")
        # number of questions doesn't change
        self.assertTrue(len(num_movies_after) == len(num_movies_before))

    def test_get_all_movies(self):
        '''Tests get_movies success'''

        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_movie_by_id(self):
        '''Tests getting movie by id'''

        res = self.client().get('/movies/1')
        data = json.loads(res.data)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'La Vie En Rose') 

    def test_404_get_movie_by_id(self):
        '''Tests failure for invalid id number'''

        res = self.client().get('/movies/9999')
        data = json.loads(res.data)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_update_movie(self):
        '''Tests succuss of update_movie'''

        res = self.client().patch('/movies/1', json=self.test_movie)
        data = json.loads(res.data)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'La Vie En Rose')
        self.assertEqual(
            data['movie']['release_date'],
            'Fri, 20 Jul 2007 05:00:00 GMT'
        )

    def test_400_update_movie(self):
        '''Tests 400 failure of update_movie if no data sent'''

        res = self.client().patch('/movies/1', json={})
        data = json.loads(res.data)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    def test_404_update_movie(self):
        '''Tests 404 failure if update_movie sent bad id'''

        res = self.client().patch('/movies/9999', json=self.test_movie)
        data = json.loads(res.data)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_movie(self):
        '''Tests successful delete of movie'''

        num_movies_before = Movie.query.all()

        res = self.client().delete('/movies/37')
        data = json.loads(res.data)

        num_movies_after = Movie.query.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 37)
        # number of movies is one less
        self.assertTrue(len(num_movies_before) - len(num_movies_after) == 1)

    def test_404_delete_movie(self):
        '''Tests failure to delete movie with non-existant id'''

        num_movies_before = Movie.query.all()

        res = self.client().delete('/movies/9999')
        data = json.loads(res.data)

        num_movies_after = Movie.query.all()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        # number of movies is one less
        self.assertTrue(len(num_movies_before) == len(num_movies_after))

#----------------------------------------------------------------------------#
# Actor Route Tests
#----------------------------------------------------------------------------#
    def test_add_actor(self):
        '''Tests add actor success'''

        num_actors_before = Actor.query.all()

        res = self.client().post('/actors', json=self.test_actor)
        data = json.loads(res.data)

        num_actors_after = Actor.query.all()

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertEqual(data['actor']['name'], 'Marion Cotillard')
        self.assertEqual(data['actor']['age'], 46)
        self.assertEqual(data['actor']['gender'], 'female')
        #check that number of actors increases by 1
        self.assertTrue(len(num_actors_after) - len(num_actors_before) == 1)
    
    def test_400_add_actor_fails(self):
        '''Tests add_actor failure sends 400'''

        num_actors_before = Actor.query.all()

        # no data sent to create actor
        res = self.client().post('/actors', json={})
        data = json.loads(res.data)

        num_actors_after = Actor.query.all()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'])
        self.assertEqual(data["message"], "bad request")
        # number of questions doesn't change
        self.assertTrue(len(num_actors_after) == len(num_actors_before))

    def test_get_all_actors(self):
        '''Tests get_actors success'''

        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_actor_by_id(self):
        '''Tests getting actor by id'''

        res = self.client().get('/actors/1')
        data = json.loads(res.data)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertEqual(data['actor']['name'], 'Marion Cotillard')
        self.assertEqual(data['actor']['age'], 46)
        self.assertEqual(data['actor']['gender'], 'female') 

    def test_404_get_actor_by_id(self):
        '''Tests failure for invalid id number'''

        res = self.client().get('/actors/9999')
        data = json.loads(res.data)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_update_actor(self):
        '''Tests succuss of update_actor'''

        res = self.client().patch('/actors/1', json=self.test_actor)
        data = json.loads(res.data)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertEqual(data['actor']['name'], 'Marion Cotillard')
        self.assertEqual(data['actor']['age'], 46)
        self.assertEqual(data['actor']['gender'], 'female')

    def test_400_update_actor(self):
        '''Tests 400 failure of update_actor if no data sent'''

        res = self.client().patch('/actors/1', json={})
        data = json.loads(res.data)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    def test_404_update_actor(self):
        '''Tests 404 failure if update_actor sent bad id'''

        res = self.client().patch('/actors/9999', json=self.test_actor)
        data = json.loads(res.data)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_actor(self):
        '''Tests successful delete of actor'''

        num_actors_before = Actor.query.all()

        res = self.client().delete('/actors/10')
        data = json.loads(res.data)

        num_actors_after = Actor.query.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 10)
        # number of actors is one less
        self.assertTrue(len(num_actors_before) - len(num_actors_after) == 1)

    def test_404_delete_actor(self):
        '''Tests failure to delete actor with non-existant id'''

        num_actors_before = Actor.query.all()

        res = self.client().delete('/actors/9999')
        data = json.loads(res.data)

        num_actors_after = Actor.query.all()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        # number of actors is one less
        self.assertTrue(len(num_actors_before) == len(num_actors_after))


if __name__ == "__main__":
    unittest.main()