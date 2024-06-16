import time
import datetime
import pyftdi.spi
from find_ft232h import find_ft232h
from PIL import Image, ImageDraw, ImageFont

D_C = 0x10
BUSY = 0x20
RESET = 0x40
CS = 0x80

SW_RESET = 0x12

DRIVER_OUTPUT_CONTROL = 0x01
GATE_DRIVING_VOLTAGE_CONTROL = 0x03

DATA_ENTRY_MODE_SETTING = 0x11  # 0x03 Default
X_DEC_Y_DEC = 0x00
X_INC_Y_DEC = 0x01
X_DEC_Y_INC = 0x02
X_INC_Y_INC = 0x03
ADDR_Y_DIR = 0x04

SET_RAM_X_ADDRESS = 0x44  # 0x00, 0x15 Default
SET_RAM_Y_ADDRESS = 0x45  # 0x00, 0x127 Default

BORDER_WAVEFORM_CONTROL = 0x3C  # 0xc0 Default

TEMPERATURE_SENSOR_CONTROL = 0x18  # 0x48 - external Default, 0x80 - internal
TEMPERATURE_SENSOR_WRITE = 0x1A  # 2 bytes
TEMPERATURE_SENSOR_READ = 0x1B  # 2 bytes

MASTER_ACTIVATION = 0x20
DISPLAY_UPDATE_CONTROL_1 = 0x21
DISPLAY_UPDATE_CONTROL_2 = 0x22  # 0xff Default

LUT = 0x32
lut_partial = [0x0, 0x40, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
               0x80, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
               0x40, 0x40, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
               0x0, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
               0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
               0x0A, 0x0, 0x0, 0x0, 0x0, 0x0, 0x2,
               0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
               0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
               0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
               0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
               0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
               0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
               0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
               0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
               0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
               0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
               0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
               0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x0, 0x0, 0x0, ]

READ_RAM = 0x27
WRITE_RAM = 0x24

RAM_X = 0x4e
RAM_Y = 0x4f

BOOSTER_SOFT_START_CONTROL = 0x0C  # 0x8b, 0x9c, 0x96 0x0f Default

NOP = 0x7f

SPI_FREQ = 10E6

spi = pyftdi.spi.SpiController(cs_count=1)
spi.configure(find_ft232h())
eink = spi.get_port(cs=0, freq=SPI_FREQ, mode=0)

gpio = spi.get_gpio()
gpio.set_direction(CS | BUSY | D_C | RESET, CS | D_C | RESET)
gpio.write(CS | RESET | D_C)


def write_command(command, data=None):
    gpio.write(RESET)
    eink.write(out=command)
    if data:
        gpio.write(RESET | D_C)
        eink.write(out=data)
    gpio.write(CS | RESET | D_C)


def read_data(command, length) -> bytes:
    gpio.write(RESET)
    eink.write(out=command)
    gpio.write(RESET | D_C)
    r_data = eink.exchange(readlen=length, duplex=False)
    gpio.write(CS | RESET | D_C)
    return r_data


def wait_busy():
    while gpio.read() & BUSY:
        time.sleep(0.1)


def write_screen(image):
    write_command([RAM_X], [0x0f])
    write_command([RAM_Y], [0x00, 0x00])
    write_command([WRITE_RAM], image)
    write_command([NOP])
    write_command([MASTER_ACTIVATION])
    wait_busy()


def screen_refresh():
    # screen = [0x00] * 4736
    # write_screen(screen)
    screen = [0xff] * 4736
    write_screen(screen)
    wait_busy()


# 1. Power On
time.sleep(0.01)
# 2. Set Initial Configuration
gpio.write(D_C)
time.sleep(0.1)
gpio.write(RESET | D_C)
time.sleep(0.1)
write_command([SW_RESET])
time.sleep(0.01)
# 3. Send Initialization Code
write_command([DRIVER_OUTPUT_CONTROL], [0x27, 0x01, 0x01])
write_command([DATA_ENTRY_MODE_SETTING], [X_DEC_Y_INC])
write_command([0x47], [0x64])
write_command([SET_RAM_X_ADDRESS], [0x0f, 0x00])
write_command([SET_RAM_Y_ADDRESS], [0x00, 0x00, 0x27, 0x01])
write_command([BORDER_WAVEFORM_CONTROL], [0x05])
write_command([DISPLAY_UPDATE_CONTROL_1], [0x00, 0x80])
write_command([RAM_X], [0x00])
write_command([RAM_Y], [0x00, 0x00])
# 4. Load Waveform LUT
write_command([TEMPERATURE_SENSOR_CONTROL], [0x80])
# write_command([LUT], lut_partial)
write_command([DISPLAY_UPDATE_CONTROL_2], [0xff])
write_command([MASTER_ACTIVATION])
# 5. Write Image and Drive Display Panel
wait_busy()

image_path = 'masha.jpg'
img = Image.open(image_path)
img = img.resize((128, 296))
gamma = 1.0  # Гамма < 1 робить зображення яскравішим, > 1 - темнішим
img = img.point(lambda p: 255 * (p / 255) ** gamma)
img = img.convert('1')
bitmap = img.tobytes()

# bitmap = bytearray()
# for i in range(18):
#     bitmap.extend([0x00, 0xff] * 8 * 8)
#     bitmap.extend([0xff, 0x00] * 8 * 8)
# bitmap.extend([0x00, 0xff] * 8 * 8)

# font_path = 'ttf/static/CascadiaCode-Light.ttf'
# font_size = 16  # Розмір шрифту
# font = ImageFont.truetype(font_path, font_size)
# image = Image.new('1', (128, 296), 1)  # 200x200 пікселів, спочатку білий фон
# draw = ImageDraw.Draw(image)
# text = "Hello, World!"
# draw.text((10, 10), text, font=font, fill=0)  # Почати малювати з (10, 10), чорний текст
# bitmap = image.convert('1')
# bitmap = bitmap.tobytes()


screen_refresh()
write_screen(bitmap)
# time.sleep(3)
# screen_refresh()
# write_screen(bitmap2)
# time.sleep(3)
# screen_refresh()
# write_screen(bitmap3)
# time.sleep(3)
# screen_refresh()
# write_screen(bitmap4)
# time.sleep(3)

# write_command([RAM_X], [0x00])
# write_command([RAM_Y], [0x00, 0x00])
# data = read_data([READ_RAM], shape)
# print(bitmap)
# print((bytes(data)))
#
# if data == bitmap:
#     print('Data is equal')

# while True:
#     temperature = read_data([TEMPERATURE_SENSOR_READ], 2)
#     print(temperature)
#     temperature = int.from_bytes(temperature, byteorder='big', signed=True)
#     print(f"Temperature: {temperature/256}°C")
#     time.sleep(1)


# 0x10 Deep Sleep Mode
# 6. Power Off
