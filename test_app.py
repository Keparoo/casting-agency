import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie

#Insert JWT Constants
CASTING_ASSISTANT='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InNWbGNMV1ZjeWVla3RUMXkzOEQ5RSJ9.eyJpc3MiOiJodHRwczovL3dlYnNlY3VyZS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBlN2E1MjNmMGY5NzUwMDZhODI0OWIwIiwiYXVkIjpbImNhc3RpbmctYWdlbmN5IiwiaHR0cHM6Ly93ZWJzZWN1cmUudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTYyNTg3NjMyNCwiZXhwIjoxNjI1OTYyNzI0LCJhenAiOiIxS1lpUVYwNjV0bVFpNzUxM1ZtRDNLYTZUeHZOcHlSbCIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.Z0IaD3fs923UXNh3kA5JNgCkcGMhOzMlX8bhgntZ7UewG0UUn4fQ5fGu1Dyy2B-VBbvgODjsW7MaXQIAN9QcjM_T8L7CAmq-YCJYbh2PdmglDzH7ZqgxQ6jl332Y1ZWVBW3875gZR7vYD6l_hEnZGTmOrlhRpST7DhHIiNPHmF8T_0bezDt0h6pQuixZVINlwJDIIHSykLL6JAO34Ll_vyQafgqg8cmGTST8PdNGc3abPI7J1OROkPe8hWAd3BC8VXy_DqqOLBdQe53IBJ08KpSM6KW7itJeas4AFZ0j84m6MdfqdnnQ9_BcYxwaqbFcTL9LxxlASbf80coHBBywuA'
CASTING_DIRECTOR='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InNWbGNMV1ZjeWVla3RUMXkzOEQ5RSJ9.eyJpc3MiOiJodHRwczovL3dlYnNlY3VyZS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBlN2E0YzcwNmJkYmUwMDcxYTcxMjcyIiwiYXVkIjpbImNhc3RpbmctYWdlbmN5IiwiaHR0cHM6Ly93ZWJzZWN1cmUudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTYyNTg3NjM1NSwiZXhwIjoxNjI1OTYyNzU1LCJhenAiOiIxS1lpUVYwNjV0bVFpNzUxM1ZtRDNLYTZUeHZOcHlSbCIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwb3N0OmFjdG9ycyJdfQ.C7rW3ZVjHLvalovrNbeY132fwQSxE_4G0-z6QZCL1PVu2_FfHC3UVIGEFmXKhgcOflStpsbL7f35KP5CsrExLuO5IZ5k4unETIl0_t0eMX1Ki_gmP0w2Dg04WBqbVxM45zQfwF8vd_bYkWp1SNlz5dmMOswxKxFUnfV6FB4fwWZ8Nk1-4RwvkZ9UfC09jKFtWytK1LtcUJETSOSoj2VlurPWY0mQtdP88ui4Tqj04CCAQFYhaTVJdywPvcxk3goD18hwI0HzrrdWA_ZpkxQDswjENS9qClDmHbSkogDKtPDK4_hp5iy3HjS5ppFcEKXnS5dP4Nuym4ubfMuixNHT2A'
EXECUTIVE_PRODUCER='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InNWbGNMV1ZjeWVla3RUMXkzOEQ5RSJ9.eyJpc3MiOiJodHRwczovL3dlYnNlY3VyZS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBlN2E0ZjEwNGY0OWEwMDZmZTRlNmExIiwiYXVkIjpbImNhc3RpbmctYWdlbmN5IiwiaHR0cHM6Ly93ZWJzZWN1cmUudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTYyNTg3NjM5MCwiZXhwIjoxNjI1OTYyNzkwLCJhenAiOiIxS1lpUVYwNjV0bVFpNzUxM1ZtRDNLYTZUeHZOcHlSbCIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.ppj2kX_vK89Rp51nnl9o9yEKU2vQHLAfhWYqJib_N19uRY9YPTaKyJF5nZSaEzuHew-NJBMWiFQWBc9BMecsXKHZ0Ji-tG5SUBu2f7SMYdNGmGMNO79qtXQHOTE5Df0TjmpJ2y0vw0Fmu6UaWJ0a6Cmh9PULXlHdWEdlfSwO-itwWmHKSeulhQAsZ2qbbiermDPJvrvyI9FTyA6qE2VCOct5sJU2PFDvGyUwhb1uXfM-rhRLcyGVT3sThCe8taEphYwWDIHAxbZgKCUyrqDHGvYSdEc6opPghlxC6QtS2rqQQWpcxOQaTtLq_WnRtPwzCagQW3ddNHUvZ2bcg-2e8A'

