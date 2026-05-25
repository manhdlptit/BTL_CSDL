from flask import Blueprint, jsonify, request, render_template, redirect, url_for, session
from app.blueprints.model import db, TaiKhoan, LoaiSanPham, SanPham, HoaDon, PhieuNhap, ChiTietHoaDon, ChiTietPhieuNhap
from datetime import datetime

admin = Blueprint("admin", __name__)

@admin.route("/nhap-hang", methods=["GET", "POST"])
def nhan_du_lieu_nhap_hang():
    if request.method == "POST":
        try:
            loai_nhap = request.form.get("loai_nhap")
            so_luong = int(request.form.get("so_luong"))
            don_gia = int(request.form.get("don_gia"))
            
            if loai_nhap == "moi":
                ma_san_pham = request.form.get("ma_san_pham")
                ten_san_pham = request.form.get("ten_san_pham")
                kich_co = request.form.get("kich_co")
                mo_ta = request.form.get("mo_ta", "")
                gia_ban = int(request.form.get("gia_ban", 0))
                id_loai_san_pham = int(request.form.get("id_loai_san_pham"))
                img_url = request.form.get("img_url", "") 
                
                san_pham_ton_tai = SanPham.query.filter_by(ma_san_pham=ma_san_pham).first()
                if san_pham_ton_tai:
                    return f"Lỗi: Mã sản phẩm '{ma_san_pham}' đã tồn tại trong hệ thống!", 400

                san_pham_moi = SanPham(
                    ma_san_pham=ma_san_pham,
                    ten_san_pham=ten_san_pham,
                    kich_co = kich_co,
                    mo_ta = mo_ta,
                    gia_nhap = don_gia,
                    gia_ban = gia_ban,
                    so_luong_ton_kho = 0,
                    img_url = img_url,
                    id_loai_san_pham = id_loai_san_pham
                )
                db.session.add(san_pham_moi)
                db.session.flush() 
                id_san_pham = san_pham_moi.id_san_pham


            else:
                id_san_pham = int(request.form.get("id_san_pham"))

            tong_tien = so_luong * don_gia
            ngay_nhap = datetime.now()
            
            moi_phieu_nhap = PhieuNhap(tong_tien=tong_tien, ngay_nhap=ngay_nhap)
            db.session.add(moi_phieu_nhap)
            db.session.flush() 
            
            moi_chi_tiet = ChiTietPhieuNhap(
                don_gia=don_gia,
                so_luong=so_luong,
                id_phieu=moi_phieu_nhap.id_phieu,
                id_san_pham=id_san_pham
            )
            db.session.add(moi_chi_tiet)
            
            san_pham = SanPham.query.get(id_san_pham)
            if san_pham:
                if san_pham.so_luong_ton_kho is None:
                    san_pham.so_luong_ton_kho = 0
                san_pham.so_luong_ton_kho += so_luong
                san_pham.gia_nhap = don_gia 
            
            db.session.commit()
            return redirect(url_for("admin.nhan_du_lieu_nhap_hang"))
            
        except Exception as e:
            db.session.rollback()
            return f"Đã xảy ra lỗi: {str(e)}", 500

    if request.method == "GET":
        if not session.get('logged_in'):
            return redirect(url_for('auth.login'))
        if session.get("vai_tro") != "admin":
            return "Bạn không phải là admin, không được phép thực hiện trong trang này"
        danh_sach_san_pham = SanPham.query.all()
        danh_sach_loai = LoaiSanPham.query.all() 
        return render_template("nhap_hang.html", 
                           danh_sach_san_pham=danh_sach_san_pham, 
                           danh_sach_loai=danh_sach_loai)