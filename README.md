# Hướng Dẫn Chạy Chương Trình

## 1. Tạo Môi Trường Ảo Python 3.9

### Trên Windows:
```sh
python -m venv venv
venv\Scripts\activate
```

### Trên MacOS/Linux:
```sh
python3 -m venv venv
source venv/bin/activate
```

## 2. Cài Đặt Thư Viện Yêu Cầu

Sau khi kích hoạt môi trường ảo, chạy lệnh sau để cài đặt các thư viện cần thiết:
```sh
pip install -r requirements.txt
```

## 3. Tổ Chức Thư Mục

### **file_csv_limit/**
Chứa các file `.csv` lấy từ CSDL để test thử, giới hạn 100 hàng.

### **file_csv_after_processed/**
Chứa các file `.csv` sau khi xử lý dữ liệu từ thư mục `file_csv_limit`.

### **process_csv_file/**
Chứa các file `.py` để xử lý dữ liệu từ file `.csv` trong thư mục `file_csv_limit` và lưu kết quả vào thư mục `file_csv_after_processed`.
- **processing_job_posting.py**: Xử lý dữ liệu bảng `job_posting` kết hợp (`join`) với bảng `company_detail`.
- **processing_experience.py**: Xử lý dữ liệu bảng `experience` kết hợp (`join`) với bảng `profile_info`.

### **export_to_csv.py**
Chạy file này để trích xuất dữ liệu từ CSDL và lưu vào các file `.csv` trong thư mục `file_csv_limit`.

Chạy bằng lệnh:
```sh
python export_to_csv.py
```

### **server_display_json_data.py**
Chạy server Flask để xem dữ liệu chi tiết từ một trong bốn bảng (`job_posting`, `company_detail`, `experience`, `profile_info`).

Chạy bằng lệnh:
```sh
python server_display_json_data.py
```

Sau đó mở trình duyệt và truy cập:
```
http://127.0.0.1:5000/profile_info/<public_id>
http://127.0.0.1:5000/experience/<public_id>
http://127.0.0.1:5000/company_detail/<int:id>
http://127.0.0.1:5000/job_posting/<int:id>
http://127.0.0.1:5000/job_posting/description/<int:id>
```
Ví dụ:
```
http://127.0.0.1:5000/profile_info/'adriane-smidht'
http://127.0.0.1:5000/company_detail/1000
http://127.0.0.1:5000/job_posting/description/3840686178
```

