from functools import wraps
import jwt
from db.connection import db
from flask import request, jsonify
from config import configure
import os
import re
from regex import EMAIL_REGEX

configure()
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify({'message' : 'Token sin especificar !!'}), 401

        try:
            
            user_data = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
            current_user = db.admin.find_one({"email":user_data["sub"]})
        except:
            return jsonify({
                'message' : 'Token invalido !!'
            }), 401

        return f(current_user, *args, **kwargs)
  
    return decorated

def email_parameter_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.args.get("email") is None:
            return jsonify({"msg":"Correo electrónico sin especificar"})

        if not re.search(EMAIL_REGEX, request.args.get("email")):
            return jsonify({"msg":"Correo electrónico no válido"})

        if db.users_accounts.count_documents({"email":request.args.get("email")}) == 0:
            return jsonify({"msg":"Correo electrónico no registrado"})

        return f(*args, **kwargs)

    return decorated

def apikey_parameter_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        
        if request.args.get("api_key") is None:
            return jsonify({"msg":"API KEY sin especificar"})

        if db.developers.count_documents({"api_key":request.args.get("api_key")}) == 0:
            return jsonify({"msg":"La API KEY proporcionada no está asignada a ninguna aplicación"})

        return f(*args, **kwargs)

    return decorated

def get_authorized_users(apikey):
    app_data = db.developers.aggregate([
        {
            "$match":{
                "api_key":apikey
            }
        },

        {
            "$project":{
                "_id":0,
                "app_name":0,
                "api_key":0,
                "redirect_uri":0
            }
        }
    ])
    
    app_data = list(app_data)

    return app_data[0]["user_group"]

def get_app_name(api_key):
    app_data = db.developers.aggregate([
        {
            "$match":{
                "api_key":api_key
            }
        },

        {
            "$project":{
                "_id":0,
                "api_key":0,
                "user_group":0,
                "redirect_uri":0
            }
        }
    ])

    app_data = list(app_data)
    return app_data[0]["app_name"]

def get_app_redirect_uri(apikey, token):
    app_data = db.developers.aggregate([
        {
            "$match":{
                "api_key":apikey
            }
        },
        {
            "$project":{
                "_id":0, 
                "api_key":0, 
                "app_name":0, 
                "user_group":0
            }
        }
    ])

    app_data = list(app_data)

    redirect_uri = app_data[0]["redirect_uri"]

    if "?" not in redirect_uri:
        redirect_uri = redirect_uri + "?token=" + token

    elif "&" not in redirect_uri and "?" in redirect_uri:

        redirect_uri = redirect_uri + "&token=" + token

    elif "&" in redirect_uri and "?" in redirect_uri:

        redirect_uri = redirect_uri + "&token=" + token

    return redirect_uri

def register_cellphone(cellphone_number):

    if db.cellphone.count_documents({"cellphone_number":cellphone_number}) == 0:
        db.cellphone.insert_one({"cellphone_number":cellphone_number})

    cellphone = db.cellphone.find_one({"cellphone_number":cellphone_number})
    return cellphone["_id"]

def is_enabled(api_key):
    app_data = db.developers.aggregate([
        {
            "$match":{
                "api_key":api_key
            }
        },

        {

            "$project":{
                "_id":0,
                "app_name":0,
                "redirect_uri":0,
                "user_group":0,
                "api_key":0
            }

        }
    ])

    app_data = list(app_data)

    return app_data[0]["enabled"]

def get_app_signature(api_key):
    app_data = db.developers.aggregate([
        {
            "$match":{
                "api_key":api_key
            }
        },

        {

            "$project":{
                "_id":0,
                "app_name":0,
                "redirect_uri":0,
                "user_group":0,
                "api_key":0,
                "enabled":0
            }

        }
    ])

    app_data = list(app_data)

    return app_data[0]["signature"]