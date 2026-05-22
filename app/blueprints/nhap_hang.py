from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from app.blueprints.model import db, TaiKhoan, LoaiSanPham, SanPham, HoaDon, PhieuNhap, ChiTietHoaDon, ChiTietPhieuNhap
from datetime import datetime

nhap_hang = Blueprint("nhap_hang", __name__)

@nhap_hang.route("/nhap-hang", methods=["GET", "POST"])
def nhan_du_lieu_nhap_hang():
    if request.method == "POST":
        try:
            loai_nhap = request.form.get("loai_nhap")
            so_luong = int(request.form.get("so_luong"))
            don_gia = int(request.form.get("don_gia"))
            
            if loai_nhap == "moi":
                ma_san_pham = request.form.get("ma_san_pham")
                ten_san_pham = request.form.get("ten_san_pham")
                mo_ta = request.form.get("mo_ta", "")
                gia_ban = int(request.form.get("gia_ban", 0))
                id_loai_san_pham = int(request.form.get("id_loai_san_pham"))
                img_url = request.form.get("img_url", "") 
                
                san_pham_ton_tai = SanPham.query.filter_by(ma_san_pham == ma_san_pham).first()
                if san_pham_ton_tai:
                    return f"Lỗi: Mã sản phẩm '{ma_san_pham}' đã tồn tại trong hệ thống!", 400

                # Tạo sản phẩm mới với số lượng tồn kho ban đầu = 0 (sẽ được cộng dồn ở bước sau)
                moi_san_pham = SanPham(
                    ma_san_pham=ma_san_pham,
                    ten_san_pham=ten_san_pham,
                    mo_ta=mo_ta,
                    gia_nhap=don_gia,
                    gia_ban=gia_ban,
                    so_luong_ton_kho=0,
                    img_url=img_url,
                    id_loai_san_pham=id_loai_san_pham
                )
                db.session.add(moi_san_pham)
                db.session.flush() 
                id_san_pham = moi_san_pham.id_san_pham


            else:
                id_san_pham = int(request.form.get("id_san_pham"))

            # --- BẮT ĐẦU QUY TRÌNH TẠO PHIẾU NHẬP (Áp dụng cho cả cũ lẫn mới) ---
            tong_tien = so_luong * don_gia
            ngay_nhap = datetime.now()
            
            # 1. Tạo Phiếu Nhập
            moi_phieu_nhap = PhieuNhap(tong_tien=tong_tien, ngay_nhap=ngay_nhap)
            db.session.add(moi_phieu_nhap)
            db.session.flush() 
            
            # 2. Tạo Chi Tiết Phiếu Nhập
            moi_chi_tiet = ChiTietPhieuNhap(
                don_gia=don_gia,
                so_luong=so_luong,
                id_phieu=moi_phieu_nhap.id_phieu,
                id_san_pham=id_san_pham
            )
            db.session.add(moi_chi_tiet)
            
            # 3. Cập nhật số lượng tồn kho của Sản Phẩm
            san_pham = SanPham.query.get(id_san_pham)
            if san_pham:
                if san_pham.so_luong_ton_kho is None:
                    san_pham.so_luong_ton_kho = 0
                san_pham.so_luong_ton_kho += so_luong
                # Cập nhật luôn giá nhập mới nhất cho sản phẩm nếu muốn
                san_pham.gia_nhap = don_gia 
            
            # Lưu toàn bộ vào Database
            db.session.commit()
            return redirect(url_for("nhap_hang.nhan_du_lieu_nhap_hang"))
            
        except Exception as e:
            db.session.rollback()
            return f"Đã xảy ra lỗi: {str(e)}", 500

    if request.method == "GET":
        # Lấy dữ liệu cho phương thức GET (Màn hình chính)
        danh_sach_san_pham = SanPham.query.all()
        # Bạn cần lấy thêm danh sách loại sản phẩm để người dùng chọn khi thêm sản phẩm mới
        danh_sach_loai = LoaiSanPham.query.all() 
        return render_template("nhap_hang.html", 
                           danh_sach_san_pham=danh_sach_san_pham, 
                           danh_sach_loai=danh_sach_loai)