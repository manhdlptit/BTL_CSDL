# Đoạn mã dùng AI để chèn dữ liệu cho nhanh
import requests

# Địa chỉ URL của endpoint nhập hàng trên Flask của bạn
URL = "http://127.0.0.1:9999/nhap-hang"

# Danh sách 10 sản phẩm mẫu khớp 100% với form HTML (mỗi loại có ít nhất 1 sản phẩm)
danh_sach_10_san_pham = [
    # Loai 1: Áo khoác
    {"ma_san_pham": "AK001", "ten_san_pham": "Áo Khoác Gió Bomber", "kich_co": "L", "mo_ta": "Áo khoác dù 2 lớp chống nước nhẹ", "don_gia": 180000, "gia_ban": 320000, "so_luong": 30, "id_loai_san_pham": 1},
    
    # Loai 2: Áo phông
    {"ma_san_pham": "AP001", "ten_san_pham": "Áo Phông Cotton Basic", "kich_co": "M", "mo_ta": "Chất vải cotton 100% co giãn tốt", "don_gia": 75000, "gia_ban": 150000, "so_luong": 100, "id_loai_san_pham": 2},
    {"ma_san_pham": "AP002", "ten_san_pham": "Áo Phông Polo Nam", "kich_co": "XL", "mo_ta": "Áo polo cổ bẻ lịch sự, đi làm đi chơi đều hợp", "don_gia": 120000, "gia_ban": 220000, "so_luong": 50, "id_loai_san_pham": 2},
    
    # Loai 3: Áo dài tay
    {"ma_san_pham": "AD001", "ten_san_pham": "Áo Sweater Nỉ Trơn", "kich_co": "L", "mo_ta": "Áo nỉ dài tay phom rộng unisex", "don_gia": 140000, "gia_ban": 250000, "so_luong": 40, "id_loai_san_pham": 3},
    
    # Loai 4: Quần đùi
    {"ma_san_pham": "QD001", "ten_san_pham": "Quần Short Kaki Nam", "kich_co": "31", "mo_ta": "Quần short mặc ở nhà hoặc dạo phố", "don_gia": 85000, "gia_ban": 160000, "so_luong": 60, "id_loai_san_pham": 4},
    
    # Loai 5: Quần dài
    {"ma_san_pham": "QL001", "ten_san_pham": "Quần Jean Slimfit Xanh Gấu", "kich_co": "32", "mo_ta": "Quần jean co giãn dáng ôm trẻ trung", "don_gia": 210000, "gia_ban": 380000, "so_luong": 35, "id_loai_san_pham": 5},
    
    # Loai 6: Giày
    {"ma_san_pham": "GI001", "ten_san_pham": "Giày Thể Thao Sneaker Trắng", "kich_co": "42", "mo_ta": "Giày đi êm chân, đế cao su chống trượt", "don_gia": 320000, "gia_ban": 550000, "so_luong": 20, "id_loai_san_pham": 6},
    
    # Loai 7: Dép
    {"ma_san_pham": "DE001", "ten_san_pham": "Dép Quai Ngang Đúc Nguyên Khối", "kich_co": "41", "mo_ta": "Dép nhựa EVA siêu nhẹ đi trong nhà hoặc đi chơi", "don_gia": 45000, "gia_ban": 95000, "so_luong": 80, "id_loai_san_pham": 7},
    
    # Loai 8: Phụ kiện kết hợp
    {"ma_san_pham": "PK001", "ten_san_pham": "Thắt Lưng Da Nam Khóa Tự Động", "kich_co": "Free size", "mo_ta": "Thắt lưng da bò mặt khóa kim loại chống rỉ", "don_gia": 90000, "gia_ban": 190000, "so_luong": 45, "id_loai_san_pham": 8},
    {"ma_san_pham": "PK002", "ten_san_pham": "Mũ Lưỡi Trai Thêu Chữ", "kich_co": "Free size", "mo_ta": "Mũ kaki cao cấp thoáng mát", "don_gia": 35000, "gia_ban": 80000, "so_luong": 120, "id_loai_san_pham": 8}
]

def thuc_hien_insert():
    print("=== BẮT ĐẦU ĐẨY 10 SẢN PHẨM MẪU VÀO DATABASE ===")
    session = requests.Session() # Sử dụng session để tối ưu hóa kết nối
    
    thanh_cong = 0
    loi = 0
    
    for item in danh_sach_10_san_pham:
        # Gom dữ liệu theo đúng cấu trúc form HTML nhận diện qua request.form.get()
        payload = {
            "loai_nhap": "moi",
            "ma_san_pham": item["ma_san_pham"],
            "ten_san_pham": item["ten_san_pham"],
            "kich_co": item["kich_co"],
            "id_loai_san_pham": item["id_loai_san_pham"],
            "gia_ban": item["gia_ban"],
            "mo_ta": item["mo_ta"],
            "so_luong": item["so_luong"],
            "don_gia": item["don_gia"],
            "img_url": "" # Trường này trong backend nhận mặc định trống nếu không truyền
        }
        
        try:
            response = session.post(URL, data=payload)
            
            # Flask xử lý xong sẽ redirect (status 302 rồi về 200) 
            # nên check response thành công hoặc có lịch sử chuyển hướng là được
            if response.status_code == 200 or response.history:
                print(f" [+] Thành công: {item['ma_san_pham']} - {item['ten_san_pham']} (Loại ID: {item['id_loai_san_pham']})")
                thanh_cong += 1
            else:
                print(f" [-] Thất bại: {item['ma_san_pham']}. Lỗi từ server: {response.text}")
                loi += 1
                
        except Exception as e:
            print(f" [!] Lỗi mất kết nối tới server: {e}")
            loi += 1
            break

    print("--------------------------------------------------")
    print(f"KẾT QUẢ: Thành công {thanh_cong}/10 | Thất bại: {loi}")

if __name__ == "__main__":
    thuc_hien_insert()