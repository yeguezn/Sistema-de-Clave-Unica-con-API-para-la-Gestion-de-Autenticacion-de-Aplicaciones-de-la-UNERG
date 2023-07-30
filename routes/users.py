from flask import Blueprint, render_template, request, jsonify
from db.connection import db
from werkzeug.security import generate_password_hash as genph
from werkzeug.security import check_password_hash as checkph
from db.schemas.register_user import register_user_schema
from regex import IDENTITY_DOCUMENT_REGEX, CELLPHONE_REGEX, EMAIL_REGEX 
import re
from helper import get_app_name, token_required, email_parameter_required, apikey_parameter_required
from helper import register_cellphone

users = Blueprint("users", __name__)

@users.route("/register_users", methods=["POST"])
@token_required
def register_users(current_user):
	if not re.search(IDENTITY_DOCUMENT_REGEX, request.json["identity_document"]):
		return jsonify({"msg":"Número de cédula no válido"}), 401

	if not re.search(CELLPHONE_REGEX, request.json["cellphone"]):
		return jsonify({"msg":"Número de telefono no válido"}), 401

	if not re.search(EMAIL_REGEX, request.json["email"]):
		return jsonify({"msg":"Correo electrónico no válido"}), 401

	if request.json["password"] != request.json["confirm_password"]:
		return jsonify({"msg":"Las contraseñas no coinciden"}), 401

	if db.users_accounts.count_documents({"identity_document": request.json["identity_document"]}) == 1:
		return jsonify({"msg":"La cédula ingresada ya está registrada"}), 401

	if db.users_accounts.count_documents({"email":request.json["email"]}) == 1:
		return jsonify({"msg":"El correo electrónico ingresado ya está registrado"}), 401

	if request.json["app_1"] == "" and request.json["app_2"] == "":
		return jsonify({"msg":"Debe solicitar al menos acceso a una aplicación"}), 401

	if db.developers.count_documents({"api_key":request.json["app_1"]}) == 0:
		return jsonify({
			"msg":"La API KEY ingresada en el campo app_1 no está asociada a ninguna aplicación"
		}), 401

	if db.developers.count_documents({"api_key":request.json["app_2"]}) == 0:
		return jsonify({
			"msg":"La API KEY ingresada en el campo app_2 no está asociada a ninguna aplicación"
		}), 401

	cellphone_id = register_cellphone(request.json["cellphone"])
	encrypted_password = genph(request.json["password"])
	document = register_user_schema(request.json, cellphone_id, encrypted_password)
	db.users_accounts.insert_one(document)
	return jsonify({"msg":"registro exitoso"})

@users.route("/delete_user", methods=["DELETE"])
@token_required
@email_parameter_required
def delete_user(current_user):
	db.users_accounts.delete_one({"email":request.args.get("email")})
	msg = f"El usuario con el email {request.args.get('email')} ha sido eliminado"
	return jsonify({"msg":msg})

@users.route("/request_aplication", methods=["PUT"])
@token_required
@email_parameter_required
@apikey_parameter_required
def request_aplication(current_user):
	
	db.users_accounts.update_one(
		{"email":request.args.get("email")},  
		{"$push": {"groups":request.args.get("api_key")}}
	)

	app_name = get_app_name(request.args.get("api_key"))
	email = request.args.get("email")
	msg = f"El usuario {email} ha solicitado permiso para accesar a la aplicación {app_name}"

	return jsonify({"msg":msg})
