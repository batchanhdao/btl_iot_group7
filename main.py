from microWebSrv import MicroWebSrv
from time import sleep
import _thread

# đặt biến
current_temp = 1
new_temp = 1
current_humid = 0
new_humid = 0


# hàm lấy dữ liệu từ DHT22


# hàm hiển thị ra màn hình LCD


# hàm đổi màu LED RGB


# hàm điều khiển buzzer phát âm thanh cảnh báo


# các hàm xử lý websocket
def _accept_websocket_callback(websocket, httpClient):
    print("WebSocket accepted")
    websocket.RecvTextCallback = _recv_text_callback
    websocket.RecvBinaryCallback = _recv_binary_callback
    websocket.ClosedCallback = _closed_callback

    def send_dht_data():
        while True:
            websocket.SendText("{'temp': 1, 'humid': 0}")
            sleep(2)

    _thread.start_new_thread(send_dht_data, ())


def _recv_text_callback(websocket, message):
    print(f"WebSocket received text: {message}")


def _recv_binary_callback(websocket, data):
    print(f"WebSocket received data: {data}")


def _closed_callback(websocket):
    print("WebSocket closed")


# tạo máy chủ webserver
mws = MicroWebSrv(webPath="/www")  # TCP port 80 and files in /www
mws.AcceptWebSocketCallback = _accept_websocket_callback
mws.Start(threaded=True)
