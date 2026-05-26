from dotenv import load_dotenv
load_dotenv()
from flask import Blueprint, redirect, url_for, render_template, session, request, jsonify
from app.blueprints.model import SanPham, db, HoaDon, ChiTietHoaDon, TaiKhoan
from datetime import datetime



user = Blueprint("user", __name__, url_prefix="/user")

@user.route("/san-pham")
def san_pham():
    from app.blueprints.auth import auth
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))

    # thong tin user
    du_lieu_user = {
        "ten_dang_nhap" : session.get("ten_dang_nhap"),
        "email": session.get('email'),
        "so_dien_thoai": session.get('so_dien_thoai'),
        "dia_chi": session.get('dia_chi')
    }

    nhieu_san_pham = SanPham.query.all()


    # thanh tim kiem
    tim_kiem = request.args.get("q",'').strip()

    if tim_kiem:
        nhieu_san_pham = SanPham.query.filter(SanPham.ten_san_pham.ilike(f"%{tim_kiem}%")).all()

    # doi du lieu user
    dia_chi = request.form.get("dia_chi")



    return render_template("san_pham.html", nhieu_san_pham = nhieu_san_pham, du_lieu_user = du_lieu_user, tim_kiem = tim_kiem)

@user.route("/thanh-toan", methods=["GET", "POST"])
def thanh_toan():
    if not session.get('logged_in'):
        return jsonify({"success": False, "message": "Bạn cần đăng nhập để thanh toán"}), 401

    if request.method == "GET":
        dia_chi = session.get('dia_chi', '').strip()
        return jsonify({
            "success": True,
            "data": {
                "dia_chi": dia_chi,
                "dia_chi_hop_le": dia_chi and dia_chi != "chua_them"
            }
        })

    elif request.method == "POST":
        try:
            dia_chi = session.get('dia_chi', '').strip()
            if not dia_chi or dia_chi == "chua_them":
                return jsonify({
                    "success": False,
                    "message": "Vui lòng cập nhật địa chỉ giao hàng trước khi thanh toán"
                }), 400

            data = request.get_json()
            items = data.get("items", [])

            if not items:
                return jsonify({"success": False, "message": "Giỏ hàng trống"}), 400

            id_tai_khoan = session.get('id_tai_khoan')

            tong_tien = 0
            for item in items:
                tong_tien += item['price'] * item['soLuong']

            hoa_don = HoaDon(
                id_tai_khoan=id_tai_khoan,
                tong_tien=tong_tien,
                ngay_ban=datetime.now()
            )
            db.session.add(hoa_don)
            db.session.flush()

            for item in items:
                chi_tiet = ChiTietHoaDon(
                    don_gia=item['price'],
                    so_luong=item['soLuong'],
                    id_hoa_don=hoa_don.id_hoa_don,
                    id_san_pham=item['id']
                )
                db.session.add(chi_tiet)

                san_pham = SanPham.query.get(item['id'])
                if san_pham:
                    san_pham.so_luong_ton_kho -= item['soLuong']

            db.session.commit()

            return jsonify({
                "success": True,
                "message": "Thanh toán thành công",
                "hoa_don_id": hoa_don.id_hoa_don,
                "hoa_don_info": {
                    "id_hoa_don": hoa_don.id_hoa_don,
                    "ngay_ban": hoa_don.ngay_ban.strftime('%d/%m/%Y %H:%M:%S'),
                    "tong_tien": hoa_don.tong_tien
                }
            })

        except Exception as e:
            db.session.rollback()
            return jsonify({"success": False, "message": str(e)}), 500

@user.route("/chi-tiet-hoa-don/<int:id_hoa_don>")
def chi_tiet_hoa_don(id_hoa_don):
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))

    hoa_don = HoaDon.query.get(id_hoa_don)
    if not hoa_don:
        return "Không tìm thấy hoá đơn", 404

    if hoa_don.id_tai_khoan != session.get('id_tai_khoan'):
        return "Bạn không có quyền xem hoá đơn này", 403

    chi_tiet = ChiTietHoaDon.query.filter_by(id_hoa_don=id_hoa_don).all()
    return render_template("chi_tiet_hoa_don.html", hoa_don=hoa_don, chi_tiet=chi_tiet)


@user.route("/cap-nhat-thong-tin", methods=["GET", "POST"])
def cap_nhat_thong_tin():
    if not session.get('logged_in'):
        return jsonify({"success": False, "message": "Bạn cần đăng nhập"}), 401

    if request.method == "GET":
        id_tai_khoan = session.get('id_tai_khoan')
        tai_khoan = TaiKhoan.query.get(id_tai_khoan)
        if not tai_khoan:
            return jsonify({"success": False, "message": "Không tìm thấy tài khoản"}), 404

        return jsonify({
            "success": True,
            "data": {
                "ten_dang_nhap": tai_khoan.ten_dang_nhap,
                "email": tai_khoan.email,
                "so_dien_thoai": tai_khoan.so_dien_thoai,
                "dia_chi": tai_khoan.dia_chi
            }
        })

    elif request.method == "POST":
        try:
            data = request.get_json()
            id_tai_khoan = session.get('id_tai_khoan')

            tai_khoan = TaiKhoan.query.get(id_tai_khoan)
            if not tai_khoan:
                return jsonify({"success": False, "message": "Không tìm thấy tài khoản"}), 404

            if 'ten_dang_nhap' in data:
                tai_khoan.ten_dang_nhap = data['ten_dang_nhap']
            if 'email' in data:
                tai_khoan.email = data['email']
            if 'so_dien_thoai' in data:
                tai_khoan.so_dien_thoai = data['so_dien_thoai']
            if 'dia_chi' in data and data['dia_chi'].strip():
                tai_khoan.dia_chi = data['dia_chi'].strip()

            db.session.commit()

            session['ten_dang_nhap'] = tai_khoan.ten_dang_nhap
            session['email'] = tai_khoan.email
            session['so_dien_thoai'] = tai_khoan.so_dien_thoai
            session['dia_chi'] = tai_khoan.dia_chi

            return jsonify({"success": True, "message": "Cập nhật thông tin thành công"})

        except Exception as e:
            db.session.rollback()
            return jsonify({"success": False, "message": str(e)}), 500