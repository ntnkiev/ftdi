import time
import datetime
import pyftdi.spi
from find_ft232h import find_ft232h

D_C = 0x10
BUSY = 0x20
RESET = 0x40

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

READ_RAM = 0x27
WRITE_RAM = 0x24

BOOSTER_SOFT_START_CONTROL = 0x0C  # 0x8b, 0x9c, 0x96 0x0f Default

SPI_FREQ = 10E5

spi = pyftdi.spi.SpiController(cs_count=1)
spi.configure(find_ft232h())
eink = spi.get_port(cs=0, freq=SPI_FREQ, mode=0)

gpio = spi.get_gpio()
gpio.set_direction(D_C | RESET, D_C | RESET)
gpio.write(RESET | D_C)


def write_command(command, data=None):
    gpio.write(RESET)
    eink.write(out=command)
    gpio.write(RESET | D_C)
    if data:
        eink.write(out=data)


def read_data(length) -> bytes:
    gpio.write(RESET | D_C)
    r_data = eink.read(length)
    return r_data


# 1. Power On
time.sleep(0.01)
# 2. Set Initial Configuration
gpio.write(D_C)
time.sleep(0.1)
gpio.write(RESET | D_C)
time.sleep(0.5)
write_command([SW_RESET])
time.sleep(0.01)
# 3. Send Initialization Code
write_command([DRIVER_OUTPUT_CONTROL], [0x80, 0x00, 0x00])
write_command([DATA_ENTRY_MODE_SETTING], [ADDR_Y_DIR | X_INC_Y_INC])
write_command([SET_RAM_X_ADDRESS], [0x00, 0x15])
write_command([SET_RAM_Y_ADDRESS], [0x00, 0x00, 0x01, 0x27])
write_command([BORDER_WAVEFORM_CONTROL], [0xc0])
# 4. Load Waveform LUT
write_command([TEMPERATURE_SENSOR_CONTROL], [0x80])
write_command([DISPLAY_UPDATE_CONTROL_2], [0xff])
write_command([MASTER_ACTIVATION])
# 5. Write Image and Drive Display Panel
while gpio.read() & BUSY == BUSY:  # Wait for BUSY pin to be LOW
    print("BUSY")
    time.sleep(0.01)

# for i in range(5):
#     write_command([TEMPERATURE_SENSOR_READ])
#     print(read_data(2))
#     time.sleep(1)


# write_command([READ_RAM])
# data = read_data(4736)
# with open("image.bin", "wb") as f:
#     f.write(data)
#     print("Image saved to image.bin")
write_data = [0xcc] * 4736
write_command([WRITE_RAM], write_data)
write_command([BOOSTER_SOFT_START_CONTROL], [0x8b, 0x9c, 0x96, 0x0f])
write_command([MASTER_ACTIVATION])
# 0x10 Deep Sleep Mode
# 6. Power Off
