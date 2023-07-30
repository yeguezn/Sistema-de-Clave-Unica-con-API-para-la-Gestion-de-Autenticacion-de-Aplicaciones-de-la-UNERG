import jwt
from flask import Blueprint, request, jsonify
from db.connection import db
from werkzeug.security import check_password_hash as checkph
from datetime import datetime, timedelta, timezone
import os
import re
from regex import EMAIL_REGEX
from config import configure

configure()
admin = Blueprint("admin", __name__)

@admin.route("/login_admin", methods=["POST"])
def login():
	
    if request.json["email"] == "" or request.json["password"] == "":
	    return jsonify({"msg":"Rellene los campos de correo electrónico y contraseña"})

    if db.admin.count_documents({"email":request.json["email"]}) == 0:
	    return jsonify({"msg":"El correo electrónico que ingresó no está registrado"})

    if not re.search(EMAIL_REGEX, request.json["email"]):
        return jsonify({"msg":"Correo electrónico no válido"})

    admin_data = db.admin.find_one({"email":request.json["email"]})

    if not checkph(admin_data["password"], request.json["password"]):
	    return jsonify({"msg":"Contraseña incorrecta"})

    token = jwt.encode({"sub":admin_data["email"], 
        "exp":(datetime.now(tz=timezone.utc) + timedelta(minutes=30))}, 
		os.getenv("SECRET_KEY")
	)

    return token









