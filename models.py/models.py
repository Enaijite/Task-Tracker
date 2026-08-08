from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy() #creates an instance of the SQLAlchemy class, used to interact with the database.

#creating a User class, that represents a table in the database, 
#inherits from db.Model, which is a base class provided by SQLAlchemy for defining models.
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(50), unique=True, nullable=False) #unique=True ensures that each username is unique in the database, and nullable=False means that this field cannot be left empty.
    password_hash = db.Column(db.String(200), nullable=False) #stores the hashed password of the user, not the plain text password.
    tasks = db.relationship('Task', backref='user', lazy=True) # not a column; a relationship that creates a one-to-many relationship between a User and task so we can get all the tasks related to a user.