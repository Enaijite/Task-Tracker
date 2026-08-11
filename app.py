from flask import Flask
from models import db

app = Flask(__name__)#Application instance is created using the Flask class

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'#tells SQLAlchemy where the database is located, tasks.db in the current directory.
app.config['SECRET_KEY'] = 'P@}K@y&ZKTfVYt@oXD['#secret key is used for securely signing the session cookie.

db.init_app(app)#connects the Flask application to the SQLAlchemy database instance.

#creates the database tables based on the models in models.py.
#This is done within the application context to ensure that the database operations are performed in the context of the Flask application.
with app.app_context():
    db.create_all() 

#app.route('/') is a decorator that tells the function below to run when someone visits,
#the root of the web application.
@app.route('/')
def index():
    return {'message': 'Task tracker API running'}

#starts the Flask development server
#debug=True provides detailed error messages and auto reload when changes are made to code
if __name__ == '__main__':
    app.run(debug=True)