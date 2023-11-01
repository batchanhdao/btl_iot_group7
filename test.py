try:
  import usocket as socket
except:
  import socket
import ujson
import network
from machine import Pin
import dht
import random

import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = 'Le Canh'
# ssid = 'Canh1'
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

led1 = Pin(2, Pin.OUT); led1.off()
ledTH = Pin(4, Pin.OUT); ledTH.off()
temp = 0
hum = 0
T_Tem = [20, 40]; temp_status = ""
T_Hum = [40, 60]; hum_status = ""



# tạo một đối tượng socket với hai tham số: socket.AF_INET chỉ định sử dụng IPv4
# và socket.SOCK_STREAM chỉ định sử dụng giao thức TCP.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# create server socket tcp with ip and port = 80 for http
s.bind(('', 80))
# đặt socket vào chế độ lắng nghe và chấp nhận tối đa 5 kết nối đồng thời từ các client
s.listen(5)

def web_page():
    led = ""
    global T_Tem, T_Hum
    if led1.value()==1:
        led = "ON"
        print('led on')
    if led1.value()==0:
        led = "OFF"
        print('led off')
    
    html_page = """<!DOCTYPE html>
            <html>

            <head>
              <title>Arduino and ESP32 Websocket</title>
              <meta name='viewport' content='width=device-width, initial-scale=1.0' />
              <meta charset='UTF-8'>
              <style>
                 html {font-family: Arial; display: inline-block; margin: 0px auto; text-align: center;}
                  h2 { font-size: 3.0rem; }
                  p { font-size: 2.0rem; }
                  .units { font-size: 1.2rem; }
                  .dht-labels{font-size: 2.0rem; vertical-align:middle; padding-bottom: 15px;}
                </style>
                <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
                <script> 
                    function receiveData(URL) {
                        var xhr = new XMLHttpRequest();
                        xhr.open("GET", URL, true);
                        xhr.onreadystatechange = function () {
                            if (xhr.readyState == 4 && xhr.status == 200) {
                                var data = JSON.parse(xhr.responseText);
                                document.getElementById("temp").innerHTML = data.temp;
                                document.getElementById("hum").innerHTML = data.hum;
                                document.getElementById("tempStatus").innerHTML = "| Status: " + data.temp_status;
                                document.getElementById("humStatus").innerHTML = "| Status: " + data.hum_status;
                                document.getElementById("ledStatus").innerHTML = data.led_status;
                            
                            }
                        };
                        xhr.send();
                    }

                    function updateData()   
                       {   
                         receiveData('getData');   
                       }  
                    // Gọi hàm updateData() mỗi 5 giây
                    setInterval(updateData, 5000);
                </script> 
            </head>
            <body>
                <h2>Group 7</h2>
                  <p>
                    <i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
                    <span class="dht-labels">Temperature</span> 
                    <span id="temp">--.--</span>
                    <sup class="units">&deg;C</sup>
                    <span id="tempStatus"> --.--</span>
                  </p>
                  <p>
                    <i class="fas fa-tint" style="color:#00add6;"></i> 
                    <span class="dht-labels">Humidity</span>
                    <span id="hum">--.--</span>
                    <sup class="units">%</sup>
                    <span id="humStatus"> --.--</span>
                  </p>
                  <p>
                    <i class="" style="color:#00add6;"></i> 
                    <span class="dht-labels">LED Notification:</span>
                    <span id="ledStatus">--.--</span>
                  </p>
                  <br>
                  <center>
                      <form method="POST" action="/set-temp-hum">
                        <span class="dht-labels">Temperature: </span>
                        <input type="text" name="tempDown" value= """ + str(T_Tem[0]) + """ >
                        <span>to</span>
                        <input type="text" name="tempUp" value= """ + str(T_Tem[1]) + """ >
                        <br>
                        <span class="dht-labels">Humidity: </span>
                        <input type="text" name="humDown" value= """ + str(T_Hum[0]) + """ >
                        <span>to</span>
                        <input type="text" name="humUp" value= """ + str(T_Hum[1]) + """ >
                        <br>
                        <button type="submit"> update </button>
                    </form>
                  </center>
                  <br>
                  <center>
                      <form>
                          <center><p>Led is: """ + led + """ </p></center>
                          <button type="submit" name="led1" value="1"> led on </button>
                          <button type="submit" name="led1" value="0"> led off </button>         
                      </form>
                  </center>
                  
            </body>

            </html>"""
    return html_page
        
response=""
while True:
#     socket accept
    conn, addr = s.accept()
    print("got connnection from" + str(addr))
#     got connnection from('192.168.1.9', 63260)
    
#     socket receive
    request = conn.recv(1024)
    print("----------")
    print("Content: " + str(request))
    request = str(request)
    if "led1=1" in request:
        led1.value(1)
    if "led1=0" in request:
        led1.value(0)
        
    if "POST /set-temp-hum" in request:
        vitri = request.find("tempDown")
        values = request[vitri : len(request)-1]
        print(values)
        values = values.split('&')
        tempDown, tempUp = values[0].split('='), values[1].split('=')
        humDown, humUp = values[2].split('='), values[3].split('=')
        T_Tem[0], T_Tem[1] = int(tempDown[1]), int(tempUp[1])
        T_Hum[0], T_Hum[1] = int(humDown[1]), int(humUp[1])

        
    response = web_page()
    
    if "getData" in request:
        temp = random.randint(-40,80)
        hum = random.randint(0,100)
        temp_status, hum_status, led_status = "", "", ""
        if temp > T_Tem[0] and temp < T_Tem[1]:
            temp_status = "normal"
        if temp <= T_Tem[0] or temp >= T_Tem[1]:
            temp_status = "warning"
        if hum > T_Hum[0] and hum < T_Hum[1]:
            hum_status = "normal"
        if hum <= T_Hum[0] or hum >= T_Hum[1]:
            hum_status = "warning"  
        if hum_status == 'warning' or temp_status == 'warning':
            ledTH.value(1)
        if hum_status == 'normal' and temp_status == 'normal':
            ledTH.value(0)
        if ledTH.value()==1:
            led_status = "LIGHT"
        if ledTH.value()==0:
            led_status = "DANK"


        data = {
            "temp": temp,  # Giá trị nhiệt độ từ MicroPython
            "hum": hum,    # Giá trị độ ẩm từ MicroPython
            "temp_status": temp_status,  # Trạng thái nhiệt độ (normal hoặc warning)
            "hum_status": hum_status,      # Trạng thái độ ẩm (normal hoặc warning)
            "led_status": led_status
        }
        response = ujson.dumps(data)

    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()






