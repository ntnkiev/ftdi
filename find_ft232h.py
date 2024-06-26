from pyftdi.usbtools import UsbTools

FT232H_VID = 0x0403
FT232H_PID = 0x6014

I2C_ADDRESS = 0x27


# Отримати список всіх доступних FT232H пристроїв
def find_ftdi_devices():
    devices_info = UsbTools.find_all([(FT232H_VID, FT232H_PID)])  # VID і PID для FT232H, наприклад
    if devices_info:
        device = devices_info[0]
        local_url = f'ftdi://ftdi:232h:{device[0].bus}:{hex(device[0].address)}/{device[1]}'
        return local_url


def find_ft232h() -> str:
    url = find_ftdi_devices()
    if not url:
        raise Exception('FT232H device not found')
    print(url)
    return url


if __name__ == '__main__':
    find_ft232h()
