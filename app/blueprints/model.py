from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class TaiKhoan(db.Model):
    __tablename__ = "tai_khoan"
    
    id_tai_khoan = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)        
    vai_tro = db.Column(db.String(5), nullable=False)          
    ten_dang_nhap = db.Column(db.String(16), nullable=False) 
    mat_khau = db.Column(db.String(255), nullable=False)

    def __init__(self, email, vai_tro, ten_dang_nhap, mat_khau):
        self.email = email
        self.vai_tro = vai_tro
        self.ten_dang_nhap = ten_dang_nhap
        self.mat_khau = mat_khau

class LoaiSanPham(db.Model):
    __tablename__ = "loai_san_pham"
    id_loai_san_pham = db.Column(db.Integer, primary_key = True)
    ten_loai_san_pham  = db.Column(db.String(50))

    def __init__(self, ten_loai_san_pham):
        self.ten_loai_san_pham = ten_loai_san_pham

class SanPham(db.Model):
    __tablename__ = "san_pham"
    id_san_pham = db.Column(db.Integer, primary_key = True)
    ma_san_pham  = db.Column(db.String(20))
    ten_san_pham  = db.Column(db.String(100))
    mo_ta = db.Column(db.String(500))
    gia_nhap = db.Column(db.Integer)
    gia_ban = db.Column(db.Integer)
    so_luong_ton_kho = db.Column(db.Integer)
    img_url = db.Column(db.String(500))
    id_loai_san_pham = db.Column(db.Integer, db.ForeignKey('loai_san_pham.id_loai_san_pham'), nullable=False)
    loai_san_pham = db.relationship('LoaiSanPham', backref=db.backref('danh_sach_san_pham', lazy=True))
    
    def __init__(self, ma_san_pham, ten_san_pham, mo_ta, gia_nhap, gia_ban, so_luong_ton_kho, img_url, id_loai_san_pham):
        self.ma_san_pham = ma_san_pham
        self.ten_san_pham = ten_san_pham
        self.mo_ta = mo_ta
        self.gia_nhap = gia_nhap
        self.gia_ban = gia_ban
        self.so_luong_ton_kho = so_luong_ton_kho
        self.img_url = img_url
        self.id_loai_san_pham = id_loai_san_pham

class HoaDon(db.Model):
    __tablename__ = "hoa_don"
    
    id_hoa_don = db.Column(db.Integer, primary_key=True)  
    ngay_ban = db.Column(db.DateTime)
    tong_tien = db.Column(db.Integer,)
    id_tai_khoan = db.Column(db.Integer, db.ForeignKey('tai_khoan.id_tai_khoan'), nullable=False)
    tai_khoan = db.relationship('TaiKhoan', backref=db.backref('danh_sach_hoa_don', lazy=True))
        
    def __init__(self, id_tai_khoan, tong_tien, ngay_ban):
        self.id_tai_khoan = id_tai_khoan
        self.tong_tien = tong_tien
        self.ngay_ban = ngay_ban

class PhieuNhap(db.Model):
    __tablename__ = "phieu_nhap"
    
    id_phieu = db.Column(db.Integer, primary_key=True) 
    tong_tien = db.Column(db.Integer, nullable=False)
    ngay_nhap = db.Column(db.DateTime, nullable=False)

    def __init__(self, tong_tien, ngay_nhap):
        self.tong_tien = tong_tien
        self.ngay_nhap = ngay_nhap

class ChiTietHoaDon(db.Model):
    __tablename__ = "chi_tiet_hoa_don"
    
    id = db.Column(db.Integer, primary_key=True)         
    don_gia = db.Column(db.Integer, nullable=False)
    so_luong = db.Column(db.Integer, nullable=False)
    id_hoa_don = db.Column(db.Integer, db.ForeignKey('hoa_don.id_hoa_don'), nullable=False)
    id_san_pham = db.Column(db.Integer, db.ForeignKey('san_pham.id_san_pham'), nullable=False)
    hoa_don = db.relationship('HoaDon', backref=db.backref('chi_tiet_hoa_don', lazy=True))
    san_pham = db.relationship('SanPham', backref=db.backref('chi_tiet_hoa_don', lazy=True))

    def __init__(self, don_gia, so_luong, id_hoa_don, id_san_pham):
        self.don_gia = don_gia
        self.so_luong = so_luong
        self.id_hoa_don = id_hoa_don
        self.id_san_pham = id_san_pham

class ChiTietPhieuNhap(db.Model):
    __tablename__ = "chi_tiet_phieu_nhap"
    
    id = db.Column(db.Integer, primary_key=True)
    don_gia = db.Column(db.Integer, nullable=False)
    so_luong = db.Column(db.Integer, nullable=False)
    id_phieu = db.Column(db.Integer, db.ForeignKey('phieu_nhap.id_phieu'), nullable=False)
    id_san_pham = db.Column(db.Integer, db.ForeignKey('san_pham.id_san_pham'), nullable=False)
    phieu_nhap = db.relationship('PhieuNhap', backref=db.backref('chi_tiet_phieu_nhap', lazy=True))
    san_pham_nhap = db.relationship('SanPham', backref=db.backref('chi_tiet_phieu_nhap', lazy=True))

    def __init__(self, don_gia, so_luong, id_phieu, id_san_pham):
        self.don_gia = don_gia
        self.so_luong = so_luong
        self.id_phieu = id_phieu
        self.id_san_pham = id_san_pham