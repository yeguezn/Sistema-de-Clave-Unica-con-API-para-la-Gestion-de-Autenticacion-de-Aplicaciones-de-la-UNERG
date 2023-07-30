from db.connection import db
from bson.objectid import ObjectId


def google_schema(user_data, cellphone_id, api_key):
	
	document = {
		"name": user_data["name"].title(),
		"identity_document": user_data["identity_document"],
		"email": user_data["email"],
		"cellphone_id": ObjectId(cellphone_id),
		"groups": [api_key]
	}

	return document