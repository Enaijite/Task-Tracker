import jwt
from functools import wraps
from flask import request, jsonify, current_app
from models import User

#decorator function that takes another function(f) as an argument
#takes function, comfirms if user is authenticated by checking for a valid JWT token in the request headers 
#then calls the original function(f) with the current user as an argument if the token is valid.
def token_required(f):
    @wraps(f)#decorator that preserves the original function's metadata, such as its name, when it is wrapped by another function.
    def decorated(*args, **kwargs):
        token = None

        #gets token from HTTP header and splits returned value to get the token alone
        # e.g Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        #verifying token
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(payload['user_id'])
            if not current_user:
                return jsonify({'error':'User not found'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'error':'Token has Expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error':'Invalid Token'}), 401

        return f(current_user, *args, **kwargs)

    return decorated
            
