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
    
    def Index(this):
            
        html_page = """<!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Weboscoket MQTT</title>
                <style>
                    body {
                        /* background-color: #E6D8D5; */
                        text-align: center;
                    }
                </style>
                <script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>
                <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            </head>

            <body>
                <div>
                    <h1>Lê Hồng Ánh - B20DCCN083</h1>
                    <h1>Temperature: <span id='temp'>-</span></h1>
                    <h1>Humidity: <span id='hum'>-</span></h1>

                </div>
                <div>
                    <canvas id="myChartTemp"></canvas>
                </div>
                <div>
                    <canvas id="myChartHum"></canvas>
                </div>
                <a href="weather.html">View Local Weather</a>

            </body>
            <script>
                const ctxTemp = document.getElementById('myChartTemp');
                const ctxHum = document.getElementById('myChartHum');
                let myChartTemp;
                let myChartHum;
                // Mảng để lưu trữ dữ liệu nhiệt độ và độ ẩm
                const temperatureData = [];
                const humidityData = [];
                const timeData = [];

                // Hàm để thêm dữ liệu mới vào mảng và vẽ biểu đồ
                function addDataAndDrawChartTemp() {

                    // Chỉ hiển thị 30 điểm dữ liệu mới nhất
                    if (temperatureData.length > 20) {
                        temperatureData.shift();
                    }

                    console.log(timeData)

                    // Update the existing chart with new data
                    if (myChartTemp) {
                        myChartTemp.data.labels = timeData;
                        myChartTemp.data.datasets.data = temperatureData;
                        myChartTemp.update();
                    } else {
                        // Create a new chart if it doesn't exist
                        myChartTemp = new Chart(ctxTemp, {
                            type: 'line',
                            data: {
                                // labels: Array.from({ length: temperatureData.length }, (_, i) => i + 1),
                                labels: timeData,
                                datasets: [
                                    {
                                        label: 'Temperature (°C)',
                                        data: temperatureData,
                                        borderColor: 'rgba(255, 99, 132, 1)',
                                        borderWidth: 2,
                                        fill: false,
                                    },
                                ],
                            },
                        });
                    }
                }


                // Hàm để thêm dữ liệu mới vào mảng và vẽ biểu đồ
                function addDataAndDrawChartHum() {
                    console.log(temperatureData);
                    console.log(humidityData);

                    // Chỉ hiển thị 30 điểm dữ liệu mới nhất
                    if (humidityData.length > 20) {
                        humidityData.shift();
                    }
                    console.log(timeData)

                    // Update the existing chart with new data
                    if (myChartHum) {
                        myChartHum.data.labels = timeData;
                        myChartHum.data.datasets.data = humidityData;
                        myChartHum.update();
                    } else {
                        // Create a new chart if it doesn't exist
                        myChartHum = new Chart(ctxHum, {
                            type: 'line',
                            data: {
                                // labels: Array.from({ length: temperatureData.length }, (_, i) => i + 1),
                                labels: timeData,
                                datasets: [
                                    {
                                        label: 'Humidity (%)',
                                        data: humidityData,
                                        borderColor: 'rgba(75, 192, 192, 1)',
                                        borderWidth: 2,
                                        fill: false,
                                    },
                                ],
                            },
                        });
                    }
                }



                const clientId = 'mqttjs_' + Math.random().toString(16).substr(2, 8)
                const host = 'ws://broker.hivemq.com:8000/mqtt'
                const options = {
                    keepalive: 60,
                    clientId: clientId,
                    protocolId: 'MQTT',
                    protocolVersion: 4,
                    clean: true,
                    reconnectPeriod: 1000,
                    connectTimeout: 30 * 1000,
                    will: {
                        topic: 'WillMsg',
                        payload: 'Connection Closed abnormally..!',
                        qos: 0,
                        retain: false
                    },
                }
                console.log('Connecting mqtt client');
                const client = mqtt.connect(host, options);
                client.on('error', (err) => {
                    console.log('Connection error: ', err);
                    client.end();
                })
                client.on('reconnect', () => {
                    console.log('Reconnecting...');
                })

                const topicTem = '/iot/group7/temp'
                const topicHum = '/iot/group7/hum'
                client.on('connect', () => {
                    console.log(`Client connected: ${clientId}`);
                    client.subscribe([topicTem], () => {
                        console.log(`Subscribe to topic '${topicTem}'`)
                        // client.publish(topicTem, '40 C', { qos: 0, retain: false }, (error) => {
                        //     if (error) {
                        //         console.error(error)
                        //     }
                        // })
                    })
                    client.subscribe([topicHum], () => {
                        console.log(`Subscribe to topic '${topicHum}'`)
                        // client.publish(topicHum, '30', { qos: 0, retain: false }, (error) => {
                        //     if (error) {
                        //         console.error(error)
                        //     }
                        // })
                    })
                })

                // Receive
                client.on('message', (topic, message, packet) => {
                    let temp = 0;
                    let hum = 0;
                    console.log(`Received Message: ${message.toString()} On topic: ${topic}`);
                    if (topic == '/iot/group7/temp') {
                        const s_temp = message.toString();
                        document.getElementById('temp').innerHTML = s_temp;
                        temp = parseFloat(s_temp);
                        temperatureData.push(temp);
                    }
                    if (topic == '/iot/group7/hum') {
                        const s_hum = message.toString();
                        document.getElementById('hum').innerHTML = s_hum;
                        hum = parseFloat(s_hum);
                        humidityData.push(hum);
                    }
                    if (temperatureData.length == humidityData.length) {
                        date = new Date();
                        timeData.push(date.getSeconds().toString() + ":" + date.getMinutes().toString() + ":" + date.getHours().toString());
                        if (timeData.length > 20) {
                            timeData.shift();
                        }
                        addDataAndDrawChartTemp();
                        addDataAndDrawChartHum()
                    }

                })

            </script>

            </html>"""
        return html_page

