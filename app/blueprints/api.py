from dotenv import load_dotenv
load_dotenv()
from app.blueprints.model import SanPham
from flask import Blueprint, redirect, url_for, render_template


tab_api = Blueprint("tab_api", __name__)

@tab_api.route("/")
@tab_api.route("/san-pham")
def san_pham():
    nhieu_san_pham = SanPham.query.all()
    return render_template("san_pham.html", nhieu_san_pham = nhieu_san_pham)



@tab_api.route("/them-hang")
def them_hang():
    return render_template("them_hang.html")
    


