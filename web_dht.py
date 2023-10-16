try:
  import usocket as socket
except:
  import socket

import network
from machine import Pin
import dht
import random

import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = 'Le Canh'
password = '16011710'


# connect to wifi
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)
# connect fail
while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())
# ---------------------------------------

# sensor = dht.DHT22(Pin(14))

def read_sensor():
    global temp, hum
    temp = random.randint(-40,80)
    hum = random.randint(0,100)
#     try:
#         sensor.measure()
#         temp = sensor.temperature()
#         hum = sensor.humidity()
#         if (isinstance(temp, float) and isinstance(hum, float)) or (isinstance(temp, int) and isinstance(hum, int)):
#             msg = (b'{0:3.1f},{1:3.1f}'.format(temp, hum))
#             temp = temp * (9/5) + 32.0
#             hum = round(hum, 2)
#             return(msg)
#         else:
#             return('Invalid sensor readings.')
#     except OSError as e:
#         return('Failed to read sensor.')

def web_page():
    html = """<!DOCTYPE><html>
    <head>
        <title> ESP32 DHT Server </title>
        <style>
         html {
           font-family: Arial;
           display: inline-block;
           margin: 0px auto;
           text-align: center;
          }
          h2 { font-size: 3.0rem; }
          p { font-size: 3.0rem; }
          .units { font-size: 1.2rem; }
          .dht-labels{
            font-size: 1.5rem;
            vertical-align:middle;
            padding-bottom: 15px;
          }
        </style>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    </head>
    <body>
        <h2>ESP DHT Server</h2>
        <p>
            <i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
            <span class="dht-labels">Temperature</span> 
            <span>"""+str(temp)+"""</span>
            <sup class="units">C</sup>
        </p>
        <p>
            <i class="fas fa-tint" style="color:#00add6;"></i> 
            <span class="dht-labels">Humidity</span>
            <span>"""+str(hum)+"""</span>
            <sup class="units">%</sup>
        </p>
    </body>
    </html>"""
    
    html1="""
<!DOCTYPE html>
<html>

<head>
  <title>Arduino and ESP32 Websocket</title>
  <meta name='viewport' content='width=device-width, initial-scale=1.0' />
  <meta charset='UTF-8'>
  <style>
    body {
      background-color: #E6D8D5;
      text-align: center;
    }
  </style>
</head>

<body>
  <h1>Temperature: <span id='temp'>-</span></h1>
  <h1>Humidity: <span id='hum'>-</span></h1>
  <h1>Received message: <span id='message'>-</span></h1>
  <button type='button' id='BTN_1'>
    <h1>ON</h1>
  </button>
  <button type='button' id='BTN_2'>
    <h1>OFF</h1>
  </button>
</body>
    <script>
        var Socket;
        document.getElementById('BTN_1').addEventListener('click', button_1_pressed);
        document.getElementById('BTN_2').addEventListener('click', button_2_pressed);
        function init() {
            Socket = new WebSocket('ws://' + window.location.hostname + ':80/');
        Socket.onmessage = function (event) { processCommand(event); }; }
        function processCommand(event) {
            var obj = JSON.parse(event.data);
        document.getElementById('message').innerHTML = obj.PIN_Status;
        document.getElementById('temp').innerHTML = obj.Temp;
        document.getElementById('hum').innerHTML = obj.Hum;
        console.log(obj.PIN_Status); console.log(obj.Temp); console.log(obj.Hum); }
        function button_1_pressed() { Socket.send('1'); }
        function button_2_pressed() { Socket.send('0'); }
        window.onload = function (event) { init(); }
    </script>

</html>"""

    return html

# Set up the socket server
# tạo một đối tượng socket với hai tham số: socket.AF_INET chỉ định sử dụng IPv4
# và socket.SOCK_STREAM chỉ định sử dụng giao thức TCP.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# create server socket tcp with ip and port = 80 for http
s.bind(('', 80))
# đặt socket vào chế độ lắng nghe và chấp nhận tối đa 5 kết nối đồng thời từ các client
s.listen(5)

while True:
    conn, addr = s.accept() # get connection and ip of client
    print('Got a connection from %s' % str(addr))
#   got data form client với dung lượng maximun là 1024 bytes và save on var request
    request = conn.recv(1024)
    print('Content = %s' % str(request))
    
    sensor_readings = read_sensor()
    print(sensor_readings)
    
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
#   send header for HTTP response để chỉ định content of type is text HTML
    conn.send('Content-Type: text/html\n')
#   connection will be close immediatety after response sent
    conn.send('Connection: close\n\n')
#     send content HTML to client
    conn.sendall(response)
    conn.close()
