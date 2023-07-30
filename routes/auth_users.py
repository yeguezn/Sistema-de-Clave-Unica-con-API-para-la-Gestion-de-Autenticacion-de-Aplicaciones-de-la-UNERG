from flask import Blueprint, request, redirect, render_template
import jwt
from datetime import datetime, timedelta, timezone
from werkzeug.security import check_password_hash as checkph
from config import configure
import os
from db.connection import db
import re
from regex import EMAIL_REGEX
from helper import get_authorized_users, get_app_redirect_uri, is_enabled, get_app_signature

configure()
auth = Blueprint("auth", __name__)

def get_user_data(email):

    user_data = db.users_accounts.aggregate([
            
        {
            "$match":{
                "email":email
            }
        },
            
        {
            "$lookup":{
                "from":"cellphone", 
                "localField":"cellphone_id", 
                "foreignField":"_id", 
                "as": "cellphone"
            }
        },

        {
            "$project":{
                "_id":0,
                "identity_document":0,
                "cellphone_id":0,
                "groups":0,
                "cellphone._id":0
            }
        }
    ])

    return user_data

@auth.route("/login_users/<apikey>")
def login(apikey):
    ctx = {"title":"", "warning":""}

    if not apikey:
        ctx["title"] = "Permiso denegado"
        ctx["warning"] = "Necesita una API KEY para continuar"
        return render_template("warning.html", ctx=ctx)

    if db.developers.count_documents({"api_key":apikey}) == 0:
        ctx["title"] = "Permiso denegado"
        ctx["warning"] = "La API KEY no está asociada a su aplicación"
        return render_template("warning.html", ctx=ctx)

    if not is_enabled(apikey):
        ctx["title"] = "Permiso denegado"
        ctx["warning"] = "En este momento esta aplicación se encuentra deshabilitada"
        return render_template("warning.html", ctx=ctx)
    
    action = "/verify_user_data/" + apikey
    return render_template("login.html", action=action)


@auth.route("/verify_user_data/<apikey>", methods=["POST"])
def verify_user_data(apikey):

    if request.form["email"] == "" or request.form["password"] == "":
        return render_template("login.html", 
            warning="Campos vacíos"
        )

    if not re.search(EMAIL_REGEX, request.form["email"]):
        return render_template("login.html", 
            warning="Correo electrónico no válido"
        )

    if request.form["email"] not in get_authorized_users(apikey):
        return render_template("login.html", 
            warning="Usted no está autorizado para accesar a esta aplicación"
        )

    user_data = get_user_data(request.form["email"])
    
    if user_data is None:
        return render_template("login.html",
            warning="Usted no está registrado"
        )

    user_data = list(user_data)

    if "password" not in list(user_data[0].keys()):
       return render_template("login.html",
            warning="Contraseña incorrecta, si el error persiste intente iniciar sesión por otro servicio"
        )

    if not checkph(user_data[0]["password"], request.form["password"]):
        return render_template("login.html",
            warning="Contraseña incorrecta"
        )

    signature = get_app_signature(apikey)

    token = jwt.encode({
        "user_email":user_data[0]["email"],
        "user_name": user_data[0]["name"],  
        "exp":(datetime.now(tz=timezone.utc) + timedelta(minutes=1))},
        signature
    )

    redirect_uri = get_app_redirect_uri(apikey, token)

    return redirect(redirect_uri)