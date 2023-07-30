from flask import Flask, abort, render_template, jsonify
from routes.users import users
from routes.auth_users import auth
from routes.aplications import aplications
from routes.google_auth import google_auth
from routes.authorize_users import authorization
from routes.admin import admin
from routes.queries import queries
from config import configure
import os
from flask_swagger_ui import get_swaggerui_blueprint


configure()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'

SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "API autenticación"
    }
)

#Registering routes
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
app.register_blueprint(users)
app.register_blueprint(auth)
app.register_blueprint(aplications)
app.register_blueprint(google_auth)
app.register_blueprint(authorization)
app.register_blueprint(admin)
app.register_blueprint(queries)

if __name__ == "__main__":
	url = "sso.unerg.com:5000"
	app.config["SERVER_NAME"] = url
	app.run(debug=True, ssl_context="adhoc")