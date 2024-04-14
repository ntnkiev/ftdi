from time import sleep
from pyftdi.i2c import I2cController
from pyftdi.usbtools import UsbTools
from pyftdi.gpio import GpioController
import datetime
import time

# url = 'ftdi://ftdi:232h:1:3/1'  # 'ftdi://ftdi:232h:0:1/1'
# RED = 0xff  # fe
# YELLOW = 0x00  # fd
# GREEN = 0x00  # fb
#
# FT232H_VID = 0x0403
# FT232H_PID = 0x6014
#
# I2C_ADDRESS = 0x27
#
#
# # Отримати список всіх доступних FTDI пристроїв
# def find_ftdi_devices():
#     devices_info = UsbTools.find_all([(FT232H_VID, FT232H_PID)])  # VID і PID для FT232H, наприклад
#     if devices_info:
#         device = devices_info[0]
#         local_url = f'ftdi://ftdi:232h:{device[0].bus}:{hex(device[0].address)}/{device[1]}'
#         return local_url
#
#
# url = find_ftdi_devices()
# if not url:
#     raise Exception('FT232H device not found')
# print(url)
# ftdi = Ftdi()
# ftdi.open_from_url(url)
# print(ftdi.device_port_count)
# ftdi.close()

# gpio = GpioController()
# gpio.configure(url, direction=0x70)
# port = gpio.get_gpio()
#
# while True:
#     port.write(0x60)  # Встановити стан високий
#     sleep(0.5)
#     port.write(0x50)  # Встановити стан низький
#     sleep(0.5)
#     port.write(0x30)  # Встановити стан низький
#     sleep(0.5)

# i2c = I2cController()
# i2c.configure(url)
# i2c_port = i2c.get_port(I2C_ADDRESS)
# while True:
#     i2c_port.write([RED])
#     sleep(.5)
#     i2c_port.write([YELLOW])
#     sleep(.5)
#     i2c_port.write([GREEN])
#     sleep(.5)

print(datetime.date.today().strftime('%d-%m-%Y'))
print(time.strftime('%H:%M:%S'))

