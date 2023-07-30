from flask import Blueprint, request, redirect, jsonify, render_template
import requests
from oauthlib.oauth2 import WebApplicationClient
import json
import os
from config import configure
from db.connection import db
import jwt
from datetime import datetime, timedelta, timezone
import re
from regex import CELLPHONE_REGEX, IDENTITY_DOCUMENT_REGEX
from db.schemas.google import google_schema
from helper import get_authorized_users, get_app_redirect_uri, register_cellphone, is_enabled, get_app_signature

configure()
google_auth = Blueprint("google_auth", __name__)

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
client = WebApplicationClient(GOOGLE_CLIENT_ID)
API_KEY = None

@google_auth.route("/google")
def google():
	global API_KEY
	ctx = {"title":"", "warning":""}
	
	if request.args.get("api_key") is None:
		ctx["title"] = "Permiso denegado"
		ctx["warning"] = "API KEY sin especificar"
		return render_template("warning.html", ctx=ctx)

	if db.developers.count_documents({"api_key": request.args.get("api_key")}) == 0:
		ctx["title"] = "Permiso denegado"
		ctx["warning"] = "La API KEY proporcionada no está asignada a ninguna aplicación"
		return render_template("warning.html", 
			ctx=ctx
		)

	if not is_enabled(request.args.get("api_key")):
		ctx["title"] = "Permiso denegado"
		ctx["warning"] = "En este momento esta aplicación se encuentra deshabilitada"
		return render_template("warning.html", ctx=ctx)

	try:
		google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
		authorization_endpoint = google_provider_cfg['authorization_endpoint']
	except:
		warning = "No fue posible obtener la configuración del proveedor de Google"
		return render_template("warning.html", ctx={"title":"Permiso denegado", "warning":warning})
	
	request_uri = client.prepare_request_uri(
 		authorization_endpoint,
 		redirect_uri=request.base_url + "/callback",
 		scope=["openid", "email", "profile"]
 	)

	API_KEY = request.args.get("api_key")

	return redirect(request_uri)

@google_auth.route("/google/callback")
def callback():
	global API_KEY
	
	try:
		code = request.args.get("code")
		google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
		token_endpoint = google_provider_cfg['token_endpoint']
	except:
		warning = "No fue posible obtener la configuración del proveedor de Google"
		return render_template("warning.html", ctx={"title":"Permiso denegado", "warning":warning})

	token_url, headers, body = client.prepare_token_request(
		token_endpoint,
		authorization_response=request.url,
		redirect_url=request.base_url,
		code=code
	)

	token_response = requests.post(
		token_url,
		headers=headers,
		data=body,
		auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
	)

	client.parse_request_body_response(json.dumps(token_response.json()))

	userinfo_endpoint = google_provider_cfg['userinfo_endpoint']
	uri, headers, body = client.add_token(userinfo_endpoint)
	userinfo_response = requests.get(uri, headers=headers, data=body)

	if not userinfo_response.json().get("email_verified"):
		return "User email not available or not verified by Google.", 400

	user_email = userinfo_response.json()['email']
	user_name = userinfo_response.json()['given_name']

	if db.users_accounts.count_documents({"email":user_email}) == 0:
		return render_template("complete_register.html", 
			ctx={
				"user_email":user_email, 
				"user_name":user_name,
				"identity_document":'',
				"cellphone":''
			}
		)

	if user_email not in get_authorized_users(API_KEY):
		warning = "Usted no tiene permitido el acceso a esta aplicación"
		return render_template("warning.html", 
			ctx={"title":"Permiso denegado", "warning":warning}
		)

	signature = get_app_signature(API_KEY)
	
	token = jwt.encode(
		{
			"user_email":user_email,
			"user_name": user_name, 
			"exp":(datetime.now(tz=timezone.utc) + timedelta(minutes=1))
		},
		signature
	)

	app_redirect_uri = get_app_redirect_uri(API_KEY, token)

	return redirect(app_redirect_uri)
	

@google_auth.route("/complete_register", methods=["POST"])
def complete_register():
	if not re.search(IDENTITY_DOCUMENT_REGEX, request.form["identity_document"]):
		return render_template(
			"complete_register.html",
			ctx={
				"user_email":request.form["email"], 
				"user_name":request.form["name"],
				"identity_document":request.form['identity_document'],
				"cellphone":request.form['cellphone'],
				"warning":"El número de cédula que introdujo no es válido"
			}
		)
	
	if db.users_accounts.count_documents({"identity_document":request.form["identity_document"]}) == 1:
		return render_template(
			"complete_register.html",
			ctx={
				"user_email":request.form["email"], 
				"user_name":request.form["name"],
				"identity_document":request.form['identity_document'],
				"cellphone":request.form['cellphone'],
				"warning": "El número de cedúla que introdujo ya se encuentra registrado"
			}
		)

	if not re.search(CELLPHONE_REGEX, request.form["cellphone"]):
		return render_template(
			"complete_register.html",
			ctx={
				"user_email":request.form["email"], 
				"user_name":request.form["name"],
				"identity_document":request.form['identity_document'],
				"cellphone":request.form['cellphone'],
				"warning":"El número de teléfono que ingresó no es válido"
			}
		)

	cellphone_id = register_cellphone(request.form["cellphone"])
	document = google_schema(request.form, cellphone_id, API_KEY)
	db.users_accounts.insert_one(document)

	warning = "Registro exitoso, debe esperar a ser autorizado para accesar a la aplicación"
	return render_template("warning.html", 
		ctx={"title":"Registro completado", "warning":warning}
	)