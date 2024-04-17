from time import sleep
from pyftdi.i2c import I2cController
from pyftdi.usbtools import UsbTools
from pyftdi.gpio import GpioController
from pyftdi import FtdiLogger
from pyftdi.eeprom import FtdiEeprom
from pyftdi.ftdi import Ftdi
from pyftdi.misc import add_custom_devices, hexdump
from find_ft232h import find_ft232h

import datetime
import time


# FT232H_VID = 0x0403
# FT232H_PID = 0x6014
#
# I2C_ADDRESS = 0x27
url = find_ft232h()
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
eeprom = FtdiEeprom()
eeprom.open(url, size=args.size, model=args.eeprom)
if args.output:
    if args.output == '-':
        eeprom.save_config(stdout)
    else:
        with open(args.output, 'wt') as ofp:
            eeprom.save_config(ofp)

print(datetime.date.today().strftime('%d-%m-%Y'))
print(time.strftime('%H:%M:%S'))

