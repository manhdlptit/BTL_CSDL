from dotenv import load_dotenv
load_dotenv()
from flask import Blueprint, request, redirect, url_for, render_template, jsonify, session
from werkzeug.security import check_password_hash, generate_password_hash
from app.blueprints.model import TaiKhoan, db
from app.blueprints.user import user
from app.blueprints.admin import admin

auth = Blueprint("auth", __name__)

@auth.route("/login", methods = ["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        find_username = TaiKhoan.query.filter(TaiKhoan.ten_dang_nhap == username).first()

        if find_username is None:
            return "Không tìm thấy user_name" 
        if not check_password_hash(find_username.mat_khau, password):
            return "Sai mật khẩu"
        thong_tin = {
            "ten_dang_nhap" : find_username.ten_dang_nhap,
            "email" : find_username.email,
            "so_dien_thoai" : find_username.so_dien_thoai,
            "dia_chi" : find_username.dia_chi,
            "vai_tro" : find_username.vai_tro
            }  
        if find_username.vai_tro == "admin":
            session['logged_in'] = True
            session['vai_tro'] = thong_tin["vai_tro"]
            return redirect(url_for("admin.nhan_du_lieu_nhap_hang"))
        if find_username.vai_tro == "user":
            session['logged_in'] = True
            session['id_tai_khoan'] = find_username.id_tai_khoan
            session['ten_dang_nhap'] = thong_tin["ten_dang_nhap"]
            session['email'] = thong_tin["email"]
            session['so_dien_thoai'] = thong_tin["so_dien_thoai"]
            session['dia_chi'] = thong_tin["dia_chi"]
            return redirect(url_for("user.san_pham"))
        
    if request.method == "GET":
        return render_template("login.html")

@auth.route("/signup", methods = ["GET","POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        phone_number = request.form.get("phone_number")
        password = request.form.get("password")
        check_password = request.form.get("check_password")

        find_email = TaiKhoan.query.filter(TaiKhoan.email == email).first()
        find_username = TaiKhoan.query.filter(TaiKhoan.ten_dang_nhap == username).first()
        find_phone_number = TaiKhoan.query.filter(TaiKhoan.so_dien_thoai == phone_number).first()

        if find_email is not None:
            return "email đã tồn tại trong hệ thống"    
        if find_username is not None:
            return "username đã tồn tại trong hệ thống"  
        if find_phone_number is not None:
            return "số điện thoại đã tồn tại trong hệ thống"     
        if len(username) > 30:
            return "username phải nhỏ hơn 30 ký tự"     
        if len(password) > 16 or len(password)<8:
            return "mật khẩu chỉ từ 8 - 16 ký tự"
        if password != check_password:
            return "mat khau va kiem tra mat khau khong trung nhau"   
        gen_password = generate_password_hash(password)
        new_user = TaiKhoan(email=email,ten_dang_nhap=username, so_dien_thoai= phone_number, mat_khau=gen_password, vai_tro="user", dia_chi= "chua_them")
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("auth.login"))
    return render_template("signup.html")


@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))