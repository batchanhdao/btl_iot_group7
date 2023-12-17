# Bài tập lớn IoT
Hệ thống giám sát nhiệt độ, độ ẩm trong phòng.
[Tài liệu thiết kế](https://docs.google.com/document/d/1nviKiFsDmlR3RfjStg4YKHOSAtpBClvGuQ-qJb5EANo/)

## Danh sách tệp và thư mục
- `/lib-custom/` dùng để chứa các thư viện bên thứ ba mà không được tạo bởi mip.
- `/www/` dùng để chứa các tệp HTML, JS, CSS được sử dụng bởi webserver trên ESP32.
- `boot.py` được tự động thực thi khi thiết bị khởi động nguồn.
- `main.py` cũng được tự động thực thi khi thiết bị khởi động nguồn, sau khi `boot.py` thực thi xong.
- `/anh/` chứa các file cảu máy chủ web bên ngoài
- `/anh/backend.py`: chứa các mã ở phía Backend
- `/anh/chart.html`: chứa các mã để trực quan hóa dữ liệu bằng biểu đồ
- `/anh/weather.html`: chứa các mã để nhận dữ liệu từ "openweathermap"
- `/anh/chat.html`: chứa các mã để nhân câu hỏi của người dùng và trả lời
- `/anh/data.txt`: là file lưu dữ liệu nhiệt độ - độ ẩm nhận được từ esp32
- `/anh/requiments.txt` là file chứa các thư viện cần có để chạy phía backend



