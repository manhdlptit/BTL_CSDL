import sqlite3

def cap_nhat_anh_san_pham():
    # Kết nối tới file dữ liệu shop.db của bạn
    conn = sqlite3.connect('instance/shop.db')
    cursor = conn.cursor()
    
    # Danh sách cấu hình ảnh dựa theo Mã sản phẩm
    data_anh = [
        ("ao-khoac-bomber10.webp", "AK001")
        
        
        
    ]
    
    print("=== BẮT ĐẦU CẬP NHẬT ẢNH VÀO DATABASE ===")
    so_luong = 0
    
    for ten_anh, ma_sp in data_anh:
        # Câu lệnh SQL cập nhật cột img_url tìm theo ma_san_pham
        cursor.execute("UPDATE san_pham SET img_url = ? WHERE ma_san_pham = ?", (ten_anh, ma_sp))
        if cursor.rowcount > 0:
            print(f" [+] Đã cập nhật ảnh '{ten_anh}' cho sản phẩm {ma_sp}")
            so_luong += 1
            
    conn.commit()
    conn.close()
    print("--------------------------------------------------")
    print(f"KẾT QUẢ: Đã bổ sung ảnh thành công cho {so_luong}/10 sản phẩm!")

if __name__ == "__main__":
    cap_nhat_anh_san_pham()