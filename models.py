from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy() #creates an instance of the SQLAlchemy class, used to interact with the database.

#creating a User class, that represents a table in the database, 
#inherits from db.Model, which is a base class provided by SQLAlchemy for defining models.
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(80), unique=True, nullable=False) #unique=True ensures that each username is unique in the database, and nullable=False means that this field cannot be left empty.
    password_hash = db.Column(db.String(200), nullable=False) #stores the hashed password of the user, not the plain text password.
    tasks = db.relationship('Task', backref='user', lazy=True) #not a column; a relationship that creates a one-to-many relationship between a User and task so we can get all the tasks related to a user.

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)#Text for longer unbounded text like paragraphs
    status = db.Column(db.String(20), nullable=False, default='In-Progress')#default for status is "In-Progress", can be changed to Completed or any other status as needed.
    createdAt = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))#lambda function used so when time is set it is the current time each time, not a static time.
    updatedAt = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))#onupdate is used to automatically update the timestamp whenever the task is updated.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)#Foreign key that establishes a relationship between the Task and User models(tables), linking each task to a specific user, Nullable=False means that every task must belong with a user.
