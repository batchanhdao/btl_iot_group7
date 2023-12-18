# Bài tập lớn IoT
Đây là code phần máy chủ ngoài của hệ thống giám sát nhiệt độ, độ ẩm trong phòng.
[Tài liệu thiết kế](https://docs.google.com/document/d/1nviKiFsDmlR3RfjStg4YKHOSAtpBClvGuQ-qJb5EANo/)

## Danh sách tệp và thư mục
- `/anh/` chứa các file cảu máy chủ web bên ngoài
- `/anh/backend.py`: chứa các mã ở phía Backend
- `/anh/chart.html`: chứa các mã để trực quan hóa dữ liệu bằng biểu đồ
- `/anh/weather.html`: chứa các mã để nhận dữ liệu từ "openweathermap"
- `/anh/chat.html`: chứa các mã để nhân câu hỏi của người dùng và trả lời
- `/anh/data.txt`: là file lưu dữ liệu nhiệt độ - độ ẩm nhận được từ esp32
- `/anh/requiments.txt` là file chứa các thư viện cần có để chạy phía backend
