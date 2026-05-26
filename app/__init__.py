from dotenv import load_dotenv
load_dotenv()
import os
from flask import Flask, redirect, url_for
from app.blueprints.model import db
from app.blueprints.user import user
from app.blueprints.admin import admin
from app.blueprints.auth import auth
from app.blueprints.invoice import invoice

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "abcdefghijklmnop")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI","sqlite:///shop.db")

    db.init_app(app)

    app.register_blueprint(user)
    app.register_blueprint(admin)
    app.register_blueprint(auth)
    app.register_blueprint(invoice)

    @app.route("/")
    def index():
        return redirect(url_for("auth.login"))
    
    with app.app_context():
        db.create_all()
    return app
