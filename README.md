# Bài tập lớn IoT
Hệ thống giám sát nhiệt độ, độ ẩm trong phòng.
[Tài liệu thiết kế](https://docs.google.com/document/d/1nviKiFsDmlR3RfjStg4YKHOSAtpBClvGuQ-qJb5EANo/)

## Danh sách tệp và thư mục
- `/lib-custom/` dùng để chứa các thư viện bên thứ ba mà không được tạo bởi mip.
- `/www/` dùng để chứa các tệp HTML, JS, CSS được sử dụng bởi webserver trên ESP32.
- `boot.py` được tự động thực thi khi thiết bị khởi động nguồn.
- `main.py` cũng được tự động thực thi khi thiết bị khởi động nguồn, sau khi `boot.py` thực thi xong.


server thứ 2 nhận dữ liệu nhiệt độ, độ ẩm từ hivemq và hiển thị ra màn hình 
vẽ biểu đồ.



