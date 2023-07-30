from db.connection import db
from bson.objectid import ObjectId


def register_user_schema(user_data, cellphone_id, encrypted_password):
	if user_data["app_1"] == user_data["app_2"]:
		groups = [user_data["app_1"]]
	elif user_data["app_1"] != user_data["app_2"]:
		groups = [user_data["app_1"], user_data["app_2"]]
	
	document = {
		"name": user_data["name"].title(),
		"identity_document": user_data["identity_document"],
		"email": user_data["email"],
		"password": encrypted_password,
		"cellphone_id": ObjectId(cellphone_id),
		"groups": groups
	}

	return document