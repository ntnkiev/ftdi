from time import sleep
from pyftdi.i2c import I2cController
from pyftdi.usbtools import UsbTools

# url = 'ftdi://ftdi:232h:1:3/1'  # 'ftdi://ftdi:232h:0:1/1'
RED = 0xfe
YELLOW = 0xfd
GREEN = 0xfb

FT232H_VID = 0x0403
FT232H_PID = 0x6014

I2C_ADDRESS = 0x21


# Отримати список всіх доступних FTDI пристроїв
def find_ftdi_devices():
    devices_info = UsbTools.find_all([(FT232H_VID, FT232H_PID)])  # VID і PID для FT232H, наприклад
    if devices_info:
        device = devices_info[0]
        local_url = f'ftdi://ftdi:232h:{device[0].bus}:{hex(device[0].address)}/{device[1]}'
        return local_url


url = find_ftdi_devices()
print(url)
i2c = I2cController()
i2c.configure(url)
i2c_port = i2c.get_port(I2C_ADDRESS)
while True:
    i2c_port.write([RED])
    sleep(.5)
    i2c_port.write([YELLOW])
    sleep(.5)
    i2c_port.write([GREEN])
    sleep(.5)