class CastingAgencyTestCase(unittest.TestCase):
    '''This class represents the Casting Agency Test Case'''

    def setUp(self) -> None:
        '''Define test variables and initialize app'''
        self.app = create_app()
        self.client = self.app.test_client

        # Set up database
        self.database_path=os.environ['TEST_DATABASE_URL']
        # self.database_name = "test_casting"
        # self.database_path = "postgresql://{}:{}@{}/{}".format('kep','password','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # Create test variable data
        self.test_movie = {
            'title': 'La Vie En Rose',
            'release_date': '2007-07-20'
        }
        self.test_actor = {
            'name': 'Marion Cotillard',
            'age': 46,
            'gender': 'female'
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

        res = self.client().post('/movies', json=self.test_movie, headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER})
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
        res = self.client().post('/movies', json={}, headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER})
        data = json.loads(res.data)

        num_movies_after = Movie.query.all()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'])
        self.assertEqual(data["message"], "bad request")
        # check number of movies doesn't change
        self.assertTrue(len(num_movies_after) == len(num_movies_before))

    def test_get_all_movies(self):
        '''Tests get_movies success'''

        res = self.client().get('/movies', headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_movie_by_id(self):
        '''Tests getting movie by id'''

        res = self.client().get('/movies/1', headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER})
        data = json.loads(res.data)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'Call Me By Your Name') 

    def test_404_get_movie_by_id(self):
        '''Tests failure for invalid id number'''

        res = self.client().get('/movies/9999', headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER})
        data = json.loads(res.data)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_update_movie(self):
        '''Tests succuss of update_movie'''

        res = self.client().patch('/movies/1', json=self.test_movie, headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER})
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

        res = self.client().patch('/movies/1', json={}, headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER})
        data = json.loads(res.data)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    def test_404_update_movie(self):
        '''Tests 404 failure if update_movie sent bad id'''

        res = self.client().patch('/movies/9999', json=self.test_movie, headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER})
        data = json.loads(res.data)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_movie(self):
        '''Tests successful delete of movie'''

        num_movies_before = Movie.query.all()

        res = self.client().delete('/movies/2', headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER})
        data = json.loads(res.data)

        num_movies_after = Movie.query.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 2)
        # check number of movies is one less
        self.assertTrue(len(num_movies_before) - len(num_movies_after) == 1)

    def test_404_delete_movie(self):
        '''Tests failure to delete movie with non-existant id'''

        num_movies_before = Movie.query.all()

        res = self.client().delete('/movies/9999', headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER})
        data = json.loads(res.data)

        num_movies_after = Movie.query.all()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        # check number of movies is one less
        self.assertTrue(len(num_movies_before) == len(num_movies_after))

#----------------------------------------------------------------------------#
# Actor Route Tests
#----------------------------------------------------------------------------#
    def test_add_actor(self):
        '''Tests add actor success'''

        num_actors_before = Actor.query.all()

        res = self.client().post('/actors', json=self.test_actor, headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER})
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
        res = self.client().post('/actors', json={}, headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER})
        data = json.loads(res.data)

        num_actors_after = Actor.query.all()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'])
        self.assertEqual(data["message"], "bad request")
        # check number of actors doesn't change
        self.assertTrue(len(num_actors_after) == len(num_actors_before))

    def test_get_all_actors(self):
        '''Tests get_actors success'''

        res = self.client().get('/actors', headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_actor_by_id(self):
        '''Tests getting actor by id'''

        res = self.client().get('/actors/1', headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER})
        data = json.loads(res.data)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertEqual(data['actor']['name'], 'Timothee Chalamet')
        self.assertEqual(data['actor']['age'], 26)
        self.assertEqual(data['actor']['gender'], 'male') 

    def test_404_get_actor_by_id(self):
        '''Tests failure for invalid id number'''

        res = self.client().get('/actors/9999', headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER})
        data = json.loads(res.data)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_update_actor(self):
        '''Tests succuss of update_actor'''

        res = self.client().patch('/actors/1', json=self.test_actor, headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER})
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

        res = self.client().patch('/actors/1', json={}, headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER})
        data = json.loads(res.data)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    def test_404_update_actor(self):
        '''Tests 404 failure if update_actor sent bad id'''

        res = self.client().patch('/actors/9999', json=self.test_actor, headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER})
        data = json.loads(res.data)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_actor(self):
        '''Tests successful delete of actor'''

        num_actors_before = Actor.query.all()

        res = self.client().delete('/actors/2', headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER})
        data = json.loads(res.data)

        num_actors_after = Actor.query.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 2)
        # check number of actors is one less
        self.assertTrue(len(num_actors_before) - len(num_actors_after) == 1)

    def test_404_delete_actor(self):
        '''Tests failure to delete actor with non-existant id'''

        num_actors_before = Actor.query.all()

        res = self.client().delete('/actors/9999', headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER})
        data = json.loads(res.data)

        num_actors_after = Actor.query.all()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        # check number of actors is one less
        self.assertTrue(len(num_actors_before) == len(num_actors_after))

#----------------------------------------------------------------------------#
# Authorization Tests
#----------------------------------------------------------------------------#
    def test_unauthorised_add_movies(self):
        response= self.client().post(
            '/movies',
            json=self.test_movie,
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Permission not found')

    def test_unauthorised_add_actors(self):
        response= self.client().post(
            '/actors',
            json=self.test_actor,
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Permission not found')

    def test_unauthorised_in_edit_actor(self):
        response= self.client().patch(
            '/actors/1',
            json=self.test_actor,
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Permission not found')

    def test_unauthorised_delete_movie(self):
        response = self.client().delete(
            '/movies/1',
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Permission not found')

if __name__ == "__main__":
    unittest.main()