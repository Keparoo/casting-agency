import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie

#Insert JWT Constants
CASTING_ASSISTANT='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InNWbGNMV1ZjeWVla3RUMXkzOEQ5RSJ9.eyJpc3MiOiJodHRwczovL3dlYnNlY3VyZS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBlN2E1MjNmMGY5NzUwMDZhODI0OWIwIiwiYXVkIjpbImNhc3RpbmctYWdlbmN5IiwiaHR0cHM6Ly93ZWJzZWN1cmUudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTYyNjAyNzc0NiwiZXhwIjoxNjI2MTE0MTQ2LCJhenAiOiIxS1lpUVYwNjV0bVFpNzUxM1ZtRDNLYTZUeHZOcHlSbCIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.TLGzTE8LgETh9ITRGr9BrPkxkgV6pXKqfLkFlinttrutEorzWHw0pO9mXGtmJjhx7HEMU7Oy679sMOL1cqHFB6rLmC5O_Oi_l659RFU6R1I2DYpbnAHN81Hmww7_e17x3p734KLiJrPcLRlDDYmKpygTm7W7ol2zintbDzg6tAh_cWHslUHFqEzbc1xhbWsAIbek51l9Y2c646u29bKOGnQLT7GdGpmu1cIUakTpQpBa4Sre00n818TEvwsf6kZFoGnyesOYbDVPx-GvpEnnu93Kf4dXy4dEGZBZH0B1S2wZoP8T8uY_T_PgPCrcmtnJhXOxfXk3U4bMeUmnZPVPBw'
CASTING_DIRECTOR='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InNWbGNMV1ZjeWVla3RUMXkzOEQ5RSJ9.eyJpc3MiOiJodHRwczovL3dlYnNlY3VyZS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBlN2E0YzcwNmJkYmUwMDcxYTcxMjcyIiwiYXVkIjpbImNhc3RpbmctYWdlbmN5IiwiaHR0cHM6Ly93ZWJzZWN1cmUudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTYyNjAyNzcxMiwiZXhwIjoxNjI2MTE0MTEyLCJhenAiOiIxS1lpUVYwNjV0bVFpNzUxM1ZtRDNLYTZUeHZOcHlSbCIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwb3N0OmFjdG9ycyJdfQ.Okv02_VwQTU8uI7oKZpHP1hYWJRLYdZQxpxRYdOXBHkPNjwA6bK4TFiEw1nbSSzj0zF_JXC2GHk1kpEk7ddRQpE4pNGvmmzbbeswerVN9aR9EXmIzNEtxDavm1VKs3EeKLrG7OjP-iydGkqRY8ZWK7FIE1wZch8LtUSvO67pVsc0xP917W0oajHbo42UCD6ErppSmM_y6Xv1Aq4zLnrU6N-MPX67lzBnokb2tb4t3myefagupxxQu5DPlmJzvQrD7MHWhtN605cf87n9Jdb_RGMujfiRkv6o24yBYWja-Bzl35j6rdwkCtBJDs1OUwXhY2GxzMpE5dLH2qP_h5g-mw'
EXECUTIVE_PRODUCER='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InNWbGNMV1ZjeWVla3RUMXkzOEQ5RSJ9.eyJpc3MiOiJodHRwczovL3dlYnNlY3VyZS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBlN2E0ZjEwNGY0OWEwMDZmZTRlNmExIiwiYXVkIjpbImNhc3RpbmctYWdlbmN5IiwiaHR0cHM6Ly93ZWJzZWN1cmUudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTYyNjAyNzYzMCwiZXhwIjoxNjI2MTE0MDMwLCJhenAiOiIxS1lpUVYwNjV0bVFpNzUxM1ZtRDNLYTZUeHZOcHlSbCIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.dRTYfEN4fFUJttlvKeYhyEsVBuqt33fpXCtPo-hJ0IbPrKz6eVa6lKDCBWZFVmznPX7PeSu6UR5hAtjP8vw9iTJuC3cL3AwiLpHI8NLKxym1RSV0ydzfijCIkIGvyQUpkvPvmpSmDVCEcmrSXO3ajvuYo9jS61Rei__-LXS0CdE2O88JNieAnnoMn37HMJnTlUh4S33rm--2LcVTipbqypVhgNUM_hgR9WEHm2CoFhDxHj6yDDTAbLi4kCeRIeGZLsl3yMsOxrTVkklmevztuYn_G0ca9wNznCJp34KQLG7eoWk4j8YIalrO5h0kAp4630YImlgZj6ewHfyyHgV-GA'

class CastingAgencyTestCase(unittest.TestCase):
    '''This class represents the Casting Agency Test Case'''

    def setUp(self) -> None:
        '''Define test variables and initialize app'''
        self.app = create_app()
        self.client = self.app.test_client

        # Set up database
        self.database_path=os.environ['TEST_DATABASE_URL']
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
        '''Tests success of update_movie'''

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
        '''Tests success of update_actor'''

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
        '''Test auth failure: no post:movies'''
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
        '''test auth failure: no post:actors'''
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
        '''Test auth failure: no patch:actors'''
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
        '''Test auth error: no delete:movies'''
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