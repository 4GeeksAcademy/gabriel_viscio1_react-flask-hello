"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200
@api.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data['email']
    password = data['password']
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"message": "Usuario ya registrado"}), 400

    new_user = User(email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuario registrado con éxito"}), 201

@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        return jsonify({"message": "Credenciales incorrectas"}), 401

    token = jwt.encode(
        {'user_id': user.id, 'exp': datetime.utcnow() + timedelta(hours=1)},
        app.config['SECRET_KEY'],
        algorithm='HS256'
    )

    return jsonify({'token': token})
@api.route('/validate', methods=['GET'])
def validate_token():
    token = request.headers.get('Authorization').split()[1]
    try:
        decoded_token = jwt.decode(token, api.config['SECRET_KEY'], algorithms=['HS256'])
        user = User.query.get(decoded_token['user_id'])
        return jsonify({"id": user.id, "email": user.email}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token expirado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Token inválido"}), 401
@api.route('/logout', methods=['POST'])
def handle_logout():
    # Lógica para invalidar el token (si es necesario)
    return jsonify({"message": "Cierre de sesión exitoso"}), 200
