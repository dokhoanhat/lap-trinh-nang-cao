# Lập trình nâng cao

Bài tập xây dựng hệ thống quản lý thư viện

## Yêu cầu hệ thống

- Python 3.8 trở lên
- Virtualenv

## Hướng dẫn
Windows
```bash
# Khởi tạo virtualenv
python -m venv venv

# Kích hoạt virtualenv
.\venv\Scripts\activate

# Sau khi khởi tạo virtualenv
pip install -r requirements.txt

# start server
flask run
```
Linux
```bash
# Khởi tạo virtualenv
python -m venv venv

# Kích hoạt virtualenv
source venv/bin/activate

# Sau khi khởi tạo virtualenv
pip install -r requirements.txt

# start server
flask run
```
## Chú ý
- Lần đầu khởi tạo, hệ thống sẽ sinh ra file "sql.db" để làm database dự án
- Để tạo lại database, ta chỉ cần xóa file "sql.db" rồi restart lại server
- Thông tin đăng nhập thủ thư: admin/admin
- Thông tin đăng nhập user: a/1
