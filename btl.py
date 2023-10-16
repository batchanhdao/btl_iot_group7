from machine import Pin
from time import sleep
import dht
import random

sensor = dht.DHT22(Pin(23))
led = Pin(2, Pin.OUT)
while True:
    try:
        sleep(2)
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
#         temp = random.randint(-40,80)
#         hum = random.randint(0,100)
        temp_f = temp * (9/5) + 32.0
        print('Temperature: %3.1f C' % temp)
        print('Temperature: %3.1f F' % temp_f)
        print('Humidity: %3.1f %%' % hum)
        led.on()
    except OSError as e:
        print('Failed to read sensor.')