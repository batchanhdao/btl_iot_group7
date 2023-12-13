import network

class Boot():
    def __init__(this):
        pass
    
    def ConnectWifi(this, ssid, password):
        # connect to wifi
        station = network.WLAN(network.STA_IF)
        station.active(True)
        station.connect(ssid, password)
        # connect fail
        while station.isconnected() == False:
          pass

        print('Connection successful')
        print(station.ifconfig())
    
    def Index(this, led, T_Tem, T_Hum):
            
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
                            function thongbao(){
                                window.alert("Cập nhập thành công");
                            }
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
                                <button type="submit" onclick="thongbao()"> update </button>
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


