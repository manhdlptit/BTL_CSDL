from dotenv import load_dotenv
load_dotenv()
import os
from flask import Flask
from app.blueprints.model import db
from app.blueprints.api import tab_api
from app.blueprints.nhap_hang import nhap_hang

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "abcdefghijklmnop")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI","sqlite:///shop.db")

    db.init_app(app)

    app.register_blueprint(tab_api)
    app.register_blueprint(nhap_hang)

    with app.app_context():
        db.create_all()
    return app
