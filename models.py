import os
from sqlalchemy import Column, String, Integer, DateTime, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

#----------------------------------------------------------------------------#
# Connect the database and environment variables
#----------------------------------------------------------------------------#

if os.getenv('ENV') == 'test':
    database_path = os.getenv('TEST_DATABASE_URL')
else:
    database_path = os.getenv('NEW_DATABASE_URL')

# DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
# DB_USER = os.getenv('DB_USER', 'kep')
# DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
# DB_NAME = os.getenv('DB_NAME', 'casting')

# DB_PATH = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

# database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
    Binds a flask app to a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    print(f'Connecting to: {database_path}')
    # migrate = Migrate(app, db)

'''
    Drops the database and creates an an empty one
'''
def db_drop_and_create():
    db.drop_all()
    db.create_all()

#----------------------------------------------------------------------------#
# Movie table
#----------------------------------------------------------------------------#
class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(DateTime(), nullable=False)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date
    
    '''
        Inserts a new movie into the database
        The title and release date must not be null
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
        Updates fields of an existing movie
        The title and relase date must not be null
    '''
    def update(self):
        db.session.commit()

    '''
        Deletes a movie from the database matching the sent id
        If the movie does not exist a 404 error is sent
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

    def __repr__(self):
        return f'id: {self.id} title: {self.title} release date: {self.release_date}'

#----------------------------------------------------------------------------#
# Actor table
#----------------------------------------------------------------------------#
class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
    
    '''
        Inserts a new actor into the database
        The name, age, and gender must not be null
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    '''
        Updates fields of an existing actor
        The name, age, and gender must not be null
    '''
    def update(self):
        db.session.commit()

    '''
        Deletes an actor from the database matching the sent id
        If the actor does not exist a 404 error is sent
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def __repr__(self):
        return f'id: {self.id} name: {self.name} age: {self.age} gender: {self.gender}'