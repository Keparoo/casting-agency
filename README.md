# Casting Agency

This is the capstone project for Udacity's Fullstack Nanodegree program. It models a casting agency that is responsible for casting actors in movies and managing these actors. Authorized users can interact with the API to view, add, update, and delete movies and actor details.

---
## API URL 
- **Heroku:** [base URL](https://xxxx.herokuapp.com/)
- **Localhost:** base URL is http://127.0.0.1:5000/


## Features
- Create and manage a database of actors and movies for casting purposes.

## Authentication and Authorisation
Authentication is implemented in the form of Role Based Access Control using Auth0
#### Roles
- Executive Producer
- Casting Director
- Casting Assistance

## Getting Started

### Installation and Database Setup

Clone the repo by running 

```bash
git clone https://github.com/Keparoo/casting-agency.git
```
#### Key Dependencies

- [Python 3.8.5](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python) Follow the instructions to install the latest version of python for your platform. This project was developed using Python 3.8.5 and the project will not run with versions of Python below 3.6.
- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.
- Flask-Migrate
- PostgreSQL
- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.
- Unittest
- Auth0

#### Virtual Enviornment

It is recommended to work within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

```bash
python3 -m venv venv
```

Activate the virtual environment:

```bash
. venv/bin/activate
```

#### Installing Python Dependencies

Once the virtual environment is setup and running, install the required dependencies by navigating to the project directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages in the `requirements.txt` file.

---

## Database Setup

The project uses  Postgresql databases.
- Create two databases: One for **testing** and one for **development**
```bash
createdb <database_name>
```
- Generate database tables from the migration files included by executing: 
  `python manage.py db upgrade`
- Add starter data by executing:
  `python manage.py seed`

- Change the database_url in setup.sh and setup_testing.sh to match the names of your development and testing databases

## Running the Server
From within the project directory first ensure you are working using your created virtual environment.

#### To run the **development** server, execute:  

```bash
source setup.sh
flask run
```
#### To run the **test** suite:
- Stop the development server
- add fresh token for each of the roles specified above under roles. (See section on authorization)
- Then execute:
 
```bash
source setup_test.sh
```

---
## API

In order to use the API users need to be authenticated. JWT tokens can be generated by logging in with the provided credentials on the hosted site.

### Endpoints

#### GET /movies

- General:

  - Returns a list of all the movies.
  - Roles authorized : Casting Assistant, Casting Director, Executive Producer.

- Sample: `curl http://127.0.0.1:5000/movies`

```json
{
    "movies": [
        {
            "id": 1,
            "release_date": "Fri, 19 Jan 2018 05:00:00 GMT",
            "title": "Call Me By Your Name"
        },
        {
            "id": 2,
            "release_date": "Wed, 30 Sep 2020 05:00:00 GMT",
            "title": "The Boys in the Band"
        }
        ],
    "success": true
}
```

#### GET /movies/\<int:id>

- General:

  - Route for getting a specific movie.
  - Roles authorized : Casting Assistant,Casting Director,Executive Producer.

- Sample: `curl http://127.0.0.1:5000/movies/1`

```json
{
  "movie": {
    "id": 1,
    "release_date": "Fri, 19 Jan 2018 05:00:00 GMT",
    "title": "Call Me By Your Name"
  },
  "success": true
}
```

#### POST /movies

- General:

  - Creates a new movie based on a payload.
  - Roles authorized : Executive Producer.

- Sample: `curl http://127.0.0.1:5000/movies -X POST -H "Content-Type: application/json" -d '{ "title": "The Boys in the Band", "release_date": "2020-09-30" }'`

```json
{
  "movie": {
    "id": 3,
    "release_date": "Wed, 30 Sep 2020 05:00:00 GMT",
    "title": "The Boys in the Band"
  },
  "success": true
}
```

#### PATCH /movies/\<int:id>

- General:

  - Patches a movie based on a payload.
  - Roles authorized : Casting Director, Executive Producer.

- Sample: `curl http://127.0.0.1:5000/movies/3 -X PATCH -H "Content-Type: application/json" -d '{ "title": "The Boys in the Band Updated", "release_date": "2018-01-19" }'`

```json
{
  "movie": {
    "id": 3,
    "release_date": "Fri, 19 Jan 2018 05:00:00 GMT",
    "title": "The Boys in the Band Updated"
  },
  "success": true
}
```

#### DELETE /movies/\<int:id>

- General:

  - Deletes a movies by id form the url parameter.
  - Roles authorized : Executive Producer.

- Sample: `curl http://127.0.0.1:5000/movies/3 -X DELETE`

```json
{
  "delete": 3,
  "success": true
}
```

#### GET /actors

- General:

  - Returns a list of all the actors.
  - Roles authorized : Casting Assistant,Casting Director,Executive Producer.

- Sample: `curl http://127.0.0.1:5000/actors`

```json
{
  "actors": [
    {
      "age": 26,
      "gender": "male",
      "id": 1,
      "name": "Timothee Chalamet"
    },
    {
      "age": 44,
      "gender": "male",
      "id": 2,
      "name": "Zachary Quinto"
    }
  ],
  "success": true
}
```

#### GET /actors/\<int:id>

- General:

  - Route for getting a specific actor.
  - Roles authorized : Casting Assistant,Casting Director,Executive Producer.

- Sample: `curl http://127.0.0.1:5000/actors/1`

```json
{
  "actor": {
    "age": 26,
    "gender": "male",
    "id": 1,
    "name": "Timothee Chalamet"
  },
  "success": true
}
```

#### POST /actors

- General:

  - Creates a new actor based on a payload.
  - Roles authorized : Casting Director,Executive Producer.

- Sample: `curl http://127.0.0.1:5000/actors -X POST -H "Content-Type: application/json" -d '{ "name": "Marion Cotillard", "age": 46, "gender": "female" }'`

```json
{
  "actor": {
    "age": 46,
    "gender": "female",
    "id": 3,
    "name": "Marion Cotillard"
  },
  "success": true
}
```

#### PATCH /actors/\<int:id>

- General:

  - Patches an actor based on a payload.
  - Roles authorized : Casting Director, Executive Producer.

- Sample: `curl http://127.0.0.1:5000/actors/3 -X PATCH -H "Content-Type: application/json" -d '{ "name": "Marion Cotillard Updated", "age": 20, "gender": "female" }'`

```json
{
  "actor": {
    "age": 20,
    "gender": "female",
    "id": 3,
    "name": "Marion Cotillard Updated"
  },
  "success": true
}
```

#### DELETE /actors/<int:id>

- General:

  - Deletes an actor by id form the url parameter.
  - Roles authorized : Casting Director,Executive Producer.

- Sample: `curl http://127.0.0.1:5000/actors/3 -X DELETE`

```json
{
  "delete": 3,
  "success": true
}
```
## Testing

Replace the jwt tokens in test_app.py with the ones generated on the website.

For testing locally, we need to stop the development server and reset the database.
To reset database and run the test suite, run

```bash
source setup_test.sh
```

---

## Error Handling

- 401 errors due to authorization are returned as

```json
{
  "code": "unauthorized",
  "description": "Permission not found."
}
```

Other Errors are returned in the following json format:

```json
{
  "success": "False",
  "error": 404,
  "message": "resource not found"
}
```

The error codes currently returned are:

- 400 – bad request
- 401 – unauthorized
- 403 - forbidden
- 404 – resource not found
- 422 – unprocessable
- 500 – internal server error