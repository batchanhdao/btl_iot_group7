# This file is executed on every boot (including wake-boot from deepsleep)
# import esp
# esp.osdebug(None)
# import webrepl
# webrepl.start()

import network
import sys

# Đưa thư mục lib-custom vào danh sách import
sys.path.append("/lib-custom")

# Kết nối wifi khi thiết bị khởi động
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print("connecting to network...")
    wlan.connect("ten-mang-wifi", "mat-khau")
    while not wlan.isconnected():
        pass
print("network config:", wlan.ifconfig())
