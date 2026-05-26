from flask import Blueprint, render_template, session, redirect, url_for
from app.blueprints.model import HoaDon, ChiTietHoaDon

invoice = Blueprint("invoice", __name__)

@invoice.route("/chi-tiet-hoa-don/<int:id_hoa_don>")
def chi_tiet_hoa_don(id_hoa_don):
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))

    hoa_don = HoaDon.query.get(id_hoa_don)
    if not hoa_don:
        return "Không tìm thấy hoá đơn", 404

    id_tai_khoan = session.get('id_tai_khoan')
    vai_tro = session.get('vai_tro')

    if vai_tro != "admin" and hoa_don.id_tai_khoan != id_tai_khoan:
        return "Bạn không có quyền xem hoá đơn này", 403

    chi_tiet = ChiTietHoaDon.query.filter_by(id_hoa_don=id_hoa_don).all()
    return render_template("chi_tiet_hoa_don.html", hoa_don=hoa_don, chi_tiet=chi_tiet)
