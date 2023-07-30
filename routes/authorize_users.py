from flask import Blueprint, jsonify, request
from db.connection import db
from helper import token_required, get_authorized_users, get_app_name
from helper import email_parameter_required, apikey_parameter_required
from regex import EMAIL_REGEX
import re

authorization = Blueprint("authorization", __name__)

def get_app_access_request(email):
	
	app_access_request = db.users_accounts.aggregate([
		{
			"$match":{
				"email":email
			}
		},

		{
			"$project":{
				"_id":0,
				"name":0,
				"identity_document":0,
				"email":0,
				"cellphone_id":0
			}
		}
	])

	app_access_request = list(app_access_request)
	return app_access_request[0]["groups"]
	

@authorization.route("/authorization_user", methods=["PUT"])
@token_required
@email_parameter_required
@apikey_parameter_required
def authorization_user(current_user):
	email = request.args.get("email")
	api_key = request.args.get('api_key')

	if email in get_authorized_users(api_key):
		msg = f"""El usuario {email} ya ha sido autorizado para accesar a la aplicación
		{get_app_name(api_key)}"""
		return jsonify({"msg":msg})

	if api_key not in get_app_access_request(email):
		msg = f"""El usuario {email} no ha solicitado accesar a la aplicación
		{get_app_name(api_key)}"""
		return jsonify({"msg":msg})
		
	db.developers.update_one(
		{"api_key":api_key},
		{"$push": {"user_group":email}}
	)

	app_name = get_app_name(api_key)
	msg = f"El usuario {email} ha sido autorizado para usar la aplicación {app_name}"
	return jsonify({"msg":msg})

@authorization.route("/reject_user", methods=["PUT"])
@token_required
@email_parameter_required
@apikey_parameter_required
def reject(current_user):

	email = request.args.get("email")
	api_key = request.args.get('api_key')

	if api_key not in get_app_access_request(email):
		msg = f"""El usuario {email} no ha solicitado accesar a la aplicación
		{get_app_name(api_key)}"""
		return jsonify({"msg":msg})
	
	db.developers.update_one(
		{"api_key":api_key},
		{"$pull": {"user_group":email}}
	)

	db.users_accounts.update_one(
		{"email":request.args.get("email")},  
		{"$pull": {"groups":api_key}}
	)

	app_name = get_app_name(api_key)
	msg = f"El usuario {email} no ha sido autorizado para usar la aplicación {app_name}"
	return jsonify({"msg":msg})
