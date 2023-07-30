from flask import Blueprint, jsonify, request
from db.connection import db
from helper import token_required, email_parameter_required, apikey_parameter_required
from regex import EMAIL_REGEX
import re

queries = Blueprint("queries", __name__)

@queries.route("/get_users")
@token_required
def get_users(current_user):
	pipeline = [
		{
			"$lookup":{
				"from":"developers",
				"localField": "groups",
				"foreignField": "api_key",
				"as": "aplications"
			}
		},
		
		{
			"$lookup":{
				"from":"cellphone",
				"localField": "cellphone_id",
				"foreignField": "_id",
				"as": "cellphone"
			}
		},

		{
			"$project":{
				"password": 0,
				"_id": 0,
				"groups":0,
				"cellphone_id":0,
				"aplications.api_key": 0,
				"aplications.redirect_uri": 0,
				"aplications._id": 0,
				"aplications.user_group": 0,
				"cellphone._id": 0
			}
		}
	]

	users = []
	
	for user in db.users_accounts.aggregate(pipeline):
		users.append(user)

	return jsonify(users)

@queries.route("/get_user")
@token_required
@email_parameter_required
def get_user(current_user):
	
	pipeline = [
		{
			"$lookup":{
				"from":"developers",
				"localField": "groups",
				"foreignField": "api_key",
				"as": "aplications"
			}
		},
		
		{
			"$lookup":{
				"from":"cellphone",
				"localField": "cellphone_id",
				"foreignField": "_id",
				"as": "cellphone"
			}
		},

		{
			"$project":{
				"password": 0,
				"_id": 0,
				"groups":0,
				"cellphone_id":0,
				"aplications.api_key": 0,
				"aplications.redirect_uri": 0,
				"aplications._id": 0,
				"aplications.user_group": 0,
				"cellphone._id": 0
			}
		},

		{
			"$match":{
				"email": request.args.get("email")
			}
		}
	]

	user = db.users_accounts.aggregate(pipeline)

	return jsonify(list(user))


@queries.route("/get_aplications")
@token_required
def get_aplications(current_user):
	pipeline = [
		{
			"$lookup":{
				"from":"users_accounts",
				"localField": "user_group",
				"foreignField": "email",
				"as": "authorized_users"
			}
		},

		{
			"$project":{
				"authorized_users.password": 0,
				"authorized_users.name": 0,
				"authorized_users.identity_document": 0,
				"authorized_users._id": 0,
				"authorized_users.cellphone_id": 0,
				"authorized_users.groups": 0,
				"_id": 0,
				"authorized_users.group":0,
				"api_key": 0,
				"redirect_uri": 0,
				"user_group": 0,

				
			}
		}
	]

	aplications = []
	
	for aplication in db.developers.aggregate(pipeline):
		aplications.append(aplication)

	return jsonify(aplications)

@queries.route("/get_aplication")
@token_required
@apikey_parameter_required
def get_aplication(current_user):	
	pipeline = [
		{
			"$lookup":{
				"from":"users_accounts",
				"localField": "user_group",
				"foreignField": "email",
				"as": "authorized_users"
			}
		},

		{
			"$project":{
				"authorized_users.password": 0,
				"authorized_users.name": 0,
				"authorized_users.identity_document": 0,
				"authorized_users._id": 0,
				"authorized_users.cellphone_id": 0,
				"authorized_users.groups": 0,
				"_id": 0,
				"authorized_users.group":0,
				"user_group": 0,

				
			}
		},

		{
			"$match":{
				"api_key": request.args.get("api_key")
			}
		}
	]

	aplication = db.developers.aggregate(pipeline)

	return jsonify(list(aplication))