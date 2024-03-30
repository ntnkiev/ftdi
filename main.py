from pyftdi.ftdi import Ftdi
from pyftdi.i2c import I2cController

# Instantiate an I2C controller
i2c = I2cController()
try:
    # Ініціалізуємо контролер з адаптером FT232H
    i2c.configure('ftdi://ftdi:232h:1:a/1')

    # Скануємо всі можливі адреси на шині I2C (0x03 - 0x77)
    print('Сканування I2C шини...')
    for address in range(0x03, 0x78):
        try:
            i2c_port = i2c.get_port(address)
            i2c_port.exchange([0], readlen=1)
            print(f'Знайдено пристрій на адресі 0x{address:02X}')
        except IOError:
            # Якщо немає відповіді від пристрою, буде викинуто виняток
            continue
finally:
    # Закриваємо контролер I2c
    i2c.terminate()
# ftdi://ftdi:232h:1:a/1