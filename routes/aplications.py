from flask import Blueprint, request, jsonify, render_template
import secrets
from db.connection import db
from db.schemas.register_aplications import aplications_schema
from helper import token_required, get_app_name, apikey_parameter_required
from regex import REDIRECT_URI_REGEX
import re

aplications = Blueprint("aplications", __name__)

@aplications.route("/register_aplications", methods=["POST"])
@token_required
def register_aplications(current_user):

	if db.developers.count_documents({"redirect_uri":request.json["redirect_uri"]}) > 0:
		return jsonify({"msg":"La URL ingresada ya está registrada"}), 401

	if not re.search(REDIRECT_URI_REGEX, request.json["redirect_uri"]):
		return jsonify({"msg": "URL no válida"}), 401
	  
	api_key = secrets.token_hex(20)
	signature = secrets.token_hex(20)
	document = aplications_schema(request.json, api_key, signature)
	db.developers.insert_one(document)
	return jsonify({"msg":f"""su API key para consumir el servicio es: {api_key}. Para acceder al login
	use la siguiente URI: https://sso.unerg.com:5000/login_users/?api_key. Para autenticar a sus usuarios 
	a través de servicios de google use la siguiente URI: sso.unerg.com:5000/google?api_key. Y
	su clave secreta para decodificar tokens con los datos de sus usuarios es: {signature}"""})

@aplications.route("/delete_aplication", methods=["DELETE"])
@token_required
@apikey_parameter_required
def delete_aplication(current_user):
	app_name = get_app_name(request.args.get("api_key"))
	db.developers.delete_one({"api_key":request.args.get("api_key")})
	msg = f"La aplicación {app_name} ha sido eliminada"

	return jsonify({"msg":msg})

@aplications.route("/enable_aplication", methods=["PUT"])
@token_required
@apikey_parameter_required
def enable_aplication(current_user):
	app_name = get_app_name(request.args.get("api_key"))
	db.developers.update_one({"api_key":request.args.get("api_key")}, {"$set":{"enabled":True}})
	msg = f"La aplicación {app_name} ha sido habilitada"

	return jsonify({"msg":msg})

@aplications.route("/disable_aplication", methods=["PUT"])
@token_required
@apikey_parameter_required
def disable_aplication(current_user):
	app_name = get_app_name(request.args.get("api_key"))
	db.developers.update_one({"api_key":request.args.get("api_key")}, {"$set":{"enabled":False}})
	msg = f"La aplicación {app_name} ha sido deshabilitada"

	return jsonify({"msg":msg})


	
	