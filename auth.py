from time import timezone
from datetime import datetime, timezone, timedelta

import jwt
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth_bp = Blueprint("auth", __name__)

#register route
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error':'password or username required'}), 400

    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({'error':'Username already taken'}), 409

    hashed_password = generate_password_hash(data['password'])
    new_user = User(username=data['username'], password_hash=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message':'new user created successfully'}), 201

#login route
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400

    user = User.query.filter_by(username=data['username']).first()

    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error':'Invalid username or password'}), 401

    #creates a signed token
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.now(timezone.utc) + timedelta(hours=24) #token expires after 24 Hours
    }, current_app.config['SECRET_KEY'], algorithm='HS256') #Same secret key as in app.py, it signs the token #HMAC using SHA-256, a standard symmetric-signing algorithm for JWTs, same key both signs and verifies.

    return jsonify({'token': token}), 200