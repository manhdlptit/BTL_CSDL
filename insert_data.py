import os
from app import create_app, db
from app.blueprints.model import LoaiSanPham  # Đảm bảo đường dẫn import chính xác

def insert_data():
    # Khởi tạo Application Context để có thể làm việc với Database của Flask
    app = create_app()
    with app.app_context():
        print("--- Bắt đầu chèn dữ liệu vào bảng loai_san_pham ---")
        
        # Danh sách dữ liệu tương ứng với các ID bạn yêu cầu
        danh_sach_loai = [
            {"id_loai_san_pham": 1, "ten_loai_san_pham": "Áo khoác"},
            {"id_loai_san_pham": 2, "ten_loai_san_pham": "Áo phông"},
            {"id_loai_san_pham": 3, "ten_loai_san_pham": "Áo dài tay"},
            {"id_loai_san_pham": 4, "ten_loai_san_pham": "Quần đùi"},
            {"id_loai_san_pham": 5, "ten_loai_san_pham": "Quần dài"},
            {"id_loai_san_pham": 6, "ten_loai_san_pham": "Giày"},
            {"id_loai_san_pham": 7, "ten_loai_san_pham": "Dép"},
            {"id_loai_san_pham": 8, "ten_loai_san_pham": "Phụ kiện kết hợp"},
        ]
        
        count = 0
        for data in danh_sach_loai:
            # Sửa Cảnh báo Legacy: Dùng db.session.get(Model, id) thay cho Model.query.get(id)
            ton_tai = db.session.get(LoaiSanPham, data["id_loai_san_pham"])
            
            if not ton_tai:
                # Cách xử lý lỗi __init__: Khởi tạo với 'ten_loai_san_pham' trước, 
                # sau đó gán thủ công 'id_loai_san_pham' vào đối tượng
                moi = LoaiSanPham(ten_loai_san_pham=data["ten_loai_san_pham"])
                moi.id_loai_san_pham = data["id_loai_san_pham"]
                
                db.session.add(moi)
                count += 1
                print(f" Đã thêm: {data['ten_loai_san_pham']} (ID: {data['id_loai_san_pham']})")
            else:
                print(f" Bỏ qua: {data['ten_loai_san_pham']} (ID: {data['id_loai_san_pham']}) đã tồn tại.")
        
        # Lưu thay đổi vào database
        if count > 0:
            db.session.commit()
            print(f"--- Thành công! Đã chèn mới {count} danh mục vào database. ---")
        else:
            print("--- Không có dữ liệu mới nào được thêm (Tất cả đã tồn tại trước đó). ---")

if __name__ == "__main__":
    insert_data()