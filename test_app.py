import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie

#Insert JWT Constants
CASTING_ASSISTANT='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InNWbGNMV1ZjeWVla3RUMXkzOEQ5RSJ9.eyJpc3MiOiJodHRwczovL3dlYnNlY3VyZS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBiZTcxYzU2MTJkODIwMDcwYTRlZWVlIiwiYXVkIjoiY2FzdGluZy1hZ2VuY3kiLCJpYXQiOjE2MjU2OTQ0MTcsImV4cCI6MTYyNTcwMTYxNywiYXpwIjoiMUtZaVFWMDY1dG1RaTc1MTNWbUQzS2E2VHh2TnB5UmwiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.TUN8zZbjd3B4tq2bOzvThpkR1Ynn-kjuKIzQDg9iyyIR03tM1R5F3yzC-d_xZnOpVOFmRtR6GvNq0240o43NYh2SEmx-OPgvMVBSCXTzGH8GLT2pUeL_cCo9I9ru47mgVARjPQRsEAnP_QExuOpbWhhHz2c6sdwYf7FpTDikK7aOzQezq4H6j5FRHarhSrlHp7SgagzDKO5t4TButV-30wOWLY9wG_9MdNhubY0ApIXfj9RPAarGahwv4JQdNf-Lz4TVez2gYR0woV4ajW0Fy-dqpELMsQ-aTExi5usYU2kCUzeb1YzFXoASGYU2YD3zYd4wTFd9HIGVp61XMDn3-w'
CASTING_DIRECTOR='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InNWbGNMV1ZjeWVla3RUMXkzOEQ5RSJ9.eyJpc3MiOiJodHRwczovL3dlYnNlY3VyZS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBlNjI2MDBmMGY5NzUwMDZhODIxMGM1IiwiYXVkIjoiY2FzdGluZy1hZ2VuY3kiLCJpYXQiOjE2MjU2OTU3NTUsImV4cCI6MTYyNTcwMjk1NSwiYXpwIjoiMUtZaVFWMDY1dG1RaTc1MTNWbUQzS2E2VHh2TnB5UmwiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbXX0.Axb4kz2xm_xuhxUESmVXHb1Do_gDcgZqeDaOO_5GbvGH6MHql01TvmVrxAC0NZp0J5jmXml5AkcUdpfilP4ci_jwkXlykPH46VaqSyzPiTchNzExaIaiMRxg06O-wH7Kmw2YBXH0F3aF8sxjwTrRQ823aZm2noU1Lx12wnqxRnN1Yd3HPsKWg3yOkpr0RDBBk6uyzq5ERDABLq59sCI1zBrVWBhs3KCrES1_ebJRVE0KNagnbn6bR562ShW6GMxT6nEiofKUIRidjX9f1xDIegMcO2uZz5QYdnjCyGd_MAbwuOD5LQB_7ZFKvDNZrnub0BwLf9e19EGP8mtWKI1Cqg'
EXECUTIVE_PRODUCER='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InNWbGNMV1ZjeWVla3RUMXkzOEQ5RSJ9.eyJpc3MiOiJodHRwczovL3dlYnNlY3VyZS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBiN2Y2MjM3M2NhOGMwMDY4OTU3YjBkIiwiYXVkIjoiY2FzdGluZy1hZ2VuY3kiLCJpYXQiOjE2MjU2OTMwODgsImV4cCI6MTYyNTcwMDI4OCwiYXpwIjoiMUtZaVFWMDY1dG1RaTc1MTNWbUQzS2E2VHh2TnB5UmwiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.FMme79obO4wLyVeXdJsAD1rn6RXg63Tf4EvFKpTkt85oSHUrsnZMjG9_l9Me2hHhgTsMth4bFUWmgO5r_4Gk8Ob6FS-9vPOM2emmdwTzEXmyP86CgnQQatENgi69IqCugRR_6p8XqBw75jWSsEIcs7RKWMRZ_8xop-VrnsjYHJezqZp3RKMLkr6MYhThNF4C6_goUMmg5tn8HmCfidkHkmQ844GWaXvMsbLdx2TGwwAhU_jIcJkpZI8URT7-tqJ6o7hg6cAdyn8x3owvv7gXFb0kfdIroCh6g6Z_3aiwd2E4i2cvrTfVkL6qF9Si58KOSwRzYoZ0OUhh2BH5VlVp9A'

class CastingAgencyTestCase(unittest.TestCase):
    '''This class represents the Casting Agency Test Case'''

    def setUp(self) -> None:
        '''Define test variables and initialize app'''
        self.app = create_app()
        self.client = self.app.test_client

        # Set up database
        self.database_name = "test_casting"
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
        # number of questions doesn't change
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
        # number of movies is one less
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
        # number of movies is one less
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
        # number of questions doesn't change
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
        # number of actors is one less
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
        # number of actors is one less
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

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertTrue(data['description'], 'Permission not found')

    def test_unauthorised_add_actors(self):
        response= self.client().post(
            '/actors',
            json=self.test_actor,
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertTrue(data['description'], 'Permission not found')

    def test_unauthorised_in_edit_actor(self):
        response= self.client().patch(
            '/actors/1',
            json=self.test_actor,
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertTrue(data['description'], 'Permission not found')

    def test_unauthorised_delete_movie(self):
        response = self.client().delete(
            '/movies/1',
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertTrue(data['description'], 'Permission not found')

if __name__ == "__main__":
    unittest.main()