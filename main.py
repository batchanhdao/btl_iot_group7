import _thread
from time import sleep

import dht
from i2c_lcd import I2cLcd
from lcd_api import LcdApi
from machine import PWM, Pin, SoftI2C
from microWebSrv import MicroWebSrv

sensor = dht.DHT22(Pin(34))

# đặt biến nhiệt độ, độ ẩm
prev_temp = 1
new_temp = 1
prev_humid = 0
new_humid = 0
# khởi tạo màn hình LCD
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)
lcd = I2cLcd(i2c, 0x27, 2, 16)
# khởi tạo buzzer
buzzer = PWM(Pin(4))


# hàm lấy dữ liệu từ DHT22
def read_sensor():
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    return (temp, hum)


# hàm hiển thị ra màn hình LCD
def lcd_output(string):
    global lcd
    lcd.clear()
    lcd.putstr(string)


# hàm đổi màu LED RGB


# hàm điều khiển buzzer phát âm thanh cảnh báo
def play_tone(frequency):
    buzzer.duty_u16(1000)
    buzzer.freq(frequency)


def be_quiet():
    buzzer.duty_u16(0)


def play_song(song, tempo):
    for note in range(len(song)):
        # nếu nốt nhạc = rest, không phát âm thanh
        if song[note] == "R":
            be_quiet()
        # phát âm thanh ứng với tần số của nốt nhạc
        else:
            play_tone(tones[song[note]])
        # tiếp tục phát âm trong quãng thời gian ứng với độ dài một nốt nhạc
        sleep(60 / tempo)
    be_quiet()


# các hàm xử lý websocket
def _accept_websocket_callback(websocket, httpClient):
    print("WebSocket accepted")
    websocket.RecvTextCallback = _recv_text_callback
    websocket.RecvBinaryCallback = _recv_binary_callback
    websocket.ClosedCallback = _closed_callback

    # Gửi dữ liệu đến front-end khi nhiệt độ, độ ẩm thay đổi
    def send_dht_data():
        while True:
            temp, hum = read_sensor()
            websocket.SendText("{'temp': temp, 'humid': hum}")
            sleep(2)

    _thread.start_new_thread(send_dht_data, ())


# Hàm nhận lệnh từ front-end người dùng
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
