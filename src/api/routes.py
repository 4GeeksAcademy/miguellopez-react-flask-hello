"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, JWTManager,get_jwt_identity, jwt_required

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

@api.route("/crear_usuario", methods =["POST"])
def crear_usuario():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(email=email,password=password).first()
    if user:
        return jsonify ({"msg":"Este usuario ya existe"}), 401
    user_new = User(email=email,password=password)
    db.session.add(user_new)
    db.session.commit()
    return jsonify({"msg":"Usuario creado"}), 200

@api.route("/iniciar_sesion", methods =["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(email=email,password=password).first()
    if user is None:
        return jsonify({"msg":"Usuario no encontrado"}), 401
    access_token = create_access_token(identity = user.id)
    return jsonify({"token":access_token,"user.id":user.id}), 200

@api.route("/protected" , methods = ["GET"])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user is None:
        return APIException("Usuario no encontrado", status_code = 404)
    return jsonify("Usuario autenticado"),200